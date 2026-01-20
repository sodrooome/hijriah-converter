from dateutil import parser as date_parser


def parser(*args, **kwargs):
    return date_parser.parse(*args, **kwargs)


def to_representation(date_object, date_format):
    """Method for represents ISO format"""
    if date_format == "ISO":
        fmt = "%Y-%m-%dT%H:%M:%SZ"
    elif date_format == "DMY":
        fmt = "%d-%m-%Y"
    else:
        fmt = "%Y-%m-%d %H:%M:%S"
    return date_object.strftime(fmt)


def formatted_date(date_string, date_format):
    date_object = parser(date_string)
    return to_representation(date_object, date_format)
