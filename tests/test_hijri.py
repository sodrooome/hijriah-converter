import unittest
from hijri.core import Hijriah
from hijri import core as core_module
from hijri.errors import HijriRangeError, HijriDateError
from unittest import mock


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
        with self.assertRaises(HijriRangeError):
            hijri_invalid.validate_gregorian_range()

    def test_validate_hijri_range_valid(self):
        """Test validate_hijri_range with valid date"""
        hijri_valid = Hijriah(15, 6, 1400)
        # Should not raise an exception
        hijri_valid.validate_hijri_range()

    def test_validate_hijri_range_out_of_bounds(self):
        """Test validate_hijri_range with out of bounds date"""
        hijri_invalid = Hijriah(1, 1, 1600)
        with self.assertRaises(HijriRangeError):
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

    def test_to_hijri_month_adjustment(self):
        """Test gregorian to hijri conversion for January/February months
        which should trigger the internal month/year adjustment
        (_month <= 2 branch)"""
        # Choose a date in January within supported range
        hijri = Hijriah(15, 1, 2012)
        result = hijri.to_hijri()
        self.assertIsInstance(result, Hijriah)
        # Basic sanity checks on the converted Hijri date
        self.assertTrue(1 <= result.day <= 30)
        self.assertTrue(1 <= result.month <= 12)
        self.assertTrue(1343 <= result.year <= 1500)

    def test_to_hijri_before_supported_range_raises(self):
        """Trigger the key == 0 branch which should raise for dates
        before the supported Umm al-Qura range"""

        # 1900-01-01 is within validate_gregorian_range but expected
        # to map before ummalqura[0], triggering the specific ValueError.
        hijri = Hijriah(1, 1, 1900)
        with self.assertRaises(ValueError) as cm:
            hijri.to_hijri()
        self.assertIn("Date before supported range", str(cm.exception))

    def test_to_hijri_out_of_range_raises(self):
        """Force a 'no lunation found' scenario (key is None) by
        temporarily shrinking the `ummalqura` table so the date is out
        of range and ensures the correct ValueError is raised"""

        # Patch the ummalqura table to small values so any realistic
        # reduced_julien_day will be larger and produce key == None
        with mock.patch.object(core_module, "ummalqura", (1, 2, 3)):
            hijri = Hijriah(1, 1, 2000)
            with self.assertRaises(ValueError) as cm:
                hijri.to_hijri()
            self.assertIn(
                "Date is out of range for calendar conversion", str(cm.exception)
            )

    def test_to_gregorian_conversion(self):
        """Test to_gregorian returns a Hijriah instance"""
        hijri = Hijriah(1, 1, 1356)
        result = hijri.to_gregorian()
        self.assertIsInstance(result, Hijriah)

    def test_to_gregorian_round_trip(self):
        """Test gregorian -> hijri -> gregorian returns a Hijriah instance"""
        hijri = Hijriah(21, 12, 2012)
        hijri_result = hijri.to_hijri()
        greg_result = hijri_result.to_gregorian()
        self.assertIsInstance(greg_result, Hijriah)

    def test_to_gregorian_invalid_calendar(self):
        """Test to_gregorian with empty day raises HijriDateError"""
        hijri_invalid = Hijriah("", 1, 1356)
        with self.assertRaises(ValueError):
            hijri_invalid.to_gregorian()

    def test_julian_to_gregorian_returns_hijriah(self):
        """Test _julian_to_gregorian returns a Hijriah instance"""
        result = Hijriah._julian_to_gregorian(2451677)
        self.assertIsInstance(result, Hijriah)

    def test_julian_to_gregorian_has_date_attributes(self):
        """Test _julian_to_gregorian result has day, month, year"""
        result = Hijriah._julian_to_gregorian(2451677)
        self.assertTrue(hasattr(result, "day"))
        self.assertTrue(hasattr(result, "month"))
        self.assertTrue(hasattr(result, "year"))

    def test_julian_to_gregorian_correct_value(self):
        """Regression test: JD 2451677 must resolve to 12 May 2000.
        Previously wrong divisors/typo'd constants made this arithmetic
        return nonsense dates."""
        result = Hijriah._julian_to_gregorian(2451677)
        self.assertEqual((result.day, result.month, result.year), (12, 5, 2000))

    def test_to_gregorian_round_trip_matches_original(self):
        """Regression test: gregorian -> hijri -> gregorian must return
        to the original date, not garbage. Also covers the lunation-index
        offset bug (was 16260, pointed at the wrong month entirely)."""
        original = Hijriah(21, 12, 2012)
        result = original.to_hijri().to_gregorian()
        self.assertEqual(result, original)

    def test_to_gregorian_matches_to_hijri_month_index(self):
        """Regression test: to_gregorian's lunation offset must line up
        with the same month_index base to_hijri() uses (1343 AH epoch)."""
        result = Hijriah(8, 2, 1434).to_gregorian()
        self.assertEqual((result.day, result.month, result.year), (21, 12, 2012))

    def test_eq_with_non_hijriah_returns_false(self):
        """Regression test: comparing against a non-Hijriah value must
        evaluate to False instead of raising NotImplementedError."""
        self.assertFalse(self.hijri == "21/12/2012")
        self.assertFalse(self.hijri == None)
        self.assertNotEqual(self.hijri, 42)

    def test_validate_gregorian_range_invalid_month(self):
        """Regression test: an in-range year must not mask an invalid
        month (tuple comparison alone let month=13 through)."""
        hijri_invalid = Hijriah(15, 13, 1950)
        with self.assertRaises(HijriRangeError):
            hijri_invalid.validate_gregorian_range()

    def test_validate_gregorian_range_invalid_day(self):
        """Regression test: day out of 1-31 must be rejected even when
        year/month are in range."""
        hijri_invalid = Hijriah(0, 6, 1950)
        with self.assertRaises(HijriRangeError):
            hijri_invalid.validate_gregorian_range()

    def test_validate_hijri_range_invalid_month(self):
        """Regression test: month out of 1-12 must be rejected even when
        year is in range."""
        hijri_invalid = Hijriah(15, 13, 1400)
        with self.assertRaises(HijriRangeError):
            hijri_invalid.validate_hijri_range()

    def test_to_gregorian_out_of_range_raises_range_error(self):
        """Regression test: to_gregorian() must reject an out-of-range
        hijri date with HijriRangeError instead of a raw IndexError
        from indexing the ummalqura table."""
        hijri_invalid = Hijriah(1, 1, 9999)
        with self.assertRaises(HijriRangeError):
            hijri_invalid.to_gregorian()


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
