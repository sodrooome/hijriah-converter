import math
from hijri.constant import ummalqura, hijri_month


class Hijriah:
    def __init__(self, day, month, year) -> None:
        self.day = day
        self.month = month
        self.year = year

    def __str__(self):
        return f"{self.day}/{self.month}/{self.year}"

    @classmethod
    def to_representation(cls, day, month, year, date_format: str) -> str:
        """Class method for represent formatted date whether in standard
        ISO or using ISO-8601
        """
        _year = int(year)
        _month = int(month)
        _day = int(day)

        if date_format == "ISO":
            return cls(_day, _month, _year)
        elif date_format == "DMY":
            return cls(_day, _month, _year)
        elif date_format == "ISO-8601":
            return f"{_year:04d}-{_month:02d}-{_day:02d}"
        else:
            raise Exception("Unknown formatter date")

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
            raise ValueError("Date is out of range for calendar conversion")

        # guard the result if it's equal to 0 which indexed
        # last element of array
        if key == 0:
            raise ValueError("Date before supported range for calendar conversion")

        # calculate the Umm al-Qura calendar
        month_index = key - 1

        # total months since 1 Muharram 1343 AH (starting point from this lbirary)
        total_months = month_index
        hijri_year = 1343 + (total_months // 12)
        hijri_month = (total_months % 12) + 1
        hijri_day = reduced_julien_day - ummalqura[month_index] + 1
        result = Hijriah(day=hijri_day, month=hijri_month, year=hijri_year)

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

        # TODO: this will causing an infinite loops bug
        return self.to_gregorian(julien_calendar_day)

    def to_julien(self):
        # TODO: convert the gregorian calendar into julien calendar
        raise NotImplementedError("This function is not being implemented yet")

    # future notes: override base exception and create
    # custom exception for this validation
    def validate_calendar(self):
        """Method for date validation."""
        if (
            self.day in ("", None)
            or self.month in ("", None)
            or self.year in ("", None)
        ):
            raise ValueError("Calendar fields can't be empty")
        return True

    def validate_hijri_range(self):
        offset_date = (1343, 1, 1)
        limit_date = (1500, 12, 30)
        check_date = (self.year, self.month, self.day)
        if not offset_date <= check_date <= limit_date:
            raise OverflowError("Hijriah date out of range / bounds")

    def validate_gregorian_range(self):
        offset_date = (1900, 1, 1)
        limit_date = (2100, 12, 31)
        check_Date = (self.year, self.month, self.day)
        if not offset_date <= check_Date <= limit_date:
            raise OverflowError("Gregorian calendar date out of range / bounds")
