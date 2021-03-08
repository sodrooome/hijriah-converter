import datetime, math
from hijri.constant import ummalqura, hijri_range, hijri_month


class Hijriah(object):
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def __str__(self):
        return f"{self.day}/{self.month}/{self.year}"

    @classmethod
    def to_representation(cls, day, month, year, date_format):
        """Class method for represent formatted date
        
        TODO: for future release, using standard ISO 8601 string
        """
        _year = int(year)
        _month = int(month)
        _day = int(day)

        if date_format == "ISO":
            return cls(_year, _month, _day)
        elif date_format == "DMY":
            return cls(_day, _month, _year)
        elif date_format == "ISO-8601":
            pass
        else:
            raise Exception("Unknown formatter date")

    def get_hijri_month(self):
        """Method for formatted both calendar and returned as
        month name based on Hijriah calendar.

        Temporary, i'm using tricky way for get the month attributes
        """
        return hijri_month[self.month]

    def to_hijri(self):
        """Function for converting gregorian calendar day,
        to Hijriah calendar day.

        TODO: fix the returned values (still zero)
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
            math.floor(365.25 * (_year + 4176))
            + math.floor(30.6001 * (_month + 1))
            + _day
            - julien_gregorian
            - 1524
        )
        offset_limit = math.floor((julien_calendar_day - 1867216.25) / 36524.25)

        # calculate modified julien calendar day
        # and indexing the lunation of Umm al-Qura calendar
        modified_julien = julien_calendar_day - 2400000
        for key, value in enumerate(ummalqura):
            if key > modified_julien:
                return key
        # lunation = ummalqura[modified_julien]

        # calculate the Umm al-Qura calendar
        index = key + 16260
        in_one_year = math.floor((index - 1) / 12)
        in_year = in_one_year + 1
        in_month = in_year - 12 * in_one_year
        in_day = modified_julien - ummalqura[index - 1] + 1
        result = ummalqura[index] - ummalqura[index - 1]
        return Hijriah(in_day, in_month, in_year)

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
        return self.to_gregorian(julien_calendar_day)

    def to_julien(self):
        # TODO: convert the gregorian calendar into julien calendar
        pass

    # future notes: override base exception and create
    # custom exception for this validation
    def validate_calendar(self):
        """Method for date validation."""
        if self.day and self.month and self.year == "":
            raise Exception("Calendar can't be set into empty value")
        elif self.day and self.month and self.year is None:
            raise Exception("Calendar can't be set into None type")
        else:
            raise Exception("Unknown exception for this calendar")

    def validate_hijri_range(self):
        offset_date = (1343, 1, 1)
        limit_date = (1500, 12, 30)
        check_date = (self.day, self.month, self.year)
        if offset_date <= check_date <= limit_date:
            pass
        else:
            raise OverflowError("Hijriah date out of range / bounds")

    def validate_gregorian_range(self):
        offset_date = (1, 1, 1900)
        limit_date = (31, 12, 2100)
        check_Date = (self.day, self.month, self.year)
        if not offset_date <= check_Date <= limit_date:
            raise OverflowError("Gregorian calendar date out of range / bounds")


# example only, probably split into another modules
test = Hijriah
print(test.to_representation(1, 1, 1945, "DMY").to_hijri())
print(test.to_representation(21, 1, 2021, "ISO").get_hijri_month())
print(test(21, 2, 2009).get_hijri_month())
