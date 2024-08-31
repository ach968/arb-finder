import json
from urllib.request import urlopen
import pandas as pd
import functions
from scrape_scores import scrape_scores
import datetime


def export_dataframe_to_csv(dataframe, file_path):
    dataframe.to_csv(file_path, index=False)


# need to make it so that the function only returns the highest EV for each game
def find_arb_opportunities(df):
    opportunities = []

    grouped_df = df.groupby(["id"])

    for group_key, group_df in grouped_df:
        if len(group_df) > 1:
            for i in range(len(group_df)):
                for j in range(i + 1, len(group_df)):

                    # Extract lines and odds
                    line_1 = group_df.iloc[i]
                    line_2 = group_df.iloc[j]
                    odd_1 = line_1["price"]
                    odd_2 = line_2["price"]

                    # Calculate implied probabilities
                    implied_prob_1 = functions.calc_implied_probability(odd_1)
                    implied_prob_2 = functions.calc_implied_probability(odd_2)

                    stakes = functions.calc_stake_size(line_1["price"], line_2["price"])

                    # Calculate outcomes, check if they are profitable
                    outcome_1 = stakes[0] * odd_1
                    outcome_2 = stakes[1] * odd_2

                    # Not betting on the same team
                    name_1 = line_1["name"]
                    name_2 = line_2["name"]

                    # Betting on different bookmakers
                    bookmaker_1 = line_1["bookmaker_key"]
                    bookmaker_2 = line_2["bookmaker_key"]

                    condition_1 = (
                        functions.calc_expected_value(odd1=odd_1, odd2=odd_2) < 1
                    )
                    condition_2 = outcome_1 > 1 and outcome_2 > 1
                    condition_3 = name_1 != name_2
                    condition_4 = bookmaker_1 != bookmaker_2

                    if condition_1 and condition_2 and condition_3 and condition_4:
                        opportunity = {
                            "id": line_1["id"],
                            "bookmaker_1": bookmaker_1,
                            "name_1": name_1,
                            "price_1": line_1["price"],
                            "implied_prob_1": implied_prob_1,
                            "stake_1": stakes[0],
                            "bookmaker_2": bookmaker_2,
                            "name_2": name_2,
                            "price_2": line_2["price"],
                            "implied_prob_2": implied_prob_2,
                            "stake_2": stakes[1],
                            "expected_value": functions.calc_expected_value(
                                odd1=odd_1, odd2=odd_2
                            ),
                            "outcome_1": outcome_1,
                            "outcome_2": outcome_2,
                            "commence_time": line_1["commence_time"],
                        }
                        opportunities.append(opportunity)

    return pd.DataFrame(opportunities)


def pull_historical_data(data_json):

    non_draws = []
    draws = []

    for data in data_json.get("data"):
        identifier = data.get("id")
        sport_key = data.get("sport_key")
        commence_time = data.get("commence_time")
        home_team = data.get("home_team")
        away_team = data.get("away_team")
        sport_title = data.get("sport_title")

        for bookmaker in data.get("bookmakers", []):
            bookmaker_key = bookmaker.get("key")

            for market in bookmaker.get("markets", []):
                market_last_update = market.get("last_update")
                market_title = market.get("key")

                for outcome in market.get("outcomes", []):
                    name = outcome.get("name")
                    price = outcome.get("price")
                    new_row = {
                        "id": identifier,
                        "sport_key": sport_key,
                        "bookmaker_key": bookmaker_key,
                        "market_title": market_title,
                        "name": name,
                        "price": price,
                        "last_update": market_last_update,
                        "commence_time": commence_time,
                        "home_team": home_team,
                        "away_team": away_team,
                        "sport_title": sport_title,
                    }
                    if name == "Draw":
                        draws.append(new_row)
                    else:
                        non_draws.append(new_row)
    return [pd.DataFrame(draws), pd.DataFrame(non_draws)]


def run_test():
    start_date = datetime.date(2023, 8, 1)
    end_date = datetime.date(2024,5, 30)

    arb_data = []
    draws = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.day in [5, 15, 25]:
            print(f"Fetching data for {current_date}")
            template_url = f"https://api.the-odds-api.com/v4/historical/sports/soccer_epl/odds/?apiKey=a06923bffa794007036e956d4a22e3cb&bookmakers=bovada,fliff,betonlineag&markets=h2h&date={current_date}T12:05:00Z&regions=us,us2"
            try:
                response = urlopen(template_url)
                data_json = json.loads(response.read())
                df_list = pull_historical_data(data_json=data_json)
                draws.append(df_list[0])
                arb_data.append(find_arb_opportunities(df_list[1]))
            except Exception as e:
                print(f'error fetching data for {current_date}: {e}')

        current_date += datetime.timedelta(days=1)
    export_dataframe_to_csv(pd.concat(arb_data), "arb_opportunities.csv")
    export_dataframe_to_csv(pd.concat(draws), "draws.csv")


if __name__ == "__main__":
    run_test()
