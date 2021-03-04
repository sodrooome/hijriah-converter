from dateutil import parser


def parser(*args, **kwargs):
    date_object = parser.parse(*args, **kwargs)
    return date_object


@classmethod
def to_representation(date_object, date_format):
    """Method for represents ISO format."""
    format = None
    if format == "ISO":
        format = "%Y-%m-%dT%H:%M:%SZ"
    elif format == "DMY":
        format = "%d-%m-%Y"
    else:
        format = "%Y-%m-%d %H:%M:%S"
    return date_object.strftime(object)


def formatted_date(date_object, date_format):
    return to_representation(parser(date_object))
