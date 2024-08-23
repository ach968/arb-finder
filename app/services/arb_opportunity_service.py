import json
from datetime import datetime, timezone
from urllib.request import urlopen
import logging

import pandas as pd
from sqlalchemy.dialects.postgresql import insert

from app.models.arb_opportunity import ArbOpportunity
from app.services.functions import calc_implied_probability, calc_expected_value
from app.services.no_fly_list import no_fly_list
from database import db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def serialize_arb_opportunity(arb_opportunity):
    return {
        'market': arb_opportunity.market,
        'line_1': arb_opportunity.line_1,
        'line_2': arb_opportunity.line_2,
        'expected_value': arb_opportunity.expected_value,
        'commence_time': arb_opportunity.commence_time,
        'league': arb_opportunity.league,
        'game_title': arb_opportunity.game_title,
        'last_update': arb_opportunity.last_update,
        'id': arb_opportunity.id,
        'time_sent': arb_opportunity.time_sent
    }


def save_arb_opportunity_model(api_key, sports, markets_string, time_sent):
    all_data = []
    for sport in sports:
        if not no_fly_list.get(sport):
            try:
                template_url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={api_key}&regions=us,us2&markets={markets_string}&oddsFormat=american'
                response = urlopen(template_url)
                data_json = json.loads(response.read())
                df = generate_lines_df(data_json, time_sent)
                all_data.extend(find_arb_opportunities(df))
            except:
                continue

    successful_attempts = 0
    total_attempts = 0
    for data in all_data:
        upsert_stmt = insert(ArbOpportunity).values(data).on_conflict_do_update(index_elements=['id'],
                                                                                set_={'time_sent': data['time_sent']})
        try:
            db.session.execute(upsert_stmt)
            successful_attempts += 1
        except Exception as e:
            db.session.rollback()
            logger.error(f'error inserting data [{data}]: {str(e)}')
            continue
        total_attempts += 1
    db.session.commit()

    return f'{len(sports)} sports processed, {successful_attempts} out of {total_attempts} opportunities successfully inserted.'


def find_arb_opportunities(df):
    opportunities_data = []

    # group data by 'identifier'
    grouped = df.groupby('identifier')

    for current_id, group in grouped:
        commence_time = float(group['commence_time'].iloc[0])
        game_title = (f"{group['home_team'].iloc[0]} (H) @ "
                      f"{group['away_team'].iloc[0]} (A)")
        league = group['sport_title'].iloc[0]
        best_underdog = group.loc[group['price'].idxmax()]
        best_favorite = group.loc[group['price'].idxmin()]

        condition1 = (calc_implied_probability(best_underdog['price']) +
                      calc_implied_probability(best_favorite['price']) < 1)
        condition2 = best_underdog['bookmaker_key'] != best_favorite['bookmaker_key']
        condition3 = best_underdog['name'] != 'Draw' and best_favorite['name'] != 'Draw'
        if condition1 and condition2 and condition3:
            expected_value = round(1 - float(calc_expected_value(best_underdog['price'], best_favorite['price'])), 2)
            opportunity = {
                'market': best_underdog['market_title'],
                'line_1': {
                    'bookmaker': best_underdog['bookmaker_key'],
                    'name': best_underdog['name'],
                    'price': int(best_underdog['price']),
                    'implied odd': round(calc_implied_probability(best_underdog['price']), 2)
                },
                'line_2': {
                    'bookmaker': best_favorite['bookmaker_key'],
                    'name': best_favorite['name'],
                    'price': int(best_favorite['price']),
                    'implied odd': round(calc_implied_probability(best_favorite['price']), 2)
                },
                'expected_value': expected_value,
                'commence_time': commence_time,
                'league': league,
                'game_title': game_title,
                'last_update': float(best_underdog['last_update']),
                'id': best_underdog['bookmaker_key'] + best_favorite['bookmaker_key'] + str(
                    best_underdog['price']) + str(
                    best_favorite['price']) + best_underdog['market_title'] + '@' + str(expected_value),
                'time_sent': float(best_underdog['time_sent'])
            }
            opportunities_data.append(opportunity)

    return opportunities_data


def generate_lines_df(data_json, time_sent):
    rows = []

    for game in data_json:
        identifier = game.get('id')
        sport_key = game.get('sport_key')
        commence_time = convert_iso_to_timestamp(game.get('commence_time'))
        home_team = game.get('home_team')
        away_team = game.get('away_team')
        sport_title = game.get('sport_title')
        for bookmaker in game.get('bookmakers', []):
            bookmaker_key = bookmaker.get('key')

            for market in bookmaker.get('markets', []):
                market_last_update = convert_iso_to_timestamp(market.get('last_update'))
                market_title = market.get('key')

                for outcome in market.get('outcomes', []):
                    name = outcome.get('name')
                    price = outcome.get('price')
                    new_row = {
                        'identifier': identifier,
                        'sport_key': sport_key,
                        'bookmaker_key': bookmaker_key,
                        'market_title': market_title,
                        'name': name,
                        'price': price,
                        'last_update': market_last_update,
                        'commence_time': commence_time,
                        'home_team': home_team,
                        'away_team': away_team,
                        'sport_title': sport_title,
                        'time_sent': time_sent
                    }
                    rows.append(new_row)

    return pd.DataFrame(rows)


# time conversion
def convert_iso_to_timestamp(iso_str):
    dt = datetime.fromisoformat(iso_str.rstrip('Z'))
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()
