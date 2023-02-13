"""Test sendafd.apiclient module"""
import json

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
                "ERR": "Fake region for testing API error handling, does not exist in real NWS API",
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
        with open("psr_afd_list_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for AFD list for region TOP
    elif args[0] == "https://api.weather.gov/products/types/afd/locations/top":
        with open("top_afd_list_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for AFD list for region LOX
    elif args[0] == "https://api.weather.gov/products/types/afd/locations/lox":
        with open("lox_afd_list_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for AFD list for region OKX
    elif args[0] == "https://api.weather.gov/products/types/afd/locations/okx":
        with open("okx_afd_list_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for single AFD product for region PSR
    elif args[0] == "https://api.weather.gov/products/1d6cd33d-4017-4dd1-8dce-41d4541de35a":
        with open("psr_afd_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for single AFD product for region TOP
    elif args[0] == "https://api.weather.gov/products/1f29f93c-583b-4144-ae22-8624a5e56504":
        with open("top_afd_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for single AFD product for region LOX
    elif args[0] == "https://api.weather.gov/products/a922a688-acb5-4bb8-8a22-55c6a107b61d":
        with open("lox_afd_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
    # response for single AFD product for region OKX
    elif args[0] == "https://api.weather.gov/products/6893e2af-17ef-471a-b7bc-4a74a8af0374":
        with open("okx_afd_response.json", 'r', encoding='utf-8') as f:
            json_response = json.load(f)
        return MockResponse(json_response, 200)
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

def test_psr_afd_response(monkeypatch):
    """Test fetching an example AFD for PSR region, without monitoring cache"""
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    api_response = apiclient.fetch_afd("PSR")
    assert api_response['error'] is None
    assert api_response['response'] is not None
    assert api_response['response']['id'] == "1d6cd33d-4017-4dd1-8dce-41d4541de35a"
    assert api_response['response']['productCode'] == "AFD"
    assert api_response['response']['productName'] == "Area Forecast Discussion"
    assert "\n000\nFXUS65 KPSR 091229\nAFDPSR\n\nArea Forecast Discussion\nNational Weather " \
           "Service Phoenix AZ\n529 AM MST Thu Feb 9 2023\n\n" \
           in api_response['response']['productText']

def test_top_afd_response(monkeypatch):
    """Test fetching an example AFD for TOP region, without monitoring cache"""
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    api_response = apiclient.fetch_afd("TOP")
    assert api_response['error'] is None
    assert api_response['response'] is not None
    assert api_response['response']['id'] == "1f29f93c-583b-4144-ae22-8624a5e56504"
    assert api_response['response']['productCode'] == "AFD"
    assert api_response['response']['productName'] == "Area Forecast Discussion"
    assert "\n000\nFXUS63 KTOP 122335\nAFDTOP\n\nArea Forecast Discussion\nNational Weather " \
           "Service Topeka KS\n535 PM CST Sun Feb 12 2023" \
           in api_response['response']['productText']

def test_lox_afd_response(monkeypatch):
    """Test fetching an example AFD for LOX region, without monitoring cache"""
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    api_response = apiclient.fetch_afd("LOX")
    assert api_response['error'] is None
    assert api_response['response'] is not None
    assert api_response['response']['id'] == "a922a688-acb5-4bb8-8a22-55c6a107b61d"
    assert api_response['response']['productCode'] == "AFD"
    assert api_response['response']['productName'] == "Area Forecast Discussion"
    assert "\n000\nFXUS66 KLOX 130046\nAFDLOX\n\nArea Forecast Discussion...UPDATED\nNational " \
           "Weather Service Los Angeles/Oxnard CA \n446 PM PST Sun Feb 12 2023" \
           in api_response['response']['productText']

def test_okx_afd_response(monkeypatch):
    """Test fetching an example AFD for OKX region, without monitoring cache"""
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    api_response = apiclient.fetch_afd("OKX")
    assert api_response['error'] is None
    assert api_response['response'] is not None
    assert api_response['response']['id'] == "6893e2af-17ef-471a-b7bc-4a74a8af0374"
    assert api_response['response']['productCode'] == "AFD"
    assert api_response['response']['productName'] == "Area Forecast Discussion"
    assert "\n000\nFXUS61 KOKX 130251\nAFDOKX\n\nArea Forecast Discussion\nNational Weather " \
           "Service New York NY\n951 PM EST Sun Feb 12 2023" \
           in api_response['response']['productText']

def test_psr_afd_parsing(monkeypatch):
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    api_response = apiclient.fetch_afd("PSR")
    parsed_afd = apiclient.AreaForecastDiscussion(raw_afd=api_response['response'])
    # test time parsing
    assert parsed_afd.issuance_time.day == 9
    assert parsed_afd.issuance_time.month == 2
    assert parsed_afd.issuance_time.year == 2023
    assert parsed_afd.issuance_time.hour == 12
    assert parsed_afd.issuance_time.minute == 29
    # test id
    assert parsed_afd.product_id == '1d6cd33d-4017-4dd1-8dce-41d4541de35a'
    assert parsed_afd.issuing_office == 'KPSR'
    # test section parsing
    assert len(parsed_afd.sections) == 8
    assert parsed_afd.sections[0].name == 'header'
    assert parsed_afd.sections[0].body == parsed_afd.header
    assert parsed_afd.header == '000\nFXUS65 KPSR 091229\nAFDPSR\n\nArea Forecast Discussion\nNational Weather Service Phoenix AZ\n529 AM MST Thu Feb 9 2023\n\n.UPDATE...\nUpdated Fire Weather discussion.'
    assert parsed_afd.sections[1].name == 'Synopsis'
    assert parsed_afd.sections[1].body == parsed_afd.synopsis
    assert parsed_afd.synopsis == 'With dry weather persisting, temperatures will warm to above normal \nlevels through the end of the week with locally breezy to windy \nconditions. A low pressure system will track through the region \nSunday and Monday resulting in a cooling trend. Moisture with this\nsystem will be extremely limited with precipitation chances \nmainly being confined to the higher terrain areas of Arizona.'
    assert parsed_afd.sections[2].name == 'Discussion'
    assert parsed_afd.sections[2].body == parsed_afd.discussion
    assert parsed_afd.discussion == 'Latest water vapor imagery and streamline analysis reveal a \ndivergent, but dry northerly flow across the Desert Southwest, \nsituated between a vort max across the southern Rockies and a \nridge in the eastern Pacific. The high amplitude ridge will \nmigrate eastward today across the intermountain West. Reflection \nat the surface will be in the form of an anomalously strong \nsurface high building in behind a cold front that will move \nthrough this morning. Consequently, the low-level pressure \ngradient will be rather tight, resulting in windy conditions, \nparticularly across the foothills and higher terrain east of \nPhoenix this morning, where the HREF suggests a 50-80 percent \nchance localized gusts could reach 40 mph. Widespread breeziness \nis expected to develop later in the morning across the lower \ndeserts with the potential for gusts up to 30 mph. In addition to \nthe breezy/windy conditions, much drier air will mix to the \nsurface and the NBM indicates dewpoints could reach the single \ndigits by this afternoon.\n\nCold air pooling across the higher terrain will reinvigorate the \nsurface high tonight, which will translate into another period of \nwindy conditions across the higher terrain and a general \nbreeziness across the lower deserts. With the ridge sliding \nfurther eastward, the flow will also become more easterly and the \nstrongest winds will shift further south into southern Arizona. \nHowever, the latest ECMWF ensemble indicates gusts will likely \nstill reach 25-30 mph as far north as Phoenix during the late \nmorning and afternoon. The flow will also be strong enough to \npromote areas of blowing dust, particularly across northern Pinal \nand southern Maricopa Counties. Meanwhile, a return to above \nnormal temperatures is anticipated with highs in the lower 70s.\n\nA continued warming trend is likely Saturday as a southwesterly \nflow develops between a ridge to our east and a deepening low \npressure system across the California Coast. This will help to \nboost temperatures a few more degrees into the mid 70s, though \nabundant high clouds will somewhat temper the effects of the sun.\n\nThe California low pressure system is generally expected to move \nsoutheastward towards Rocky Point Sunday, though there is still \nconsiderable uncertainty with regard to the exact position and \nspeed of the low. A slower approach would translate into a \nslightly warmer day Sunday with highs again reaching the lower 70s\nacross the Phoenix area, while conditions would be considerably \ncooler if the low moves faster and further east. Limited moisture \ntransport will relegate the highest rain chances to the higher \nterrain east of Phoenix Sunday night and Monday, however PoPs \nonly peak at 40 percent. One model cluster depicting a stronger \nlow generates slightly more QPF, though only a few tenths of an \ninch are expected with this scenario across the higher terrain. \nAcross the lower deserts including Phoenix, a few hundredths of an\ninch are possible.'
    assert parsed_afd.sections[3].name == 'Previous Discussion'
    assert parsed_afd.sections[3].body == parsed_afd.previous_discussion
    assert parsed_afd.previous_discussion == 'As the upper vorticity center swings across northern Sonora Monday, \nmean troughing will become established across the intermountain west \nand central Conus during the midweek period. Ensemble spread grows \nrather substantially with potential outcomes ranging from an \nanomalous cold core digging into northern AZ to shortwave energy \nbeing pulled well downstream into the central Conus before \nintensifying. Ensemble distribution appears rather equal yielding \nlow forecast confidence towards the end of this forecast period.'
    assert parsed_afd.sections[4].name == 'Aviation'
    assert parsed_afd.sections[4].body == parsed_afd.aviation
    assert parsed_afd.aviation == 'Updated at 1216Z. \n\nSouth-Central AZ including KPHX, KIWA, KSDL, KDVT, KGYR, KGEU: \n\nWinds in the lower troposphere and at the surface will strengthen\nthis morning leading to northeasterly breeziness (gusts 20-25kts)\nat the surface after the morning inversion dissipates between \n17Z-18Z. Tonight, winds in the lower levels above the surface \nstrengthen while the surface winds weaken. After about 06Z, some \nTAF sites including KPHX are anticipated to have LLWS conditions \ndue to light and variable surface winds contrasted with \nnortheasterly winds to 30kts at 2kft AGL. Other TAF sites are \nanticipated to have less of a contrast due to more distinct \nnortheasterly surface winds and/or less strong winds in the lower \nlevels above the surface. As for sky cover, only minor passing \ncirrus at most. \n\nSoutheast California/Southwest Arizona including KIPL and KBLH: \n\nWinds in the lower troposphere and at the surface will strengthen\nthis morning leading to northerly breeziness (gusts 20-25kts) at \nthe surface after the morning inversion dissipates between \n17Z-18Z. At KBLH, between about 15Z-18Z, anticipate sufficient\ncontrast between light surface winds and stronger winds in the\nlower levels above the surface to cause LLWS conditions. That will\ndissipate when surface winds strengthen. As for sky cover, only\nminor passing cirrus at most.'
    assert parsed_afd.sections[5].name == 'Fire Weather'
    assert parsed_afd.sections[5].body == parsed_afd.fire_weather
    assert parsed_afd.fire_weather == 'Strong high pressure will build across the Desert Southwest\nthrough Friday, resulting in a relatively tight pressure gradient\nalong with periods of breezy to windy conditions. Low RHs \ngenerally below 15 percent will also be prevalent. Some spots may \nreach critical RH and wind thresholds today across portions of \nsouthern Gila County. The threat will shift a bit further south \nFriday, affecting portions of Pinal, southern Maricopa and Yuma \nCounties. However, overall fire danger remains low, given the\nrelatively moist fuels.\n\nLingering breeziness is anticipated Saturday, though relative \nhumidities will climb steadily through the weekend ahead of a low \npressure system. A few showers will be possible mainly Sunday \nnight and Monday as the system moves through the Desert Southwest,\nhowever, the highest rain amounts will be relegated to the higher\nterrain east of Phoenix and will generally amount to less than a \ntenth of an inch. Another period of windy conditions will be \npossible Tuesday/Wednesday as a stronger low pressure system moves\nthrough northern Arizona.'
    assert parsed_afd.sections[6].name == 'Psr Watches/Warnings/Advisories'
    assert parsed_afd.sections[6].body == parsed_afd.psr_watches_warnings_advisories
    assert parsed_afd.psr_watches_warnings_advisories == 'AZ...None.\nCA...None.'
    assert parsed_afd.sections[7].name == 'footer'
    assert parsed_afd.sections[7].body == parsed_afd.footer
    assert parsed_afd.footer == '$$\n\nDISCUSSION...Hirsch\nPREVIOUS DISCUSSION...18\nAVIATION...AJ\nFIRE WEATHER...Hirsch'

def test_top_afd_parsing(monkeypatch):
    requests_mock = Mock(side_effect=mocked_requests_get)
    monkeypatch.setattr('requests.get', requests_mock)
    api_response = apiclient.fetch_afd("TOP")
    parsed_afd = apiclient.AreaForecastDiscussion(raw_afd=api_response['response'])
    # test time parsing
    assert parsed_afd.issuance_time.day == 12
    assert parsed_afd.issuance_time.month == 2
    assert parsed_afd.issuance_time.year == 2023
    assert parsed_afd.issuance_time.hour == 23
    assert parsed_afd.issuance_time.minute == 35
    # test id
    assert parsed_afd.product_id == '1f29f93c-583b-4144-ae22-8624a5e56504'
    assert parsed_afd.issuing_office == 'KTOP'
    # test section parsing
    assert len(parsed_afd.sections) == 5
    assert parsed_afd.sections[0].name == 'header'
    assert parsed_afd.sections[0].body == parsed_afd.header
    assert parsed_afd.header == "\n000\nFXUS63 KTOP 122335\nAFDTOP\n\nArea Forecast Discussion\nNational Weather Service Topeka KS\n535 PM CST Sun Feb 12 2023\n\n...Update to aviation forecast discussion...\n\n"
    assert parsed_afd.sections[1].name == 'Discussion'
    assert parsed_afd.sections[1].body == parsed_afd.discussion
    assert parsed_afd.discussion == "Issued at 215 PM CST Sun Feb 12 2023\n\nKey Messages:\n\n- Another round of much needed rain is expected area wide on Tuesday.\n\n- There remains decent confidence in a potential winter storm\n  impacting portions of central and northeast Kansas Wednesday\n  evening into Thursday.\n\nHigh pressure aloft builds over the southern and central plains this \nafternoon while a weak area of sfc low pressure stretches across the \nsunflower state.  Associated high clouds have provided some effect \non temps, however strong warm advection has won out with gusts in \nupwards of 25 mph. High temps remain on track to reach the upper 50s \nand lower 60s. As the sfc low exits this evening, winds should calm \nand become light from the northwest.  \n\nThe first anomalously strong system, currently rotating just off the \nsouthern CA coastline, will bring much needed rainfall to the region \nafter midnight through Tuesday afternoon.  Guidance continues to be \nin good agreement in the track and location of higher precip \namounts, lending to the definite pops mentioned Tuesday after \nsunrise. EFI and GEFS ensembles continue to indicate high PWAT \nvalues well above the climatological norms at 0.8 to 1 inches. \nOverall precip amounts were not changed with widespread totals from \na half inch to 1 inch. Winds are also of concern Monday night into \nTuesday afternoon with southerly speeds approaching advisory \ncriteria of 20 to 30 mph sustained. These winds remain stout at \naround 25 mph as they shift towards the west Tuesday evening. The \nprimary uncertainty to mention is the amount of mid level \ninstability that develops Tuesday morning and afternoon. Lapse rates \nwould be steep in the vicinity of the cold upper low so still cannot \nrule out a few afternoon thunderstorms.\n\nThe second, possibly more impactful storm system is progged to \narrive Wednesday early evening through Thursday morning. Overall \noperational and ensemble guidance is beginning to trend the track \nof the upper low slightly further south due to a northern stream \ntrough deepening further south across the Great Lakes region. This\nscenario would shift the sfc low towards southern OK and \ntherefore the higher precip amounts further south into central and\nnortheast Kansas. The 0C surface temps would also spread further \nsouth at a faster rate, allowing more snow to fall as oppose to \nrain early Thursday morning. Accumulating snow remains most likely\ntowards north central Kansas, however areas near the I-70 \ncorridor could end up seeing a few inches of snow as well. An \nimpressive pressure gradient is shaping up to be likely area wide \nas northerly winds could gust in excess of 30 mph, resulting in \nblowing snow, reduced visibilities, and hazardous travel. If \nconfidence continues to increase as models mostly remain on track,\na Winter Storm Watch will likely be needed for portions of north \ncentral and northeast Kansas.\n\nAnticipate bitterly cold temps behind the front Thursday and Friday \nmornings with wind chill readings from the single digits to 10 \ndegrees below zero. After highs in the 20s on Thursday, a quick \nwarmup should melt much of the snow with highs back in the 50s by \nSaturday."
    assert parsed_afd.sections[2].name == 'Aviation'
    assert parsed_afd.sections[2].body == parsed_afd.aviation
    assert parsed_afd.discussion == '(For the 00Z TAFS through 00Z Monday evening)\nIssued at 532 PM CST Sun Feb 12 2023\n\nExpect VFR conditions for the next 24 hours. A weak cold front\nwill switch winds to the northwest after 2Z MON, but speeds will\nremain below 10 KTS. Northwest winds will become light and\nvariable after 12Z MON, then become southerly late Monday\nafternoon.'
    assert parsed_afd.sections[3].name == 'Top Watches/Warnings/Advisories'
    assert parsed_afd.sections[3].body == parsed_afd.top_watches_warnings_advisories
    assert parsed_afd.discussion == 'NONE.'
    assert parsed_afd.sections[4].name == 'footer'
    assert parsed_afd.sections[4].body == parsed_afd.footer
    assert parsed_afd.discussion == '$$\n\nDISCUSSION...22\nAVIATION...Gargan'
