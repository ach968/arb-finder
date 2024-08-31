def calc_implied_probability(odd):
    return 1/odd

def calc_stake_size(odd1, odd2):
    implied1 = calc_implied_probability(odd1)
    implied2 = calc_implied_probability(odd2)
    total_implied = implied1 + implied2
    stake1 = (implied1 / total_implied)
    stake2 = (implied2 / total_implied)
    return [stake1, stake2]


def calc_expected_value(odd1, odd2):
    impl_odd_1 = calc_implied_probability(odd1)
    impl_odd_2 = calc_implied_probability(odd2)
    return 1-(impl_odd_1 + impl_odd_2)


def convert_american_to_decimal(odd):
    if odd > 0:
        return 1 + odd / 100
    else:
        return 1 - 100 / odd

def convert_decimal_to_american(odd):
    if odd >= 2:
        return (odd - 1) * 100
    else:
        return -100 / (odd - 1)