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
        to Hijriah calendar day.

        TODO: fix the returned values, the result still exceeds
        the current hijriah date (3 years for now)
        """
        _day = int(self.day)
        _month = int(self.month)
        _year = int(self.year)

        # validation for inputted date from gregorian calendar
        self.validate_gregorian_range()

        # offset and limit between gregorian and julien calendar
        offset = math.floor(_year / 100.0)
        julien_gregorian = offset - math.floor(offset / 4.0) - 2

        # calculate julien calendar day number
        # see at: https://en.wikipedia.org/wiki/Julian_calendar
        julien_calendar_day = (
            math.floor(365.25 * (_year + 4716))
            + math.floor(30.6001 * (_month + 1))
            + _day
            - julien_gregorian
            - 1524
        )

        # calculate modified julien calendar day
        # and indexing the lunation of Umm al-Qura calendar
        modified_julien = julien_calendar_day - 2400000
        for key, value in enumerate(ummalqura):
            if value > modified_julien:
                break
        # lunation = ummalqura[modified_julien]

        # calculate the Umm al-Qura calendar
        index = key + 16260
        in_one_year = math.floor((index - 1) / 12)
        in_year = in_one_year + 1
        in_month = index - 12 * in_one_year
        in_day = modified_julien - ummalqura[key - 1] + 1
        result = Hijriah(in_day, in_month, in_year)

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
        if offset_date <= check_date <= limit_date:
            pass
        else:
            raise OverflowError("Hijriah date out of range / bounds")

    def validate_gregorian_range(self):
        offset_date = (1900, 1, 1)
        limit_date = (2100, 12, 31)
        check_Date = (self.year, self.month, self.day)
        if not offset_date <= check_Date <= limit_date:
            raise OverflowError("Gregorian calendar date out of range / bounds")
