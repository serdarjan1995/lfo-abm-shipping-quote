from typing_extensions import Annotated

from fastapi import FastAPI, Depends

from models import ShippingRequest, ShippingQuotesSummary, ShippingQuotesDetails, ShippingQuotesResponse
from utils.abm_shipping_request import ABMShippingRequestClient
from utils.helpers import try_parse_float

app = FastAPI(title="ABM Initiative Shipping Quote API", description="based on google spreadsheet",
              openapi_url="/abm/openapi.json", docs_url="/abm/docs", redoc_url="/abm/redoc")

shipping_client = ABMShippingRequestClient()


@app.get("/abm/shipping_quote")
async def shipping_quote(req: Annotated[ShippingRequest, Depends(ShippingRequest)]) -> ShippingQuotesResponse:
    shipping_client.update_fields(**req.model_dump())

    shipping_quotes_summary = get_shipping_quotes_summary()

    shipping_quotes_details = get_shipping_quotes_details()
    return ShippingQuotesResponse(summary=shipping_quotes_summary, details=shipping_quotes_details)


def get_shipping_quotes_details():
    shipping_details_worksheet_values = shipping_client.get_shipping_details()[0]

    origin_state = shipping_details_worksheet_values[0].strip()
    origin_zone = shipping_details_worksheet_values[1].strip()
    origin_zip = shipping_details_worksheet_values[2].strip()
    destination_state = shipping_details_worksheet_values[3].strip()
    destination_zone = shipping_details_worksheet_values[4].strip()
    destination_zip = shipping_details_worksheet_values[5].strip()
    cubes = shipping_details_worksheet_values[6].strip()
    if cubes == "-":
        cubes = "0"
    weight = shipping_details_worksheet_values[7].replace("Lbs", "").strip()
    service_level = shipping_details_worksheet_values[8].strip()
    carrier = shipping_details_worksheet_values[9].strip()
    area_type = shipping_details_worksheet_values[10].strip()
    service_threshold_charges = try_parse_float(safe_get_list_value(shipping_details_worksheet_values, index=11))
    service_white_glove_charges = try_parse_float(safe_get_list_value(shipping_details_worksheet_values, index=12))
    service_doorstep_charges = try_parse_float(safe_get_list_value(shipping_details_worksheet_values, index=13))

    shipping_quotes_details = ShippingQuotesDetails(
        origin_state=origin_state,
        origin_zone=origin_zone,
        origin_zip=origin_zip,
        destination_state=destination_state,
        destination_zone=destination_zone,
        destination_zip=destination_zip,
        cubes=cubes,
        weight=weight,
        service_level=service_level,
        carrier=carrier,
        area_type=area_type,
        service_threshold_charges=service_threshold_charges,
        service_white_glove_charges=service_white_glove_charges,
        service_doorstep_charges=service_doorstep_charges,
    )
    return shipping_quotes_details


def get_shipping_quotes_summary():
    shipping_summary_worksheet_values = shipping_client.get_shipping_summary()

    # cell values
    delivery_surcharge_value = shipping_summary_worksheet_values[0]
    fuel_surcharge_value = shipping_summary_worksheet_values[1]
    remote_charges_value = shipping_summary_worksheet_values[2]
    outsource_charges_value = shipping_summary_worksheet_values[3]
    insurance_value = shipping_summary_worksheet_values[4]
    total_charge_value = shipping_summary_worksheet_values[5]

    # safe access to values
    delivery_surcharge_value = safe_get_list_value(delivery_surcharge_value)
    fuel_surcharge_value = safe_get_list_value(fuel_surcharge_value).replace("$", "")
    remote_charges_value = safe_get_list_value(remote_charges_value).replace("$", "")
    outsource_charges_value = safe_get_list_value(outsource_charges_value).replace("$", "")
    insurance_value = safe_get_list_value(insurance_value).replace("$", "")
    total_charge_value = safe_get_list_value(total_charge_value).replace("$", "")

    # format
    delivery_surcharge = try_parse_float(delivery_surcharge_value)
    fuel_surcharge = try_parse_float(fuel_surcharge_value)
    remote_charges = try_parse_float(remote_charges_value)
    outsource_charges = try_parse_float(outsource_charges_value)
    insurance = try_parse_float(insurance_value)
    total_charge = try_parse_float(total_charge_value)
    shipping_quotes_summary = ShippingQuotesSummary(
        delivery_surcharge=delivery_surcharge,
        fuel_surcharge=fuel_surcharge,
        remote_charges=remote_charges,
        outsource_charges=outsource_charges,
        insurance=insurance,
        total_charge=total_charge,
    )
    return shipping_quotes_summary


def safe_get_list_value(list_value, index=0):
    return list_value[index] if list_value and len(list_value) > index else "0"
