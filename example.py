from hijri.core import Hijriah


hijri = Hijriah(day=21, month=12, year=2025)
print(hijri.to_hijri())
print(hijri.get_hijri_month())
get_dmy = Hijriah.to_representation(day=11, month=9, year=2025, date_format="DMY")
print(get_dmy)
get_iso = Hijriah.to_representation(day=21, month=12, year=2024, date_format="ISO-8601")
print(get_iso)
