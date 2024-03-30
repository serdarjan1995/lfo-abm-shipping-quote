from typing_extensions import Annotated

from fastapi import FastAPI, Depends

from models import ShippingRequest, ShippingQuotesSummary, ShippingQuotesDetails, ShippingQuotesResponse
from utils.abm_shipping_request import ABMShippingRequestClient
from utils.helpers import try_parse_float

app = FastAPI(title="ABM Initiative Shipping Quote API", description="based on google spreadsheet")


shipping_client = ABMShippingRequestClient()


@app.get("/abm/shipping_quote")
async def shipping_quote(req: Annotated[ShippingRequest, Depends(ShippingRequest)]) -> ShippingQuotesResponse:
    shipping_client.update_fields(**req.model_dump())

    shipping_quotes_summary = get_shipping_quotes_summary()

    shipping_quotes_details = get_shipping_quotes_details()
    return {"summary": shipping_quotes_summary, "details": shipping_quotes_details}


def get_shipping_quotes_details():
    shipping_details_worksheet_values = shipping_client.get_shipping_details()[0]
    shipping_quotes_details = ShippingQuotesDetails(
        origin_state=shipping_details_worksheet_values[0].strip(),
        origin_zone=shipping_details_worksheet_values[1].strip(),
        origin_zip=shipping_details_worksheet_values[2].strip(),
        destination_state=shipping_details_worksheet_values[3].strip(),
        destination_zone=shipping_details_worksheet_values[4].strip(),
        destination_zip=shipping_details_worksheet_values[5].strip(),
        cubes=shipping_details_worksheet_values[6].strip(),
        weight=shipping_details_worksheet_values[7].replace("Lbs", '').strip(),
        service_level=shipping_details_worksheet_values[8].strip(),
        carrier=shipping_details_worksheet_values[9].strip(),
        area_type=shipping_details_worksheet_values[10].strip(),
        service_threshold_charges=try_parse_float(shipping_details_worksheet_values[11]),
        service_white_glove_charges=try_parse_float(shipping_details_worksheet_values[12]),
        service_doorstep_charges=try_parse_float(shipping_details_worksheet_values[13]),
    )
    return shipping_quotes_details


def get_shipping_quotes_summary():
    shipping_summary_worksheet_values = shipping_client.get_shipping_summary()

    delivery_surcharge = try_parse_float(shipping_summary_worksheet_values[0][0])
    fuel_surcharge = try_parse_float(shipping_summary_worksheet_values[1][0].replace("$", ''))
    remote_charges = try_parse_float(shipping_summary_worksheet_values[2][0].replace("$", ''))
    outsource_charges = try_parse_float(shipping_summary_worksheet_values[3][0].replace("$", ''))
    total_charge = try_parse_float(shipping_summary_worksheet_values[4][0].replace("$", ''))
    shipping_quotes_summary = ShippingQuotesSummary(
        delivery_surcharge=delivery_surcharge,
        fuel_surcharge=fuel_surcharge,
        remote_charges=remote_charges,
        outsource_charges=outsource_charges,
        total_charge=total_charge,
    )
    return shipping_quotes_summary
