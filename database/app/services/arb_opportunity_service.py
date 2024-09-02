import json
from datetime import datetime, timezone
from urllib.request import urlopen
import logging

import pandas as pd
from sqlalchemy.dialects.postgresql import insert

from app.models.arb_opportunity import ArbOpportunity
from app.services.functions import (
    calc_implied_probability,
    calc_expected_value,
    calc_stake_size,
    convert_american_to_decimal,
    convert_decimal_to_american
)
from app.services.no_fly_list import no_fly_list
from database_init import db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def save_arb_opportunity_model(
    api_key, sports, markets_string, time_sent, bookmakers, regions
):
    all_data = []
    processed_sports = 0
    for sport in sports:
        if not no_fly_list.get(sport):
            template_url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={api_key}&markets={markets_string}&regions={regions}&oddsFormat=american"
            try:
                response = urlopen(template_url)
                data_json = json.loads(response.read())
                dfs = generate_lines_df(data_json, time_sent)
                all_data.extend(find_arb_opportunities(dfs))
            except Exception as e:
                logger.error(f"error fetching data for {sport}: {e}")
                continue
            processed_sports += 1

    successful_attempts = 0
    total_attempts = 0
    for data in all_data:
        upsert_stmt = (
            insert(ArbOpportunity)
            .values(data)
            .on_conflict_do_update(
                index_elements=["id"], set_={"time_sent": data["time_sent"]}
            )
        )
        try:
            db.session.execute(upsert_stmt)
            successful_attempts += 1
        except Exception as e:
            db.session.rollback()
            logger.error(f"error inserting data [{data}]: {str(e)}")
            continue
        total_attempts += 1
    db.session.commit()

    return f"{processed_sports} sports processed, {successful_attempts} out of {total_attempts} opportunities successfully found!"


def find_arb_opportunities(dfs):
    try:
        totals_arbs = find_totals_arbs(dfs[1])
    except Exception as e:
        totals_arbs = []
    try:
        two_way_h2h_arbs = find_two_way_h2h_arbs(dfs[0])
    except Exception as e:
        two_way_h2h_arbs = []
    # try:
    #     three_way_h2h_arbs = find_three_way_h2h_arbs(dfs[2])
    # except Exception as e:
    #     three_way_h2h_arbs = []
        
    return totals_arbs + two_way_h2h_arbs


def find_totals_arbs(df):
    arbs_data = []
    grouped_df = df.groupby("identifier")
    for current_id, group in grouped_df:
        if len(group) > 1:
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    line_1_raw = group.iloc[i]
                    line_2_raw = group.iloc[j]

                    odd_1 = convert_american_to_decimal(line_1_raw["price"])
                    odd_2 = convert_american_to_decimal(line_2_raw["price"])

                    expected_value = round(
                        calc_expected_value(odd1=odd_1,odd2=odd_2), 2
                    )

                    condition1 = False
                    if line_1_raw["market_title"] == "spreads" and line_2_raw["market_title"] == "spreads":
                        if line_1_raw["point"] == -line_2_raw["point"]:
                            condition1 = True
                    elif line_1_raw["market_title"] == "totals" and line_2_raw["market_title"] == "totals":
                        if line_1_raw["point"] == line_2_raw["point"]:
                            condition1 = True

                    
                    condition2 = (
                        line_1_raw["name"] != line_2_raw["name"]
                    )
                    condition3 = expected_value > 0
                    
                    stakes = calc_stake_size(
                        odd1=odd_1, odd2=odd_2
                    )

                    if condition1 and condition2 and condition3:
                        arb = {
                            "market": line_1_raw["market_title"],
                            "line_1": {
                                "bookmaker": line_1_raw["bookmaker_key"],
                                "name": line_1_raw["name"],
                                "price": int(line_1_raw["price"]),
                                "implied odd": round(
                                    calc_implied_probability(line_1_raw["price"]), 2
                                ),
                                "stake": round(stakes[0], 2),
                                "point": float(line_1_raw["point"]),
                            },
                            "line_2": {
                                "bookmaker": line_2_raw["bookmaker_key"],
                                "name": line_2_raw["name"],
                                "price": int(line_2_raw["price"]),
                                "implied odd": round(
                                    calc_implied_probability(line_2_raw["price"]), 2
                                ),
                                "stake": round(stakes[1], 2),
                                "point": float(line_2_raw["point"]),
                            },
                            "expected_value": float(expected_value),
                            "commence_time": float(line_1_raw["commence_time"]),
                            "league": line_1_raw["sport_title"],
                            "game_title": (
                                f"{group['home_team'].iloc[0]} (H) @ "
                                f"{group['away_team'].iloc[0]} (A)"
                            ),
                            "last_update": float(line_1_raw["last_update"]),
                            "id": line_1_raw["bookmaker_key"]
                            + line_2_raw["bookmaker_key"]
                            + str(line_1_raw["price"])
                            + str(line_2_raw["price"])
                            + line_1_raw["market_title"]
                            + "@"
                            + str(expected_value),
                            "time_sent": float(line_1_raw["time_sent"]),
                        }
                        arbs_data.append(arb)
    return arbs_data


def find_two_way_h2h_arbs(df):
    arbs_data = []
    grouped_df = df.groupby("identifier")
    for current_id, group in grouped_df:
        if len(group) > 1:
            line_1_raw = group.loc[group["price"].idxmax()]
            line_2_raw = group.loc[group["price"].idxmin()]

            odd_1 = convert_american_to_decimal(line_1_raw["price"])
            odd_2 = convert_american_to_decimal(line_2_raw["price"])

            expected_value = round(
                calc_expected_value(odd1=odd_1,odd2=odd_2), 2
            )
            condition1 = expected_value > 0
            # condition2 = line_1_raw["name"] != line_2_raw["name"]
            if condition1:
                stakes = calc_stake_size(odd1=odd_1,odd2=odd_2)
                arb = {
                    "market": line_1_raw["market_title"],
                    "line_1": {
                        "bookmaker": line_1_raw["bookmaker_key"],
                        "name": line_1_raw["name"],
                        "price": int(line_1_raw["price"]),
                        "implied odd": round(
                            calc_implied_probability(line_1_raw["price"]), 2
                        ),
                        "stake": round(stakes[0], 2),
                    },
                    "line_2": {
                        "bookmaker": line_2_raw["bookmaker_key"],
                        "name": line_2_raw["name"],
                        "price": int(line_2_raw["price"]),
                        "implied odd": round(
                            calc_implied_probability(line_2_raw["price"]), 2
                        ),
                        "stake": round(stakes[1], 2),
                    },
                    "expected_value": float(expected_value),
                    "commence_time": float(line_1_raw["commence_time"]),
                    "league": line_1_raw["sport_title"],
                    "game_title": (f"{line_1_raw['home_team']} (H) @ {line_1_raw['away_team']} (A)"),
                    "last_update": float(line_1_raw["last_update"]),
                    "id": line_1_raw["bookmaker_key"]
                    + line_2_raw["bookmaker_key"]
                    + str(line_1_raw["price"])
                    + str(line_2_raw["price"])
                    + line_1_raw["market_title"]
                    + "@"
                    + str(expected_value),
                    "time_sent": float(line_1_raw["time_sent"]),
                }
                arbs_data.append(arb)
    return arbs_data


def generate_lines_df(data_json, time_sent):
    totals_spreads= []
    two_way_h2h = []
    three_way_h2h = []

    for game in data_json:
        identifier = game.get("id")
        sport_key = game.get("sport_key")
        commence_time = convert_iso_to_timestamp(game.get("commence_time"))
        home_team = game.get("home_team")
        away_team = game.get("away_team")
        sport_title = game.get("sport_title")
        for bookmaker in game.get("bookmakers", []):
            bookmaker_key = bookmaker.get("key")

            for market in bookmaker.get("markets", []):
                market_last_update = convert_iso_to_timestamp(market.get("last_update"))
                market_title = market.get("key")

                for outcome in market.get("outcomes", []):
                    name = outcome.get("name")
                    price = outcome.get("price")
                    point = outcome.get("point") or None
                    new_row = {
                        "identifier": identifier,
                        "sport_key": sport_key,
                        "bookmaker_key": bookmaker_key,
                        "market_title": market_title,
                        "name": name,
                        "price": price,
                        "point": point,
                        "last_update": market_last_update,
                        "commence_time": commence_time,
                        "home_team": home_team,
                        "away_team": away_team,
                        "sport_title": sport_title,
                        "time_sent": time_sent,
                    }
                    if len(market.get("outcomes", [])) > 2:
                        three_way_h2h.append(new_row)
                    else:
                        if new_row["market_title"]=="totals":
                            totals_spreads.append(new_row)
                        elif new_row["market_title"]=="h2h":
                            two_way_h2h.append(new_row)
                        elif new_row["market_title"]=="spreads":
                            totals_spreads.append(new_row)

    return [
        pd.DataFrame(two_way_h2h),
        pd.DataFrame(totals_spreads),
        pd.DataFrame(three_way_h2h),
    ]


# time conversion
def convert_iso_to_timestamp(iso_str):
    dt = datetime.fromisoformat(iso_str.rstrip("Z"))
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


def serialize_arb_opportunity(arb_opportunity):
    return {
        "market": arb_opportunity.market,
        "line_1": arb_opportunity.line_1,
        "line_2": arb_opportunity.line_2,
        "expected_value": arb_opportunity.expected_value,
        "commence_time": arb_opportunity.commence_time,
        "league": arb_opportunity.league,
        "game_title": arb_opportunity.game_title,
        "last_update": arb_opportunity.last_update,
        "id": arb_opportunity.id,
        "time_sent": arb_opportunity.time_sent,
    }
