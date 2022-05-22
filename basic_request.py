import os
import datetime

import requests
import json
from typing import Dict, Any
from dotenv import load_dotenv

from utils import Operations, save_to_json

API_URL = "https://api.untappd.com/v4/user/{}/{}{}"


class Untappd:
    
    def __init__(self, username: str = ''):
        load_dotenv()
        self.username = username
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.main_url = f"{self.username}?client_id={self.client_id}&client_secret={self.client_secret}"
        self.next_page_url = f"&client_id={self.client_id}&client_secret={self.client_secret}"

    def send_and_parse_request(
            self, operation: str = '', additional_parameters: str = '', next_page_url: str = '') -> Dict[str, Any]:
        if next_page_url != '':
            request = requests.get(next_page_url)
        else:
            request = requests.get(API_URL.format(operation, self.main_url, additional_parameters))
        response = json.loads(request.text)
        return response.get("response", {})

    def get_checkins(self) -> Dict[str, Any]:
        # get data
        data = self.send_and_parse_request(Operations.CHECKINS.name.lower())

        # parse checkins
        checkins_data = data.get("checkins", {})
        checkins: Dict[str, Any] = {
            "number_of_checkins": checkins_data.get("count"),
            "checkins_value": checkins_data.get("items")
        }
        return checkins

    def get_all_beers(self) -> Dict[str, Any]:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        additional_parameters = f"&start_date=2015-01-01&end_data={today}&limit=50"

        beers_data = self.send_and_parse_request(Operations.BEERS.name.lower(), additional_parameters)
        number_of_all_checkins = beers_data.get("total_count", {})
        all_beers = []
        all_beers.extend(beers_data.get("beers", {}).get("items", {}))
        next_page = beers_data.get("pagination", {}).get("next_url")
        while next_page:
            next_page_url = '%s%s' % (next_page, self.next_page_url)
            next_page_data = self.send_and_parse_request(next_page_url=next_page_url)
            all_beers.extend(next_page_data.get("beers").get("items"))
            next_page = next_page_data.get("pagination", {}).get("next_url")

        all_checkins: Dict[str, Any] = {"number_of_checkins": number_of_all_checkins, "beers": all_beers}
        return all_checkins


if __name__ == "__main__":
    untappd_api = Untappd('<REPLACE_ME>')
    print("Getting all beers...")
    all_beers = untappd_api.get_all_beers()
    print("Done!")
    save_to_json("<REPLACE_ME>", all_beers)
    print("File saved!")
    # checkins = untappd_api.get_checkins()
    # print(checkins)
