from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    



    def get_apartment_costs(self, apartment_key: str, year: int = None, month: int = None) -> float:
        if apartment_key not in self.apartments:
            return None
        total_cost = 0.0
        for bill in self.bills:
            if bill.apartment == apartment_key and (year is None or bill.settlement_year == year) and (month is None or bill.settlement_month == month):
                total_cost += bill.amount_pln       
        return total_cost
    
    def create_apartment_settlement(self, apartment_key: str, year: int, month: int) -> ApartmentSettlement | None:
        """Create ApartmentSettlement for given apartment/year/month.

        - Returns None if apartment not found.
        - total_rent_pln is left as 0.0 (tenant settlements handled later).
        - total_bills_pln is sum of bills for apartment and month/year.
        - total_due_pln is rent + bills.
        """
        if apartment_key not in self.apartments:
            return None

        total_bills = 0.0
        for bill in self.bills:
            if (
                bill.apartment == apartment_key
                and bill.settlement_year == year
                and bill.settlement_month == month
            ):
                total_bills += float(bill.amount_pln)

        total_rent = 0.0
        total_due = total_rent + total_bills

        return ApartmentSettlement(
            apartment=apartment_key,
            month=month,
            year=year,
            total_rent_pln=float(total_rent),
            total_bills_pln=float(total_bills),
            total_due_pln=float(total_due),
        )
    