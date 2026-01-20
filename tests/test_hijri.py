import unittest
from hijri.core import Hijriah


class TestHijriCalendar(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.hijri = Hijriah(21, 12, 2012)

    def test_initialization(self):
        """Test Hijriah object initialization"""
        hijri = Hijriah(15, 6, 1443)
        self.assertEqual(hijri.day, 15)
        self.assertEqual(hijri.month, 6)
        self.assertEqual(hijri.year, 1443)

    def test_string_representation(self):
        """Test __str__ method returns correct format"""
        self.assertEqual(self.hijri.__str__(), "21/12/2012")
        self.assertNotEqual(self.hijri.__str__(), "2012/12/21")

    def test_get_hijri_month(self):
        """Test getting month name"""
        # Month 12 is Dzul Hijjah
        self.assertEqual(self.hijri.get_hijri_month(), "Dzul Hijjah")

        # Test with other months
        hijri_safar = Hijriah(1, 2, 1443)
        self.assertEqual(hijri_safar.get_hijri_month(), "Safar")

    def test_get_hijri_month_invalid(self):
        """Test getting month name with invalid month"""
        hijri_invalid = Hijriah(1, 13, 1443)
        with self.assertRaises(ValueError):
            hijri_invalid.get_hijri_month()

    def test_to_representation_iso(self):
        """Test to_representation with ISO format"""
        result = Hijriah.to_representation(21, 12, 2012, "ISO")
        self.assertIsInstance(result, Hijriah)
        self.assertEqual(str(result), "21/12/2012")

    def test_to_representation_dmy(self):
        """Test to_representation with DMY format"""
        result = Hijriah.to_representation(21, 12, 2012, "DMY")
        self.assertIsInstance(result, Hijriah)
        self.assertEqual(str(result), "21/12/2012")

    def test_to_representation_iso8601(self):
        """Test to_representation with ISO-8601 format"""
        result = Hijriah.to_representation(21, 12, 2012, "ISO-8601")
        self.assertEqual(result, "2012-12-21")

    def test_to_representation_invalid_format(self):
        """Test to_representation with invalid format"""
        with self.assertRaises(Exception):
            Hijriah.to_representation(21, 12, 2012, "INVALID")

    def test_validate_calendar(self):
        """Test validate_calendar method"""
        self.assertTrue(self.hijri.validate_calendar())

    def test_validate_calendar_empty_day(self):
        """Test validate_calendar with empty day"""
        hijri_invalid = Hijriah("", 12, 2012)
        with self.assertRaises(ValueError):
            hijri_invalid.validate_calendar()

    def test_validate_gregorian_range_valid(self):
        """Test validate_gregorian_range with valid date"""
        hijri_valid = Hijriah(15, 6, 2000)
        # Should not raise an exception
        hijri_valid.validate_gregorian_range()

    def test_validate_gregorian_range_out_of_bounds(self):
        """Test validate_gregorian_range with out of bounds date"""
        hijri_invalid = Hijriah(1, 1, 1800)
        with self.assertRaises(OverflowError):
            hijri_invalid.validate_gregorian_range()

    def test_validate_hijri_range_valid(self):
        """Test validate_hijri_range with valid date"""
        hijri_valid = Hijriah(15, 6, 1400)
        # Should not raise an exception
        hijri_valid.validate_hijri_range()

    def test_validate_hijri_range_out_of_bounds(self):
        """Test validate_hijri_range with out of bounds date"""
        hijri_invalid = Hijriah(1, 1, 1600)
        with self.assertRaises(OverflowError):
            hijri_invalid.validate_hijri_range()

    def test_to_hijri_conversion(self):
        """Test gregorian to hijri conversion"""
        # Test with a known date such as 2012-12-21 (Gregorian)
        hijri = Hijriah(21, 12, 2012)
        result = hijri.to_hijri()
        self.assertIsInstance(result, Hijriah)
        # Result should be a Hijriah object with valid day, month, year
        self.assertTrue(1 <= result.day <= 30)
        self.assertTrue(1 <= result.month <= 12)
        self.assertTrue(1343 <= result.year <= 1500)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
