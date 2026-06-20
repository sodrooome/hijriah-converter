"""Generic error classes which raised for hijri-calendar module"""


class HijriDateError(ValueError):
    """Raised when calendar fields are missing/empty"""


class HijriFormatError(ValueError):
    """Raise when an unknown date_format is passed"""


class HijriRangeError(ValueError):
    """Raise when a date falls outside the supported range"""
