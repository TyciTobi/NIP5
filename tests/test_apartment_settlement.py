import pytest

from src.models import Parameters, Bill
from src.manager import Manager


def test_create_apartment_settlement_sums_bills_and_handles_empty_month():
    parameters = Parameters()
    manager = Manager(parameters)

    settlement = manager.create_apartment_settlement('apart-polanka', 2025, 1)

    assert settlement is not None
    assert settlement.apartment == 'apart-polanka'
    assert settlement.year == 2025
    assert settlement.month == 1
    assert isinstance(settlement.total_bills_pln, float)
    assert settlement.total_bills_pln == 910.0
    assert settlement.total_rent_pln == 0.0
    assert settlement.total_due_pln == pytest.approx(910.0)


    other = manager.create_apartment_settlement('apart-polanka', 2024, 3)
    assert other is not None
    assert other.apartment == 'apart-polanka'
    assert other.year == 2024
    assert other.month == 3
    assert other.total_bills_pln == 0.0
    assert other.total_rent_pln == 0.0
    assert other.total_due_pln == 0.0

    assert manager.create_apartment_settlement('non-existent-apartment', 2025, 1) is None

    manager.bills.append(Bill(
        amount_pln=100.0,
        date_due='2025-01-20',
        apartment='apart-polanka',
        settlement_year=2025,
        settlement_month=1,
        type='water'
    ))

    updated = manager.create_apartment_settlement('apart-polanka', 2025, 1)
    assert updated.total_bills_pln == 1010.0
    assert updated.total_due_pln == pytest.approx(1010.0)
