import logging
from flask import Blueprint, request, jsonify

from app.models.arb_opportunity import ArbOpportunity

from app.services.arb_opportunity_service import (
    generate_lines_df,
    find_arb_opportunities,
    serialize_arb_opportunity,
    save_arb_opportunity_model,
)
from database_init import db

arb_opportunity_blueprint = Blueprint("arb_opportunity", __name__)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@arb_opportunity_blueprint.route("/api/arb_opportunity", methods=["POST"])
def arb_opportunity_blueprint_post():
    api_key = request.headers.get("x-api-key")
    if not api_key:
        return {"error": "missing API key!"}, 401

    data = request.get_json()
    if not data:
        return {"error": "no data provided!"}, 400

    sports = data.get("sports")
    if not sports:
        return jsonify({"error": "missing sports information"}), 400
    markets_list = data.get("markets")
    if not markets_list:
        return jsonify({"error": "markets list is missing or empty"}), 400
    time_sent = data.get("time_sent")
    if not time_sent:
        return jsonify({"error": "missing time sent information"}), 400
    bookmakers = data.get("bookmakers")
    if not bookmakers:
        return jsonify({"error": "missing bookmakers information"}), 400

    markets_string = ",".join(markets_list)
    bookmakers_string = ",".join(bookmakers)
    outcome = save_arb_opportunity_model(
        api_key=api_key,
        sports=sports,
        markets_string=markets_string,
        time_sent=time_sent,
        bookmakers=bookmakers_string,
    )
    try:
        logger.info(outcome)
        return {"success": str(outcome)}
    except Exception as e:
        logger.error(f"{e}")
        return {"error": f"{e}, rollback executed!"}, 500


@arb_opportunity_blueprint.route("/api/arb_opportunity", methods=["GET"])
def arb_opportunity_blueprint_get():
    get_latest_data = request.args.get("get_latest_data", type=bool, default=False)
    if not get_latest_data:
        return jsonify({"error": "get latest data constraint is null or empty!"}), 400

    try:
        if get_latest_data:
            max_time_sent = db.session.query(
                db.func.max(ArbOpportunity.time_sent)
            ).scalar()
            opportunities = ArbOpportunity.query.filter_by(
                time_sent=max_time_sent
            ).all()
            results = [
                serialize_arb_opportunity(opportunity) for opportunity in opportunities
            ]
            return results
        else:
            opportunities = ArbOpportunity.query.all()
            results = [
                serialize_arb_opportunity(opportunity) for opportunity in opportunities
            ]
            return results

    except Exception as e:
        return {"error": f"{e}, operation failed!"}, 500
