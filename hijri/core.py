import math
from hijri.errors import HijriFormatError, HijriRangeError, HijriDateError
from hijri.constant import ummalqura, hijri_month


class Hijriah:
    def __init__(self, day, month, year) -> None:
        self.day = day
        self.month = month
        self.year = year

    def __str__(self) -> str:
        return f"{self.day}/{self.month}/{self.year}"

    def __repr__(self) -> str:
        return f"Hijriah(day={self.day}, month={self.month}, year={self.year})" # pragma: no cover

    def __eq__(self, other) -> bool:
        if not isinstance(other, Hijriah):
            raise NotImplementedError
        return (self.day, self.month, self.year) == (other.day, other.month, other.year)

    @classmethod
    def to_representation(cls, day, month, year, date_format: str) -> str:
        """Class method for represent formatted date whether in standard
        ISO or using ISO-8601
        """
        _year = int(year)
        _month = int(month)
        _day = int(day)

        if date_format == "ISO":
            # ISO 8601 date ordering as an object like: yyyy-dd-mm semantics,
            # kept as Hijriah instance for further implementation
            return cls(_day, _month, _year)
        elif date_format == "DMY":
            # DMY format previously was identical to the ISO branch format
            # even though they are conceptually within different format.
            # What actually distinguishes here, is the string representation
            # we return a Hijriah object which __str__ already renders
            # with the "day/month/year", in order to avoid deduplication
            # of ISO branch date format.
            return cls(_day, _month, _year)
        elif date_format == "ISO-8601":
            return f"{_year:04d}-{_month:02d}-{_day:02d}"
        else:
            raise HijriFormatError(f"Unknown date formatter: {date_format}")

    def get_hijri_month(self):
        """Method for formatted both calendar and returned as
        Islamic month name based on Hijriah calendar.
        """
        if not 1 <= self.month <= 12:
            raise ValueError("Invalid Hijri month")
        return hijri_month[self.month]

    def to_hijri(self):
        """Function for converting gregorian calendar day,
        to Hijriah calendar day. It's based on the Umm al-Qura calendar
        dataset, which is the official calendar used in Saudi Arabia
        """
        _day = int(self.day)
        _month = int(self.month)
        _year = int(self.year)

        # validation for inputted date from gregorian calendar
        self.validate_gregorian_range()

        # calculate julien calendar day number
        # see at: https://en.wikipedia.org/wiki/Julian_calendar
        # for January and February, month must be treated as 13 and 14
        # otherwise, the conversion result is off by years
        if _month <= 2:
            _year -= 1
            _month += 12

        # calculates the century number for the given year
        # and adjust for how the Gregorian calendar modifies the leap year rules
        # every 4 years = leap, except every 100 years = not leap, except every 400 years = leap
        century = _year // 100
        leap_years = 2 - century + (century // 4)

        julien_calendar_day = (
            math.floor(365.25 * (_year + 4716))
            + math.floor(30.6001 * (_month + 1))
            + _day
            + leap_years
            - 1524
        )

        modified_julien = math.floor(julien_calendar_day)
        reduced_julien_day = modified_julien - 2400000

        # find lunation index for the given julien calendar day
        # calculate modified julien calendar day
        # and indexing the lunation of Umm al-Qura calendar
        key = None
        for index, value in enumerate(ummalqura):
            if value > reduced_julien_day:
                key = index
                break

        if key is None:
            raise HijriRangeError("Date is out of range for calendar conversion")

        # guard the result if it's equal to 0 which indexed
        # last element of array
        if key == 0:
            raise HijriRangeError("Date before supported range for calendar conversion")

        # calculate the Umm al-Qura calendar
        month_index = key - 1

        # total months since 1 Muharram 1343 AH (starting point from this lbirary)
        total_months = month_index
        hijri_year = 1343 + (total_months // 12)
        hijri_month_number = (total_months % 12) + 1
        hijri_day = reduced_julien_day - ummalqura[month_index] + 1

        # guard hijriah day into explicit range instead of relying on tuple comparison
        if not 1 <= hijri_day <= 30:
            raise HijriRangeError(
                "Computed Hijriah day is out of valid range. Indicates indexing issue"
            )

        result = Hijriah(day=hijri_day, month=hijri_month_number, year=hijri_year)

        # validate the resulting hijri date to prevent
        # silent OverflowErrorw when date is exceeded
        result.validate_hijri_range()
        return result

    def to_gregorian(self):
        """Function for converting hijriah calendar day,
        to Gregorian calendar day.

        Work in progress, needs to be converted into
        julien calendar day cause the outcome is the index
        out of range
        """
        _day = int(self.day)
        _month = int(self.month)
        _year = int(self.year)

        # validation for gregorian calendar
        if not self.validate_calendar():
            return False

        in_year = _year
        in_month = _month
        in_day = _day
        in_one_year = in_year - 1
        lunation = (in_one_year * 12) + 1 + (in_month - 1)
        index = lunation - 16260

        # indexing the modified julien calendar day,
        # and calculate the result
        modified_julien = in_day + ummalqura[index - 1] - 1
        julien_calendar_day = modified_julien + 2400000

        return self._julian_to_gregorian(day=julien_calendar_day)

    @staticmethod
    def _julian_to_gregorian(day: int):
        """Convert a Julian day number to a Gregorian calendar date
        using the standard conversion (fliegel & van flandern).
        """

        # references: https://ui.adsabs.harvard.edu/scan/manifest/1983IAPPP..13...16F

        # shift epoch so days count up from a fixed reference
        # point to Gregorian calendar. This is a trick that pushes
        # from leap day (29 February) to the last day of the year
        days_since_epochs = day + 32044

        # count completed 480 years Gregorian cycles. However,
        # since every fourth year is a leap year, then it's not
        # divisible by 400. So, 146097 is where the exact numbers
        # of days in the 400 Gregorian years with leap days
        completed_years = (4 * days_since_epochs + 3) // 146097
        days_within_400_years = days_since_epochs - (146097 * completed_years) // 4

        completed_four_years = (4 * days_within_400_years + 3) // 146097

        # days remain after removing those 400 years cycle
        days_within_400_years_cycle = (
            days_since_epochs - (146097 * completed_four_years) // 4
        )

        # this is a building blocks for leap year calculation
        completed_four_years_cycle = (4 * days_within_400_years_cycle + 3) // 1461

        # days remain after removing those 4 years cycle
        days_within_4_years_cycle = (
            days_within_400_years_cycle - (14601 * completed_four_years_cycle) // 4
        )

        march_based_index = (5 * days_within_4_years_cycle + 2) // 153
        _day = (days_within_4_years_cycle - (153 * march_based_index + 2) // 5) + 1

        # convert march based index back to the gregorian calendar,
        # the previous logic was runs 0..11 starting at March, so adding
        # 3 will realigns to the calendar months again
        month = march_based_index + 3 - 12 * (march_based_index // 10)

        # reconstruct overall calendar year
        year = (
            100 * completed_years
            + completed_four_years_cycle
            - 4800
            + (march_based_index // 10)
        )
        return Hijriah(day=_day, month=month, year=year)

    def validate_calendar(self):
        """Method for date validation."""
        if (
            self.day in ("", None)
            or self.month in ("", None)
            or self.year in ("", None)
        ):
            raise HijriDateError("Calendar fields can't be empty")
        return True

    def validate_hijri_range(self) -> None:
        offset_date = (1343, 1, 1)
        limit_date = (1500, 12, 30)
        check_date = (self.year, self.month, self.day)
        if not offset_date <= check_date <= limit_date:
            raise HijriRangeError("Hijriah date out of range / bounds")

    def validate_gregorian_range(self) -> None:
        offset_date = (1900, 1, 1)
        limit_date = (2100, 12, 31)
        check_Date = (self.year, self.month, self.day)
        if not offset_date <= check_Date <= limit_date:
            raise HijriRangeError("Gregorian calendar date out of range / bounds")
