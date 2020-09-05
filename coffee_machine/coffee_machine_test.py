import unittest
# For PYCharm
# from coffee_machine.coffeemachine import CoffeeMachine
# For CLI Python
from coffeemachine import CoffeeMachine


class TestCoffeeMachine(unittest.TestCase):
    def test_example(self):
        cm = CoffeeMachine()
        self.assertDictEqual(cm.return_coins(3.14, 500),
                             {'num_one_cent_coins': 1, 'num_two_cent_coins': 0, 'num_five_cent_coins': 1,
                              'num_ten_cent_coins': 1, 'num_twenty_cent_coins': 1, 'num_fifty_cent_coins': 1,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 248})

    def test_exact_change(self):
        cm = CoffeeMachine()
        self.assertDictEqual(cm.return_coins(3.14, 3.14),
                             {'num_one_cent_coins': 0, 'num_two_cent_coins': 0, 'num_five_cent_coins': 0,
                              'num_ten_cent_coins': 0, 'num_twenty_cent_coins': 0, 'num_fifty_cent_coins': 0,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 0})

    def test_one_cent_extra(self):
        cm = CoffeeMachine()
        self.assertDictEqual(cm.return_coins(3.14, 3.15),
                             {'num_one_cent_coins': 1, 'num_two_cent_coins': 0, 'num_five_cent_coins': 0,
                              'num_ten_cent_coins': 0, 'num_twenty_cent_coins': 0, 'num_fifty_cent_coins': 0,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 0})

    def test_two_cent_extra(self):
        cm = CoffeeMachine()
        self.assertDictEqual(cm.return_coins(3.14, 3.16),
                             {'num_one_cent_coins': 0, 'num_two_cent_coins': 1, 'num_five_cent_coins': 0,
                              'num_ten_cent_coins': 0, 'num_twenty_cent_coins': 0, 'num_fifty_cent_coins': 0,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 0})

    def test_five_cent_extra(self):
        cm = CoffeeMachine()
        self.assertDictEqual(cm.return_coins(3.14, 3.19),
                             {'num_one_cent_coins': 0, 'num_two_cent_coins': 0, 'num_five_cent_coins': 1,
                              'num_ten_cent_coins': 0, 'num_twenty_cent_coins': 0, 'num_fifty_cent_coins': 0,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 0})

    def test_ten_cent_extra(self):
        cm = CoffeeMachine()
        self.assertDictEqual(cm.return_coins(3.14, 3.24),
                             {'num_one_cent_coins': 0, 'num_two_cent_coins': 0, 'num_five_cent_coins': 0,
                              'num_ten_cent_coins': 1, 'num_twenty_cent_coins': 0, 'num_fifty_cent_coins': 0,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 0})

    def test_twenty_cent_extra(self):
        cm = CoffeeMachine()
        self.assertDictEqual(cm.return_coins(3.14, 3.34),
                             {'num_one_cent_coins': 0, 'num_two_cent_coins': 0, 'num_five_cent_coins': 0,
                              'num_ten_cent_coins': 0, 'num_twenty_cent_coins': 1, 'num_fifty_cent_coins': 0,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 0})

    def test_fifty_cent_extra(self):
        cm = CoffeeMachine()
        self.assertDictEqual(cm.return_coins(3.14, 3.64),
                             {'num_one_cent_coins': 0, 'num_two_cent_coins': 0, 'num_five_cent_coins': 0,
                              'num_ten_cent_coins': 0, 'num_twenty_cent_coins': 0, 'num_fifty_cent_coins': 1,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 0})

    def test_one_euro_extra(self):
        cm = CoffeeMachine()
        self.assertDictEqual(cm.return_coins(3.14, 4.14),
                             {'num_one_cent_coins': 0, 'num_two_cent_coins': 0, 'num_five_cent_coins': 0,
                              'num_ten_cent_coins': 0, 'num_twenty_cent_coins': 0, 'num_fifty_cent_coins': 0,
                              'num_one_euro_coins': 1, 'num_two_euro_coins': 0})

    def test_two_euro_extra(self):
        cm = CoffeeMachine()
        self.assertDictEqual(cm.return_coins(3.14, 5.14),
                             {'num_one_cent_coins': 0, 'num_two_cent_coins': 0, 'num_five_cent_coins': 0,
                              'num_ten_cent_coins': 0, 'num_twenty_cent_coins': 0, 'num_fifty_cent_coins': 0,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 1})

    def test_return_one_of_each_coin(self):
        cm = CoffeeMachine()
        self.assertDictEqual(cm.return_coins(3.14, 7.02),
                             {'num_one_cent_coins': 1, 'num_two_cent_coins': 1, 'num_five_cent_coins': 1,
                              'num_ten_cent_coins': 1, 'num_twenty_cent_coins': 1, 'num_fifty_cent_coins': 1,
                              'num_one_euro_coins': 1, 'num_two_euro_coins': 1})

    def test_coffee_set_to_zero(self):
        cm = CoffeeMachine()
        self.assertDictEqual(cm.return_coins(0, 500),
                             {'num_one_cent_coins': 0, 'num_two_cent_coins': 0, 'num_five_cent_coins': 0,
                              'num_ten_cent_coins': 0, 'num_twenty_cent_coins': 0, 'num_fifty_cent_coins': 0,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 250})

    def test_zero_money_inserted_and_coffee_set_to_zero(self):
        cm = CoffeeMachine()
        self.assertDictEqual(cm.return_coins(0, 0),
                             {'num_one_cent_coins': 0, 'num_two_cent_coins': 0, 'num_five_cent_coins': 0,
                              'num_ten_cent_coins': 0, 'num_twenty_cent_coins': 0, 'num_fifty_cent_coins': 0,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 0})

    def test_not_enough_money_inserted(self):
        cm = CoffeeMachine()
        self.assertRaises(Exception, cm.return_coins, 3.14, 3.13)  # not enough money inserted

    def test_negative_money_inserted(self):
        cm = CoffeeMachine()
        self.assertRaises(Exception, cm.return_coins, 3.14, -0.1)  # Negative money inserted

    def test_set_to_negative(self):
        cm = CoffeeMachine()
        self.assertRaises(Exception, cm.return_coins, -0.1, 500)  # Coffee price set to negative

    def test_zero_money_inserted(self):
        cm = CoffeeMachine()
        self.assertRaises(Exception, cm.return_coins, -0.1, 0)  # Coffee price set to negative
