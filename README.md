## Hijriah Date Converter

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/hijri-calendar?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/hijri-calendar) [![codecov](https://codecov.io/gh/sodrooome/hijriah-converter/graph/badge.svg?token=6SHZWUEMRS)](https://codecov.io/gh/sodrooome/hijriah-converter)

A package to convert between Hijri and Gregorian calendar date using the Umm al-Qura calendar.

#### Installation

`pip install hijri-calendar`

#### Features

- Supported ISO and another extendable date format
- Representation to string with formatted name of the month based on hijriah calendar
- Offset and limit range for both calendar

#### Usage

The usage itself is quite straightforward, just input the gregorian or hijri version of the calendar with something like:

```python
from hijri.core import Hijriah

# convert gregorian calendar day into hijriah
>>> gregorian = Hijriah(day=21, month=12, year=2025)
>>> print(gregorian.to_hijri())
1/7/1447

# get the hijri month name from the month number
>>> hijri = Hijriah(day=21, month=12, year=2025)
>>> print(hijri.get_hijri_month())
Dzul Hijjah

# convert into standard ISO date format (returns Hijriah object)
>>> get_iso = Hijriah.to_representation(day=21, month=12, year=2024, date_format="ISO")
>>> print(get_iso)
21/12/2024

# convert into ISO-8601 string format
>>> get_iso = Hijriah.to_representation(day=21, month=12, year=2024, date_format="ISO-8601")
>>> print(get_iso)
2024-12-21

# convert into DMY format (returns Hijriah object)
>>> get_dmy = Hijriah.to_representation(day=11, month=9, year=2025, date_format="DMY")
>>> print(get_dmy)
11/9/2025
```

For further usage, please refer to the `example.py` file

> [!WARNING]
> The `to_gregorian()` method (converting Hijri to Gregorian) is still a work in progress and may return incorrect results.

#### Acknowledgment

For the calculation formula itself i adopted from several resources and packages, especially with these two, [Python Islamic Library](https://github.com/abougouffa/pyIslam) and [Hijri.js](https://github.com/xsoh/Hijri.js)

#### Caveats

For accuracy itself, to be honest i don't really know how accurate it is for calendar conversion. For example, if we inputted the current date (from 2021), the conversion result to the hijri year is 1455 which is actually wrong. After some research, there is a leap day in the Hijri calendar which will increase every 2 or 3 years and there are also 11 leap years in a 30-year cycle. Their distribution varies slightly from one country or Muslim community to another.

In addition to the leap days that inserted in solar calendars like the Gregorian calendar or Julien Calendar, the Hijriah leap day is not designed to align the calendar with the solar year, which on average lasts just over 365 days.

Furthermore, this makes the calculation of the months in Hijriah calendar is difficult to predict / compute. For example, bad weather conditions may delay the beginning of a new month by one day at short notice.