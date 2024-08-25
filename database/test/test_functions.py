

from app.services.functions import (
    calc_implied_probability,
    calc_stake_size,
    calc_expected_value,
)


def find_expected_value():
    while True:
        odd1 = int(input("\nEnter odd 1: "))
        odd2 = int(input("Enter odd 2: "))
        output = calc_stake_size(odd1, odd2)
        expected_value = 1 - calc_expected_value(odd1, odd2)
        expected_payout = ((odd1 / 100) + 1) * output[0]

        print(
            f"\n{round(expected_value*100,2)}% possible return\nStake on {odd1}: {round(output[0]*100,2)}%\nStake on {odd2}: {round(output[1]*100,2)}%"
        )
        print(f"\nExpected payout: %{round(expected_payout * 100,2)}")
        cont = input("X to exit: ")
        if cont.lower() == "x":
            break


if __name__ == "__main__":
    find_expected_value()
