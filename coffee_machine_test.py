import unittest
from coffee_machine import Coffee_Machine


class Test_Coffee_Machine(unittest.TestCase):
    def test(self):
        cm = Coffee_Machine()
        # Testing for the smallest amount of coins with the correct amount
        self.assertDictEqual(cm.return_coins(3.14, 500),
                             {'num_one_cent_coins': 1, 'num_two_cent_coins': 0, 'num_five_cent_coins': 1,
                              'num_ten_cent_coins': 1, 'num_twenty_cent_coins': 1, 'num_fifty_cent_coins': 1,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 248})
        self.assertDictEqual(cm.return_coins(3.14, 3.14),
                             {'num_one_cent_coins': 0, 'num_two_cent_coins': 0, 'num_five_cent_coins': 0,
                              'num_ten_cent_coins': 0, 'num_twenty_cent_coins': 0, 'num_fifty_cent_coins': 0,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 0})
        self.assertDictEqual(cm.return_coins(3.14, 3.15),
                             {'num_one_cent_coins': 1, 'num_two_cent_coins': 0, 'num_five_cent_coins': 0,
                              'num_ten_cent_coins': 0, 'num_twenty_cent_coins': 0, 'num_fifty_cent_coins': 0,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 0})
        self.assertDictEqual(cm.return_coins(3.14, 5.14),
                             {'num_one_cent_coins': 0, 'num_two_cent_coins': 0, 'num_five_cent_coins': 0,
                              'num_ten_cent_coins': 0, 'num_twenty_cent_coins': 0, 'num_fifty_cent_coins': 0,
                              'num_one_euro_coins': 0, 'num_two_euro_coins': 1})
        self.assertDictEqual(cm.return_coins(3.14, 7.02),
                             {'num_one_cent_coins': 1, 'num_two_cent_coins': 1, 'num_five_cent_coins': 1,
                              'num_ten_cent_coins': 1, 'num_twenty_cent_coins': 1, 'num_fifty_cent_coins': 1,
                              'num_one_euro_coins': 1, 'num_two_euro_coins': 1})
        self.assertRaises(Exception, cm.return_coins, 3.14, 3.13)  # not enough money inserted
        self.assertRaises(Exception, cm.return_coins, 3.14, -0.1)  # Negative money inserted
        self.assertRaises(Exception, cm.return_coins, -0.1, 500)  # Coffee price set to negative
