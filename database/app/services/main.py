from app.services.functions import calc_implied_probability

def main():  
    while True:
        odd1 = int(input("\nEnter odd 1: "))
        odd2 = int(input("Enter odd 2: "))
        wager = float(input("Enter total wager ($): "))
        output = calc_arbitrage(odd1,odd2,wager)
        percent = 1-calc_percent(odd1,odd2)

        print(f"\n{round(percent*100,2)}% possible return\nStake on {odd1}: ${round(output[0],2)}\nStake on {odd2}: ${round(output[1],2)}")
        print(f"Expected profit: ${round(wager*percent,2)}\n")
        cont = input("C to continue, X to exit: ").lower()
        if cont== "c":
            continue
        if cont== "x":
            break



def calc_arbitrage(odd1,odd2,wager):
    implied1 = calc_implied_probability(odd1)
    implied2 = calc_implied_probability(odd2)
    total_implied = implied1+implied2
    stake1 = (implied1/total_implied)*wager
    stake2 = (implied2/total_implied)*wager
    return [stake1,stake2]
    
    

def calc_percent(odd1,odd2):
    implOdd1 = calc_implied_probability(odd1)
    implOdd2 = calc_implied_probability(odd2)
    return implOdd1+implOdd2



main()