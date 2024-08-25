import json
from urllib.request import urlopen

from flask import Blueprint, render_template, request, redirect, jsonify
from sqlalchemy.dialects.postgresql import insert

from app.models.sport import Sport
from database_init import db
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

sport_blueprint = Blueprint('sport', __name__)


@sport_blueprint.route('/api/sport', methods=['POST'])
def sport_blueprint_post():
    api_key = request.headers.get('x-api-key')
    if not api_key:
        return {'error': 'missing API key!'}, 401

    data = request.get_json()
    if not data:
        return {'error': 'no data provided!'}, 400
    time_sent = data.get('time_sent')

    try:
        save_sport_model(api_key, time_sent)
        return {'success': 'sports successfully updated!'}, 200
    except Exception as e:
        return {'error': f'{e}, rollback executed!'}, 500


def save_sport_model(api_key, time_sent):
    template_url = f"https://api.the-odds-api.com/v4/sports?apiKey={api_key}"
    response = urlopen(template_url)
    data_json = json.loads(response.read())

    for sport in data_json:
        sport_key = sport.get('key')
        sport_group = sport.get('group')
        sport_title = sport.get('title')
        sport_description = sport.get('description')
        sport_active = sport.get('active')
        sport_has_outrights = sport.get('has_outrights')

        # upsert operation
        stmt = (insert(Sport).values(
            key=sport_key,
            group=sport_group,
            title=sport_title,
            description=sport_description,
            active=sport_active,
            has_outrights=sport_has_outrights,
            time_sent=time_sent
        )
        # update if not unique
        .on_conflict_do_nothing(
            index_elements=['key']
        ))

        try:
            db.session.execute(stmt)
            db.session.commit()
            logger.info(f"sport {sport_key} updated successfully!")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"error updating sport {sport_key}")
