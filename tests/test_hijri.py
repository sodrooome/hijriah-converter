import pytest
from hijri.core import Hijriah


@pytest.fixture
def hijri():
    return Hijriah(21, 12, 2012)

def test_string_representation(hijri):
    assert True if hijri.__str__() == "21/12/2012" else False
    assert False if hijri.__str__() == (21, 12, 2012) else True

def test_get_month(hijri):
    assert True if hijri.get_hijri_month() == "Dzul Hijjah" else False
    assert False if hijri.get_hijri_month() == "Safar" else True

def test_mock_initial_params(hijri):
    assert hijri.day == 21
    assert hijri.month == 12
    assert hijri.year == 2012

def test_date_iso_representation(hijri):
    assert True if hijri.to_representation(21, 12, 2012, "ISO") != "2012/12/21" else False

def test_mock_initial_params_without_value(hijri):
    with pytest.raises(Exception) as e:
        object = hijri()