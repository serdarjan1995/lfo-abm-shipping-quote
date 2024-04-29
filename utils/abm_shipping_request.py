from utils.gspread_client import GspreadClient


class ABMShippingRequestClient(GspreadClient):

    SPREADSHEET_NAME = "Metro Calculater 2024 - ABM"
    WORKSHEET_NAME = "Calculator"

    PICKUP_ZIP_CELL = "C6"
    DELIVERY_ZIP_CELL = "C7"
    SERVICE_LEVEL_CELL = "C8"
    MAX_WEIGHT_CELL = "C9"
    TOTAL_CU_FT_CELL = "C10"

    DELIVERY_SURCHARGE_CELL = "C13"
    FUEL_SURCHARGE_CELL = "C14"
    REMOTE_CHARGES_CELL = "C15"
    OUTSOURCE_CHARGES_CELL = "C16"
    INSURANCE_CELL = "C17"
    TOTAL_CHARGES_CELL = "C18"

    CALL_FOR_QUOTE = "Call for quote"

    DETAILS_CELL_RANGE = "F2:T2"

    def __init__(self):
        super().__init__()
        self.open_spreadsheet(self.SPREADSHEET_NAME)
        self.worksheet = self.get_worksheet(self.WORKSHEET_NAME)

    def set_pickup_zip(self, value):
        self.worksheet.update(self.PICKUP_ZIP_CELL, value)

    def set_delivery_zip(self, value):
        self.worksheet.update(self.DELIVERY_ZIP_CELL, value)

    def set_service_level(self, value):
        self.worksheet.update(self.SERVICE_LEVEL_CELL, value)

    def set_max_weight(self, value):
        self.worksheet.update(self.SERVICE_LEVEL_CELL, value)

    def set_total_cu_ft(self, value):
        self.worksheet.update(self.TOTAL_CU_FT_CELL, value)

    def update_fields(self, pickup_zip: int, delivery_zip: int, service_level: str, total_cu_ft: float, max_weight: int):
        self.worksheet.update(
            [[pickup_zip], [delivery_zip], [service_level], [total_cu_ft], [max_weight]],
            f'{self.PICKUP_ZIP_CELL}:{self.TOTAL_CU_FT_CELL}',
        )

    def get_shipping_details(self):
        return self.worksheet.get(self.DETAILS_CELL_RANGE)

    def get_shipping_summary(self):
        return self.worksheet.get(f"{self.DELIVERY_SURCHARGE_CELL}:{self.TOTAL_CHARGES_CELL}")



