from sqlalchemy.dialects.postgresql import JSONB

from database_init import db


class ArbOpportunity(db.Model):
    market = db.Column(db.String(), nullable=False)
    line_1 = db.Column(JSONB, nullable=False)
    line_2 = db.Column(JSONB, nullable=False)
    expected_value = db.Column(db.Float, nullable=False)
    commence_time = db.Column(db.Float, nullable=False)
    league = db.Column(db.String())
    game_title = db.Column(db.String())
    last_update = db.Column(db.Float)
    id = db.Column(db.String(), nullable=False, primary_key=True, unique=True)
    time_sent = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Arb Opportunity {self.id}>'
