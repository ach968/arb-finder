from database import db

class Sport(db.Model):
    key = db.Column(db.String(), primary_key=True, nullable=False, unique=True)
    group = db.Column(db.String())
    title = db.Column(db.String())
    description = db.Column(db.String())
    active = db.Column(db.Boolean)
    has_outrights = db.Column(db.Boolean)
    time_sent = db.Column(db.Float)

    def __repr__(self):
        return f'<Sport {self.title}>'
