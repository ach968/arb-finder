import json
from datetime import datetime, timezone
from urllib.request import urlopen
import logging

import pandas as pd
from sqlalchemy.dialects.postgresql import insert

from app.models.arb_opportunity import ArbOpportunity
from app.services.functions import calc_implied_probability, calc_expected_value, calc_stake_size
from app.services.no_fly_list import no_fly_list
from database_init import db

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
    processed_sports = 0
    for sport in sports:
        if not no_fly_list.get(sport):
            try:
                template_url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={api_key}&bookmakers=fliff,bovada,betonlineag&markets={markets_string}&oddsFormat=american'
                response = urlopen(template_url)
                data_json = json.loads(response.read())
                df = generate_lines_df(data_json, time_sent)
                all_data.extend(find_arb_opportunities(df))
            except:
                continue
            processed_sports += 1

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

    return f'{processed_sports} sports processed, {successful_attempts} out of {total_attempts} opportunities successfully found!'


def find_arb_opportunities(df):
    opportunities_data = []

    # group data by 'identifier'
    grouped = df.groupby('identifier')

    for current_id, group in grouped:
        commence_time = float(group['commence_time'].iloc[0])
        game_title = (f"{group['home_team'].iloc[0]} (H) @ "
                      f"{group['away_team'].iloc[0]} (A)")
        league = group['sport_title'].iloc[0]
        line_1_raw = group.loc[group['price'].idxmax()]
        line_2_raw = group.loc[group['price'].idxmin()]

        stakes = calc_stake_size(line_1_raw['price'], line_2_raw['price'])

        condition1 = (calc_implied_probability(line_1_raw['price']) +
                      calc_implied_probability(line_2_raw['price']) < 1)
        condition2 = line_1_raw['bookmaker_key'] != line_2_raw['bookmaker_key']
        condition3 = line_1_raw['name'] != 'Draw' and line_2_raw['name'] != 'Draw'
        if condition1 and condition2 and condition3:
            expected_value = round(1 - float(calc_expected_value(line_1_raw['price'], line_2_raw['price'])), 2)
            opportunity = {
                'market': line_1_raw['market_title'],
                'line_1': {
                    'bookmaker': line_1_raw['bookmaker_key'],
                    'name': line_1_raw['name'],
                    'price': int(line_1_raw['price']),
                    'implied odd': round(calc_implied_probability(line_1_raw['price']), 2),
                    'stake': round(stakes[0], 2)
                },
                'line_2': {
                    'bookmaker': line_2_raw['bookmaker_key'],
                    'name': line_2_raw['name'],
                    'price': int(line_2_raw['price']),
                    'implied odd': round(calc_implied_probability(line_2_raw['price']), 2),
                    'stake': round(stakes[1], 2)
                },
                'expected_value': expected_value,
                'commence_time': commence_time,
                'league': league,
                'game_title': game_title,
                'last_update': float(line_1_raw['last_update']),
                'id': line_1_raw['bookmaker_key'] + line_2_raw['bookmaker_key'] + str(
                    line_1_raw['price']) + str(
                    line_2_raw['price']) + line_1_raw['market_title'] + '@' + str(expected_value),
                'time_sent': float(line_1_raw['time_sent'])
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