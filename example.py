from hijri.core import Hijriah


test = Hijriah
print(test.to_representation(21, 12, 2012, "DMY").to_hijri())
print(test.to_representation(21, 1, 2021, "ISO").get_hijri_month())
print(test(21, 2, 2009).get_hijri_month())
print(test(28, 3, 2020).to_hijri())
print(test(28, 3, 2020).to_hijri().get_hijri_month())
