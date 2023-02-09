"""Test sendafd.apiclient module"""

import pytest
import apiclient
from unittest.mock import Mock

import requests


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if args[0] == 'https://api.weather.gov/products/types/afd/locations/err':
                raise requests.HTTPError
            else:
                pass

    # response for testing product endpoint returning 500 error
    if args[0] == 'https://api.weather.gov/products/types/afd/locations/err':
        return MockResponse({
            "type": "urn:noaa:nws:api:UnexpectedProblem",
            "title": "Unexpected Problem",
            "status": 500,
            "detail": "An unexpected problem has occurred.",
            "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
            "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
            "additionalProp1": {}
        }, 500)
    # response for location list
    elif args[0] == "https://api.weather.gov/products/types/afd/locations":
        return MockResponse({
            "@context": [],
            "locations": {
                "ABQ": "Albuquerque, NM",
                "ABR": "Aberdeen, SD",
                "AFC": "Anchorage, AK",
                "AFG": "Fairbanks, AK",
                "AJK": "Juneau, AK",
                "AKQ": "Wakefield, VA",
                "ALY": "Albany, NY",
                "AMA": "Amarillo, TX",
                "APX": "Gaylord, MI",
                "ARX": "La Crosse, WI",
                "BGM": "Binghamton, NY",
                "BIS": "Bismarck, ND",
                "BMX": "NWS Birmingham, Alabama",
                "BOI": "Boise, ID",
                "BOU": "Denver/Boulder, CO",
                "BOX": "Boston / Norton, MA",
                "BRO": "Brownsville/Rio Grande Valley, TX",
                "BTV": "Burlington, VT",
                "BUF": "Buffalo, NY",
                "BYZ": "Billings, MT",
                "CAE": "Columbia, SC",
                "CAR": "Caribou, ME",
                "CHS": "Charleston, SC",
                "CLE": "Cleveland, OH",
                "CRP": "Corpus Christi, TX",
                "CTP": "State College, PA",
                "CYS": "Cheyenne, WY",
                "DDC": "Dodge City, KS",
                "DLH": "Duluth, MN",
                "DMX": "Des Moines, IA",
                "DTX": "Detroit/Pontiac, MI",
                "DVN": "Quad Cities, IA/IL",
                "EAX": "Kansas City/Pleasant Hill, MO",
                "EKA": "Eureka, CA",
                "EPZ": "El Paso, TX",
                "ERR": "Fake region for testing API error handling",
                "EWX": "Austin/San Antonio, TX",
                "FFC": "Peachtree City, GA",
                "FGF": "Grand Forks, ND",
                "FGZ": "Flagstaff, AZ",
                "FSD": "Sioux Falls, SD",
                "FWD": "Fort Worth/Dallas, TX",
                "GGW": "Glasgow, MT",
                "GID": "Hastings, NE",
                "GJT": "Grand Junction, CO",
                "GLD": "Goodland, KS",
                "GRB": "Green Bay, WI",
                "GRR": "Grand Rapids, MI",
                "GSP": "Greenville-Spartanburg, SC",
                "GUM": "Tiyan, GU",
                "GYX": "Gray - Portland, ME",
                "HFO": "Honolulu, HI",
                "HGX": "Houston/Galveston, TX",
                "HNX": "San Joaquin Valley, CA",
                "HUN": "Huntsville, AL",
                "ICT": "Wichita, Kansas",
                "ILM": "NWS Wilmington, NC",
                "ILN": "Wilmington, OH",
                "ILX": "Central Illinois",
                "IND": "Indianapolis, IN",
                "IWX": "Northern Indiana",
                "JAN": "Jackson, Mississippi",
                "JAX": "Jacksonville, FL",
                "JKL": "Jackson, KY",
                "KEY": "Key West, FL",
                "LBF": "North Platte, NE",
                "LCH": "Lake Charles, LA",
                "LIX": "New Orleans/Baton Rouge",
                "LKN": "Elko, NV",
                "LMK": "Louisville, KY",
                "LOT": "Chicago, IL",
                "LOX": "Los Angeles, CA",
                "LSX": "St. Louis, MO",
                "LUB": "Lubbock, TX",
                "LWX": "Baltimore/Washington",
                "LZK": "Little Rock, AR",
                "MAF": "Midland/Odessa",
                "MEG": "Memphis, TN",
                "MFL": "Miami - South Florida",
                "MFR": "Medford, OR",
                "MHX": "Newport/Morehead City, NC",
                "MKX": "Milwaukee/Sullivan, WI",
                "MLB": "Melbourne, FL",
                "MOB": "Mobile/Pensacola",
                "MPX": "Twin Cities, MN",
                "MQT": "Marquette, MI",
                "MRX": "Morristown, TN",
                "MSO": "Missoula, MT",
                "MTR": "San Francisco Bay Area, CA",
                "OAX": "Omaha/Valley, NE",
                "OHX": "Nashville, TN",
                "OKX": "New York, NY",
                "OTX": "Spokane, WA",
                "OUN": "Norman, OK",
                "PAH": "Paducah, KY",
                "PBZ": "Pittsburgh, PA",
                "PDT": "Pendleton, OR",
                "PHI": "Philadelphia/Mt Holly",
                "PIH": "Pocatello, ID",
                "PPG": "WSO Pago Pago",
                "PQR": "Portland, OR",
                "PSR": "NWS Phoenix",
                "PUB": "Pueblo, CO",
                "RAH": "Raleigh, NC",
                "REV": "Reno, NV",
                "RIW": "Western and Central Wyoming",
                "RLX": "Charleston, WV",
                "RNK": "Blacksburg, VA",
                "SEW": "Seattle/Tacoma, WA",
                "SGF": "Springfield, MO",
                "SGX": "San Diego, CA",
                "SHV": "Shreveport, LA",
                "SJT": "San Angelo, TX",
                "SJU": "San Juan, PR",
                "SLC": "Salt Lake City, UT",
                "STO": "Sacramento, CA",
                "TAE": "Tallahassee, FL",
                "TBW": "Tampa Bay Area, FL",
                "TFX": "Great Falls, MT",
                "TOP": "Topeka, KS",
                "TSA": "Tulsa, OK",
                "TWC": "NWS Tucson Arizona",
                "UNR": "Rapid City, SD",
                "VEF": "Las Vegas, NV"
            }
        }, 200)
    # response for AFD list for region PSR
    elif args[0] == "https://api.weather.gov/products/types/afd/locations/psr":
        return MockResponse({
            "@context": {
                "@version": "1.1",
                "@vocab": "https://api.weather.gov/ontology#"
            },
            "@graph": [
                {
                    "@id": "https://api.weather.gov/products/1d6cd33d-4017-4dd1-8dce-41d4541de35a",
                    "id": "1d6cd33d-4017-4dd1-8dce-41d4541de35a",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-09T12:29:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/ec87c703-7085-48a7-b36b-db0ff3fc0200",
                    "id": "ec87c703-7085-48a7-b36b-db0ff3fc0200",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-09T12:16:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/50a167d7-4de0-48b8-b7e8-ba9c86998c29",
                    "id": "50a167d7-4de0-48b8-b7e8-ba9c86998c29",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-09T10:44:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/0f50cce0-fa68-4a05-8194-456905fb59dc",
                    "id": "0f50cce0-fa68-4a05-8194-456905fb59dc",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-09T05:36:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/5821663a-817a-4e41-a074-cf8dbe507606",
                    "id": "5821663a-817a-4e41-a074-cf8dbe507606",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-08T23:43:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/8c18b6b0-bcb3-47d8-a184-a788c8fd2f10",
                    "id": "8c18b6b0-bcb3-47d8-a184-a788c8fd2f10",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-08T20:15:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/f7d60934-6034-4e8a-b59c-14cf980d8193",
                    "id": "f7d60934-6034-4e8a-b59c-14cf980d8193",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-08T17:58:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/7c8e2c78-4ca8-44b5-ae5a-b0755eb1d798",
                    "id": "7c8e2c78-4ca8-44b5-ae5a-b0755eb1d798",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-08T11:37:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/c739d2f4-3cd4-4c00-bc72-8a6f9af77dee",
                    "id": "c739d2f4-3cd4-4c00-bc72-8a6f9af77dee",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-08T09:49:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/91d0b9f3-b7cc-422e-9a75-0d5ae0c4ca56",
                    "id": "91d0b9f3-b7cc-422e-9a75-0d5ae0c4ca56",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-08T09:43:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/3fcaa7a5-0291-4801-866e-962ed3a8e814",
                    "id": "3fcaa7a5-0291-4801-866e-962ed3a8e814",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-08T05:20:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/e0d05b00-941a-4749-874f-a3a7fbabfdcd",
                    "id": "e0d05b00-941a-4749-874f-a3a7fbabfdcd",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-07T23:47:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/4ac55684-055c-4cd6-8b27-5323f5397fd4",
                    "id": "4ac55684-055c-4cd6-8b27-5323f5397fd4",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-07T20:12:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/b622fe08-0d99-42a9-a3b2-16545e4f5899",
                    "id": "b622fe08-0d99-42a9-a3b2-16545e4f5899",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-07T18:07:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/38be99db-55be-4210-b470-4d44d68e2fec",
                    "id": "38be99db-55be-4210-b470-4d44d68e2fec",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-07T11:24:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/3bbfe4e2-6efa-468f-806f-c88a25a0f937",
                    "id": "3bbfe4e2-6efa-468f-806f-c88a25a0f937",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-07T09:48:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/eb2caa58-3260-4def-8d0e-5b0b426c06dd",
                    "id": "eb2caa58-3260-4def-8d0e-5b0b426c06dd",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-07T06:01:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/82459b38-fdc4-4712-b1b6-5efc5f0786ef",
                    "id": "82459b38-fdc4-4712-b1b6-5efc5f0786ef",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-07T01:06:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/a3a7ee26-c569-4b61-812c-35673ceb6448",
                    "id": "a3a7ee26-c569-4b61-812c-35673ceb6448",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-06T21:21:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/3c4c507f-f29f-49e9-b7d6-3018c3829117",
                    "id": "3c4c507f-f29f-49e9-b7d6-3018c3829117",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-06T18:19:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/5bba39e2-cac2-4b59-9d52-e44fc7d8662d",
                    "id": "5bba39e2-cac2-4b59-9d52-e44fc7d8662d",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-06T12:17:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/af0041af-e988-47fd-ac2b-8529b90ceb84",
                    "id": "af0041af-e988-47fd-ac2b-8529b90ceb84",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-06T10:06:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/4cd03b62-f6a8-4275-ba1b-a80f1dd5b621",
                    "id": "4cd03b62-f6a8-4275-ba1b-a80f1dd5b621",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-06T05:55:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/d9f0b279-b74f-4112-a8e4-5f25303f4533",
                    "id": "d9f0b279-b74f-4112-a8e4-5f25303f4533",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-06T00:43:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/b62c7eed-298f-4836-800a-2a725e69b3ee",
                    "id": "b62c7eed-298f-4836-800a-2a725e69b3ee",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-05T21:17:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/683c7a66-16bc-4456-8c7e-5c757e92faa7",
                    "id": "683c7a66-16bc-4456-8c7e-5c757e92faa7",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-05T18:36:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/47713f21-26fc-4adf-9aab-add701516f28",
                    "id": "47713f21-26fc-4adf-9aab-add701516f28",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-05T18:15:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/eb84aa76-e45f-4c5c-a18a-8e7d3e36eb44",
                    "id": "eb84aa76-e45f-4c5c-a18a-8e7d3e36eb44",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-05T11:43:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/7e9a8dcb-83db-4fc0-bb64-85953ef50e63",
                    "id": "7e9a8dcb-83db-4fc0-bb64-85953ef50e63",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-05T10:14:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/6073fa8c-db7b-4758-bf6d-baa3710daf95",
                    "id": "6073fa8c-db7b-4758-bf6d-baa3710daf95",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-05T05:40:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/772f71e8-52ea-497d-9ddc-8e2b510be61f",
                    "id": "772f71e8-52ea-497d-9ddc-8e2b510be61f",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-04T23:51:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/bc21937f-1991-48f9-9050-11d8f9e3600f",
                    "id": "bc21937f-1991-48f9-9050-11d8f9e3600f",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-04T21:01:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/dc0175cf-b608-42f1-a668-f73e745073f7",
                    "id": "dc0175cf-b608-42f1-a668-f73e745073f7",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-04T17:24:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/f0ecff5b-be74-4831-bf4e-a374e636d2fb",
                    "id": "f0ecff5b-be74-4831-bf4e-a374e636d2fb",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-04T11:59:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/5e4950a1-1de7-4d3e-a6f4-ddc9c4b1a0b7",
                    "id": "5e4950a1-1de7-4d3e-a6f4-ddc9c4b1a0b7",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-04T10:28:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/b9fb81ba-a93a-4028-a610-3dfadcf20087",
                    "id": "b9fb81ba-a93a-4028-a610-3dfadcf20087",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-04T05:29:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/40ed0fea-eda1-4058-9bae-b3066bb39f31",
                    "id": "40ed0fea-eda1-4058-9bae-b3066bb39f31",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-03T23:25:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/d3947111-a777-4b99-b469-d9ba359c2702",
                    "id": "d3947111-a777-4b99-b469-d9ba359c2702",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-03T21:33:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/095f7fa2-e475-4421-a3f9-b00389efa6d7",
                    "id": "095f7fa2-e475-4421-a3f9-b00389efa6d7",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-03T17:18:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/f67f8d41-ce5b-4e9c-b053-83b5b4b72898",
                    "id": "f67f8d41-ce5b-4e9c-b053-83b5b4b72898",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-03T11:41:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/afd49a01-b5db-46eb-b2d3-c46556112815",
                    "id": "afd49a01-b5db-46eb-b2d3-c46556112815",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-03T10:15:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/b951a496-1f69-4ac4-896c-7735420fd38a",
                    "id": "b951a496-1f69-4ac4-896c-7735420fd38a",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-03T05:44:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/5dd28ec3-e1c6-4c40-88e9-e1ce473da212",
                    "id": "5dd28ec3-e1c6-4c40-88e9-e1ce473da212",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-03T00:53:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/9486d930-2b02-481a-b335-4e7010637f76",
                    "id": "9486d930-2b02-481a-b335-4e7010637f76",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-02T20:39:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                },
                {
                    "@id": "https://api.weather.gov/products/2c9823f4-ce5f-40f2-b827-faf9305475b6",
                    "id": "2c9823f4-ce5f-40f2-b827-faf9305475b6",
                    "wmoCollectiveId": "FXUS65",
                    "issuingOffice": "KPSR",
                    "issuanceTime": "2023-02-02T18:00:00+00:00",
                    "productCode": "AFD",
                    "productName": "Area Forecast Discussion"
                }
            ]
        }, 200

        )
    # response for single AFD product for region PSR
    elif args[0] == "https://api.weather.gov/products/1d6cd33d-4017-4dd1-8dce-41d4541de35a":
        return MockResponse(
            {
                "@context": {
                    "@version": "1.1",
                    "@vocab": "https://api.weather.gov/ontology#"
                },
                "@id": "https://api.weather.gov/products/1d6cd33d-4017-4dd1-8dce-41d4541de35a",
                "id": "1d6cd33d-4017-4dd1-8dce-41d4541de35a",
                "wmoCollectiveId": "FXUS65",
                "issuingOffice": "KPSR",
                "issuanceTime": "2023-02-09T12:29:00+00:00",
                "productCode": "AFD",
                "productName": "Area Forecast Discussion",
                "productText": "\n000\nFXUS65 KPSR 091229\nAFDPSR\n\nArea Forecast Discussion\nNational Weather Service Phoenix AZ\n529 AM MST Thu Feb 9 2023\n\n.UPDATE...\nUpdated Fire Weather discussion.\n\n&&\n\n.SYNOPSIS...\nWith dry weather persisting, temperatures will warm to above normal \nlevels through the end of the week with locally breezy to windy \nconditions. A low pressure system will track through the region \nSunday and Monday resulting in a cooling trend. Moisture with this\nsystem will be extremely limited with precipitation chances \nmainly being confined to the higher terrain areas of Arizona. \n\n&&\n\n.DISCUSSION...\nLatest water vapor imagery and streamline analysis reveal a \ndivergent, but dry northerly flow across the Desert Southwest, \nsituated between a vort max across the southern Rockies and a \nridge in the eastern Pacific. The high amplitude ridge will \nmigrate eastward today across the intermountain West. Reflection \nat the surface will be in the form of an anomalously strong \nsurface high building in behind a cold front that will move \nthrough this morning. Consequently, the low-level pressure \ngradient will be rather tight, resulting in windy conditions, \nparticularly across the foothills and higher terrain east of \nPhoenix this morning, where the HREF suggests a 50-80 percent \nchance localized gusts could reach 40 mph. Widespread breeziness \nis expected to develop later in the morning across the lower \ndeserts with the potential for gusts up to 30 mph. In addition to \nthe breezy/windy conditions, much drier air will mix to the \nsurface and the NBM indicates dewpoints could reach the single \ndigits by this afternoon.\n\nCold air pooling across the higher terrain will reinvigorate the \nsurface high tonight, which will translate into another period of \nwindy conditions across the higher terrain and a general \nbreeziness across the lower deserts. With the ridge sliding \nfurther eastward, the flow will also become more easterly and the \nstrongest winds will shift further south into southern Arizona. \nHowever, the latest ECMWF ensemble indicates gusts will likely \nstill reach 25-30 mph as far north as Phoenix during the late \nmorning and afternoon. The flow will also be strong enough to \npromote areas of blowing dust, particularly across northern Pinal \nand southern Maricopa Counties. Meanwhile, a return to above \nnormal temperatures is anticipated with highs in the lower 70s.\n\nA continued warming trend is likely Saturday as a southwesterly \nflow develops between a ridge to our east and a deepening low \npressure system across the California Coast. This will help to \nboost temperatures a few more degrees into the mid 70s, though \nabundant high clouds will somewhat temper the effects of the sun.\n\nThe California low pressure system is generally expected to move \nsoutheastward towards Rocky Point Sunday, though there is still \nconsiderable uncertainty with regard to the exact position and \nspeed of the low. A slower approach would translate into a \nslightly warmer day Sunday with highs again reaching the lower 70s\nacross the Phoenix area, while conditions would be considerably \ncooler if the low moves faster and further east. Limited moisture \ntransport will relegate the highest rain chances to the higher \nterrain east of Phoenix Sunday night and Monday, however PoPs \nonly peak at 40 percent. One model cluster depicting a stronger \nlow generates slightly more QPF, though only a few tenths of an \ninch are expected with this scenario across the higher terrain. \nAcross the lower deserts including Phoenix, a few hundredths of an\ninch are possible.\n\n&&\n\n.PREVIOUS DISCUSSION...\nAs the upper vorticity center swings across northern Sonora Monday, \nmean troughing will become established across the intermountain west \nand central Conus during the midweek period. Ensemble spread grows \nrather substantially with potential outcomes ranging from an \nanomalous cold core digging into northern AZ to shortwave energy \nbeing pulled well downstream into the central Conus before \nintensifying. Ensemble distribution appears rather equal yielding \nlow forecast confidence towards the end of this forecast period. \n\n&&\n\n.AVIATION...Updated at 1216Z. \n\nSouth-Central AZ including KPHX, KIWA, KSDL, KDVT, KGYR, KGEU: \n\nWinds in the lower troposphere and at the surface will strengthen\nthis morning leading to northeasterly breeziness (gusts 20-25kts)\nat the surface after the morning inversion dissipates between \n17Z-18Z. Tonight, winds in the lower levels above the surface \nstrengthen while the surface winds weaken. After about 06Z, some \nTAF sites including KPHX are anticipated to have LLWS conditions \ndue to light and variable surface winds contrasted with \nnortheasterly winds to 30kts at 2kft AGL. Other TAF sites are \nanticipated to have less of a contrast due to more distinct \nnortheasterly surface winds and/or less strong winds in the lower \nlevels above the surface. As for sky cover, only minor passing \ncirrus at most. \n\nSoutheast California/Southwest Arizona including KIPL and KBLH: \n\nWinds in the lower troposphere and at the surface will strengthen\nthis morning leading to northerly breeziness (gusts 20-25kts) at \nthe surface after the morning inversion dissipates between \n17Z-18Z. At KBLH, between about 15Z-18Z, anticipate sufficient\ncontrast between light surface winds and stronger winds in the\nlower levels above the surface to cause LLWS conditions. That will\ndissipate when surface winds strengthen. As for sky cover, only\nminor passing cirrus at most. \n\n&&\n \n.FIRE WEATHER... \nStrong high pressure will build across the Desert Southwest\nthrough Friday, resulting in a relatively tight pressure gradient\nalong with periods of breezy to windy conditions. Low RHs \ngenerally below 15 percent will also be prevalent. Some spots may \nreach critical RH and wind thresholds today across portions of \nsouthern Gila County. The threat will shift a bit further south \nFriday, affecting portions of Pinal, southern Maricopa and Yuma \nCounties. However, overall fire danger remains low, given the\nrelatively moist fuels.\n\nLingering breeziness is anticipated Saturday, though relative \nhumidities will climb steadily through the weekend ahead of a low \npressure system. A few showers will be possible mainly Sunday \nnight and Monday as the system moves through the Desert Southwest,\nhowever, the highest rain amounts will be relegated to the higher\nterrain east of Phoenix and will generally amount to less than a \ntenth of an inch. Another period of windy conditions will be \npossible Tuesday/Wednesday as a stronger low pressure system moves\nthrough northern Arizona.\n\n&&\n\n.PSR WATCHES/WARNINGS/ADVISORIES...\nAZ...None.\nCA...None.\n&&\n\n$$\n\nDISCUSSION...Hirsch\nPREVIOUS DISCUSSION...18\nAVIATION...AJ\nFIRE WEATHER...Hirsch\n"
            }, 200
        )
    return MockResponse(None, 404)


def mocked_requests_get_500(*args, **kwargs):
    """Mock for requests.get that always returns a 500 error code and associated API response"""

    class MockResponse:
        def __init__(self):
            self.json_data = {
                "type": "urn:noaa:nws:api:UnexpectedProblem",
                "title": "Unexpected Problem",
                "status": 500,
                "detail": "An unexpected problem has occurred.",
                "instance": "urn:noaa:nws:api:request:493c3a1d-f87e-407f-ae2c-24483f5aab63",
                "correlationId": "493c3a1d-f87e-407f-ae2c-24483f5aab63",
                "additionalProp1": {}
            }
            self.status_code = 500

        def json(self):
            return self.json_data

        def raise_for_status(self):
            raise requests.HTTPError

    return MockResponse()


def test_print_region_codes(capsys):
    apiclient.print_region_codes({"ABQ": "Albuquerque, NM", "ABR": "Aberdeen, SD"})
    captured = capsys.readouterr()
    assert "ABQ Albuquerque, NM\nABR Aberdeen, SD" in captured.out


def test_500_afd_response(monkeypatch, caplog):
    """Test API returning 500 when fetching list of AFD products"""
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    response = apiclient.fetch_afd("ERR")
    assert response == {'response': None, 'error': "HTTP error fetching list of AFD products"}
    assert "HTTP error fetching list of AFD products" in caplog.text


def test_500_response(monkeypatch, caplog):
    """Test API returning 500 on any request"""
    requests_mock = Mock(side_effect=mocked_requests_get_500)
    monkeypatch.setattr('requests.get', requests_mock)
    response = apiclient.fetch_afd("PSR")
    assert response == {'response': None, 'error': "HTTP error fetching list of region codes"}
    assert "HTTP error fetching list of region codes" in caplog.text


def test_psr_response(monkeypatch):
    """Test fetching AFD for PSR region, without monitoring cache"""
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    api_response = apiclient.fetch_afd("PSR")
    assert api_response['error'] is None
    assert api_response['response'] is not None
    assert api_response['response']['id'] == "1d6cd33d-4017-4dd1-8dce-41d4541de35a"
    assert api_response['response']['productCode'] == "AFD"
    assert api_response['response']['productName'] == "Area Forecast Discussion"
    assert "\n000\nFXUS65 KPSR 091229\nAFDPSR\n\nArea Forecast Discussion\nNational Weather " \
           "Service Phoenix AZ\n529 AM MST Thu Feb 9 2023\n\n" in api_response['response']['productText']
