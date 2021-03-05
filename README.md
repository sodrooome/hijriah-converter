## Hijriah Date Converter

A package to convert between Hijri and Gregorian calendar date using the Umm al-Qura calendar.

#### Installation

Still work in progress

#### Features

- (Probably) supported ISO and another extendable date format
- Representation to string with formatted name of the month based on hijriah calendar
- Offset and limit range for both calendar

#### Usage

The usage itself is quite straightforward, just inputted the gregorian or hijri version of the calendar with something like:

```python
from hijri.core import Hijriah

# convert gregorian calendary day into hijriah
gregorian = Hijriah(23, 2, 2021)
print(gregorian.to_hijri())

# convert hijriah calendar day into gregorian
hijriah = Hijriah(1403, 2, 17)
print(hijriah.to_gregorian())
```

#### Acknowledgment

For the calculation formula itself i adopted from several packages, especially with these two, [Python Islamic Library](https://github.com/abougouffa/pyIslam) and [Hijri.js](https://github.com/xsoh/Hijri.js) for accuracy itself, i don't know how accurate it is for calendar conversion.