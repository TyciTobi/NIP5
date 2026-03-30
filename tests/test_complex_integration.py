import pytest

from src.models import Parameters
from src.manager import Manager


def test_get_apartment_costs_nonexistent_apartment():
    parameters = Parameters()
    manager = Manager(parameters)

    with pytest.raises(KeyError):
        manager.get_apartment_costs('non-existent-apartment', 2025, 1)


def test_get_apartment_costs_no_bills_in_month():
    parameters = Parameters()
    manager = Manager(parameters)
    total = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert total == 0.0


def test_get_apartment_costs_sum_for_month():
    parameters = Parameters()
    manager = Manager(parameters)
    total = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert total == 910.0
