import json
from urllib.request import urlopen
import pandas as pd

from functions import calc_expected_value,calc_implied_probability,calc_stake_size,convert_american_to_decimal,convert_decimal_to_american

template_url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey=a06923bffa794007036e956d4a22e3cb&oddsFormat=american&bookmakers=bovada,fliff,betonlineag&markets=spreads,totals"

response = urlopen(template_url)
data_json = json.loads(response.read())

df = pd.json_normalize(
    data=data_json,
    record_path=["bookmakers", "markets", "outcomes"],
    meta=[
        "id",
        "sport_key",
        "sport_title",
        "commence_time",
        "home_team",
        "away_team",  # Keep top-level fields
        ["bookmakers", "key"],
        ["bookmakers", "title"],
        ["bookmakers", "last_update"],
        ["bookmakers","markets", "key"],
    ],
)

# Ensure "point" column is numeric
df['point'] = pd.to_numeric(df['point'], errors='coerce')

# Apply absolute value to the "point" column before grouping
df['abs_point'] = df['point'].abs()

groups = df.groupby(["id", "bookmakers.markets.key", "abs_point"])

for group_name, group in groups:
    if group_name[1]=="spreads":
        if len(group) ==2 :
            valid_points = group.iloc[0]["point"] == -group.iloc[1]["point"]
            price_1 = convert_american_to_decimal(group.iloc[0]["price"])
            price_2 = convert_american_to_decimal(group.iloc[1]["price"])
            ev = calc_expected_value(price_1,price_2)
            if valid_points and ev > 0:
                print("found")
    else:
        print("none")
        # print(group_name)

