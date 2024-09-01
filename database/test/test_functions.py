

from app.services.functions import (
    calc_implied_probability,
    calc_stake_size,
    calc_expected_value,
    convert_american_to_decimal,
    convert_decimal_to_american
)


def find_expected_value():
    while True:
        odd1 = convert_american_to_decimal(int(input("\nEnter odd 1: ")))
        odd2 = convert_american_to_decimal(int(input("Enter odd 2: ")))
        output = calc_stake_size(odd1, odd2)
        expected_value = 1 - calc_expected_value(odd1, odd2)
        # expected_payout = ((odd1 / 100) + 1) * output[0]
        print(f"\nImplied probability of {odd1} (odd 1): {round(calc_implied_probability(odd1)*100,2)}%")
        print(f"Implied probability of {odd2} (odd 2): {round(calc_implied_probability(odd2)*100,2)}%")
        print(
            f"\nExpected value: {round(100-(expected_value*100),2)}% \nStake on {odd1}: {round(output[0]*100,2)}%\nStake on {odd2}: {round(output[1]*100,2)}%"
        )
        # print(f"\nExpected payout: %{round(expected_payout * 100,2)}%")
        cont = input('\nX to exit: ')
        if cont.lower() == "x":
            break


if __name__ == "__main__":
    find_expected_value()
