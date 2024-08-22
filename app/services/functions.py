from app.models.sport import Sport


def calc_implied_probability(odd):
    absolute = abs(odd)
    if odd < 0:
        return absolute / (absolute + 100)
    if odd > 0:
        return 100 / (absolute + 100)


def calc_stake_size(odd1, odd2, wager):
    implied1 = calc_implied_probability(odd1)
    implied2 = calc_implied_probability(odd2)
    total_implied = implied1 + implied2
    stake1 = (implied1 / total_implied) * wager
    stake2 = (implied2 / total_implied) * wager
    return [stake1, stake2]


def calc_expected_value(odd1, odd2):
    impl_odd_1 = calc_implied_probability(odd1)
    impl_odd_2 = calc_implied_probability(odd2)
    return impl_odd_1 + impl_odd_2

def fetch_all_sports():
    sports_keys = [item[0] for item in Sport.query.with_entities(Sport.key).all()]
    return sports_keys