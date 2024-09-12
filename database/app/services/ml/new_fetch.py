import datetime
from urllib import request
import json
from urllib.request import urlopen
import pandas as pd


def fetch_lines(data_json):
    normalized_json = pd.json_normalize(
        data=data_json.get("data"),
        record_path=["bookmakers", "markets", "outcomes"],
    )
    return normalized_json


def main():
    start_date = datetime.date(2023, 8, 1)
    end_date = datetime.date(2024, 5, 30)

    current_date = start_date
    while current_date <= end_date:

        if current_date.day in [5, 15, 25]:
            print(f"Fetching data for {current_date}")
            api_key = "a06923bffa794007036e956d4a22e3cb"
            bookmakers = "fliff,bovada,betonlineag,draftkings,fanduel,espnbet,betmgm"
            template_url = f"https://api.the-odds-api.com/v4/historical/sports/soccer_epl/odds/?apiKey={api_key}&markets=h2h&date={current_date}T12:05:00Z&regions=us&bookmakers={bookmakers}"

            try:
                response = urlopen(template_url)
                data_json = json.loads(response.read())
                df_lines = fetch_lines(data_json=data_json)
                print(df_lines.head())
            except Exception as e:
                print(f"error fetching data for {current_date}: {e}")
            break

        current_date += datetime.timedelta(days=1)


if __name__ == "__main__":
    main()
