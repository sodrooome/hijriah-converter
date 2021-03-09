## Hijriah Date Converter

[![Build Status](https://travis-ci.com/sodrooome/hijriah-converter.svg?token=rHmyG6UiRrnXStqxuNMc&branch=master)](https://travis-ci.com/sodrooome/hijriah-converter) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hijri-calendar)

A package to convert between Hijri and Gregorian calendar date using the Umm al-Qura calendar.

#### Installation

`pip install hijri-calendar`

#### Features

- (Probably) supported ISO and another extendable date format
- Representation to string with formatted name of the month based on hijriah calendar
- Offset and limit range for both calendar

#### Usage

The usage itself is quite straightforward, just inputted the gregorian or hijri version of the calendar with something like:

```python
from hijri.core import Hijriah

# convert gregorian calendary day into hijriah
>>> gregorian = Hijriah(23, 3, 2021)
>>> print(gregorian.to_hijri())
'1455/8/1'

# getting hijri based month for both calendar
>>> example = Hijriah(21, 2, 2009).get_hijri_month()
>>> print(example)
'Safar'

# converting into ISO format
>>> example = Hijriah.to_representation(21, 2, 2009, "ISO")
>>> print(example)
'2009/21/2'
```

For further usage, please refer the `example.py` file

#### Acknowledgment

For the calculation formula itself i adopted from several resources and packages, especially with these two, [Python Islamic Library](https://github.com/abougouffa/pyIslam) and [Hijri.js](https://github.com/xsoh/Hijri.js)

#### Caveats

For accuracy itself, to be honest i don't really know how accurate it is for calendar conversion. For example, if we inputted the current date (from 2021), the conversion result to the hijri year is 1455 which is actually wrong. After some research, there is a leap day in the Hijri calendar which will increase every 2 or 3 years and there are also 11 leap years in a 30-year cycle. Their distribution varies slightly from one country or Muslim community to another.

In addition to the leap days that inserted in solar calendars like the Gregorian calendar or Julien Calendar, the Hijriah leap day is not designed to align the calendar with the solar year, which on average lasts just over 365 days.

Furthermore, this makes the calculation of the months in Hijriah calendar is difficult to predict / compute. For example, bad weather conditions may delay the beginning of a new month by one day at short notice.