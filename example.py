from hijri.core import Hijriah
from hijri.errors import HijriRangeError, HijriFormatError


def print_separator(title):
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print("=" * 50)


# Gregorian Hijri calendar
print_separator("Gregorian to Hijri Conversion")

gregorian = Hijriah(day=21, month=12, year=2025)
hijri_result = gregorian.to_hijri()
print(f"Gregorian: {gregorian} -> Hijri: {hijri_result}")

gregorian_result = Hijriah(day=1, month=1, year=2000)
hijri_result2 = gregorian_result.to_hijri()
print(f"Gregorian: {gregorian_result} -> Hijri: {hijri_result2}")

# get hijri month name
print_separator("Hijri Month Name")

for month in range(1, 13):
    _hijri = Hijriah(day=1, month=month, year=1447)
    print(f"Month {month:>2}: {_hijri.get_hijri_month()}")

# date format representation
print_separator("Date Format Representations")

# ISO format (returns Hijriah object, __str__ shows day/month/year)
iso_result = Hijriah.to_representation(day=21, month=12, year=2024, date_format="ISO")
print(f"ISO       : {iso_result}  (type: {type(iso_result).__name__})")

# DMY format (returns Hijriah object)
dmy_result = Hijriah.to_representation(day=11, month=9, year=2025, date_format="DMY")
print(f"DMY       : {dmy_result}  (type: {type(dmy_result).__name__})")

# ISO-8601 format (returns string)
iso8601_result = Hijriah.to_representation(
    day=21, month=12, year=2024, date_format="ISO-8601"
)
print(f"ISO-8601  : {iso8601_result}  (type: {type(iso8601_result).__name__})")

# calendar validation example
print_separator("Calendar Validation")

valid = Hijriah(day=15, month=6, year=1443)
print(f"Valid date {valid}: validate_calendar() = {valid.validate_calendar()}")

try:
    invalid = Hijriah(day="", month=6, year=1443)
    invalid.validate_calendar()
except ValueError as e:
    print(f"Empty day field: {e}")

try:
    invalid_hijr = Hijriah(day=1, month=13, year=1443)
    invalid_hijr.get_hijri_month()
except ValueError as e:
    print(f"Invalid month: {e}")

# range validation example
print_separator("Range Validation")

# Valid Gregorian range
valid_gregorian = Hijriah(day=15, month=6, year=2000)
try:
    valid_gregorian.validate_gregorian_range()
    print(f"Gregorian {valid_gregorian} is within valid range")
except HijriRangeError as e:
    print(f"Gregorian {valid_gregorian}: {e}")

# Out-of-bounds Gregorian
invalid_gregorian = Hijriah(day=1, month=1, year=1800)
try:
    invalid_gregorian.validate_gregorian_range()
except HijriRangeError as e:
    print(f"Gregorian {invalid_gregorian}: {e}")

# Valid Hijri range
valid_hijri = Hijriah(day=15, month=6, year=1400)
try:
    valid_hijri.validate_hijri_range()
    print(f"Hijri {valid_hijri} is within valid range")
except HijriRangeError as e:
    print(f"Hijri {valid_hijri}: {e}")

# Out-of-bounds Hijri
invalid_hijri = Hijriah(day=1, month=1, year=1600)
try:
    invalid_hijri.validate_hijri_range()
except HijriRangeError as e:
    print(f"Hijri {invalid_hijri}: {e}")

# invalid format error handling
print_separator("Invalid Format Handling")

try:
    Hijriah.to_representation(day=21, month=12, year=2024, date_format="INVALID")
except HijriFormatError as e:
    print(f"Invalid format: {e}")

# Hijri to gregorian (may returned inaccurate results)
print_separator("Hijri to Gregorian (Work in Progress)")

hijri = Hijriah(day=1, month=7, year=1447)
greg_result = hijri.to_gregorian()
print(f"Hijri: {hijri} -> Gregorian: {greg_result}")
print("(Note: to_gregorian() is a work in progress and may return incorrect results)")

# round trip example: Hijri -> Gregorian
print_separator("Round-trip Conversion")

start = Hijriah(day=21, month=12, year=2025)
hijri = start.to_hijri()
back = hijri.to_gregorian()
print(f"Start : {start}")
print(f"Hijri : {hijri}")
print(f"Back  : {back}")
