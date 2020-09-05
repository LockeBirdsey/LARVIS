import math
import unittest


class CoffeeMachine:
    def return_coins(self, coffee_price, eur_inserted):
        if coffee_price < 0:
            raise Exception("Coffee price must be positive")
        if eur_inserted < 0:
            raise Exception("Negative currencies are not allowed")
        if eur_inserted < coffee_price:
            raise Exception("Not enough money inserted")

        remaining_eur = round(eur_inserted - coffee_price, 2)
        # calculate number of 2 euro coins
        num_two_euro_coins = math.floor(remaining_eur / 2)
        # update the remaining money count
        remaining_eur = round(remaining_eur - (num_two_euro_coins * 2), 2)
        # calculate number of 1 euro coins
        num_one_euro_coins = math.floor(remaining_eur)
        remaining_eur = round(remaining_eur - num_one_euro_coins, 2)
        # At this point we are guaranteed to have less than 1 euro
        num_fifty_cent_coins = 0
        num_twenty_cent_coins = 0
        num_ten_cent_coins = 0
        num_five_cent_coins = 0
        num_two_cent_coins = 0
        num_one_cent_coins = 0

        while remaining_eur >= 0.50:
            num_fifty_cent_coins += 1
            remaining_eur = round(remaining_eur - 0.5, 2)
        while remaining_eur >= 0.20:
            num_twenty_cent_coins += 1
            remaining_eur = round(remaining_eur - 0.2, 2)
        while remaining_eur >= 0.10:
            num_ten_cent_coins += 1
            remaining_eur = round(remaining_eur - 0.1, 2)
        while remaining_eur >= 0.05:
            num_five_cent_coins += 1
            remaining_eur = round(remaining_eur - 0.05, 2)
        while remaining_eur >= 0.02:
            num_two_cent_coins += 1
            remaining_eur = round(remaining_eur - 0.02, 2)
        while remaining_eur >= 0.01:
            num_one_cent_coins += 1
            remaining_eur = round(remaining_eur - 0.01, 2)

        change = {"num_one_cent_coins": num_one_cent_coins,
                  "num_two_cent_coins": num_two_cent_coins,
                  "num_five_cent_coins": num_five_cent_coins,
                  "num_ten_cent_coins": num_ten_cent_coins,
                  "num_twenty_cent_coins": num_twenty_cent_coins,
                  "num_fifty_cent_coins": num_fifty_cent_coins,
                  "num_one_euro_coins": num_one_euro_coins,
                  "num_two_euro_coins": num_two_euro_coins}
        return change

    def main(self):
        print("Inserting 500eu for a 3.14eu coffee")
        print(self.return_coins(0, 500))


if __name__ == '__main__':
    cm = CoffeeMachine()
    cm.main()
