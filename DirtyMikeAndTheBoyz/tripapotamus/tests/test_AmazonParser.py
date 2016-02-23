import os

import unittest
import django
from test.test_deque import fail
from tripapotamus.logic.AmazonRequestsHelpers import *
from tripapotamus.logic.AmazonRequests import request_amazon_product

"""
This test parses AmazonResponse.xml.  AmazonResponse.xml is a dummy file containing a list of five item entries:
item_1, item_2, item_3, item_4, item_5.  Item properties are as follows:  for an item_x, price = xxxx, title = item_x,
amazon_url = item_x_url, amazon_image_url = item_x_url.

The following items have been made invalid to test item pruning
item_3 is an invalid item and should not be parsed due to a missing image.
item_5 is an invalid item and should not be parsed due to a missing price (ie: is not for sale).

The valid items are arranged as follows, and successful tests will have price equal to xxxx.
item_1 regular price 1111, no other pricing options
item_2 offer price 2222, (lower priority prices: list, are 9999)
item_4 sale price 4444, (lower priority prices: list, offer are 9999)
"""
class AmazonParserTestCase(unittest.TestCase):

    def testParser(self):
        path = os.path.join("ParserTestFiles", "AmazonResponse.xml")
        xmlfile = open(path)
        content = xmlfile.read()

        amazon_items_list = parse_amazon_products(content)

        # test to see if there are three AmazonItems in the list
        self.assertEquals(len(amazon_items_list), 3)

        #test to see if the list is exactly what we predict
        self.assertEquals(amazon_items_list[0].title, "item_1")
        self.assertEquals(amazon_items_list[0].amazon_url, "item_1_url")
        self.assertEquals(amazon_items_list[0].picture_url, "item_1_img_url")
        self.assertEquals(amazon_items_list[0].price, "1111")

        self.assertEquals(amazon_items_list[1].title, "item_2")
        self.assertEquals(amazon_items_list[1].amazon_url, "item_2_url")
        self.assertEquals(amazon_items_list[1].picture_url, "item_2_img_url")
        self.assertEquals(amazon_items_list[1].price, "2222")

        self.assertEquals(amazon_items_list[2].title, "Samsung OEM Universal Micro Home Travel Charger for Samsung Galaxy S3/S4/Note 2 and Other Smartphones - Non-Retail Packaging - White")
        self.assertEquals(amazon_items_list[2].amazon_url, "item_4_url")
        self.assertEquals(amazon_items_list[2].picture_url, "item_4_img_url")
        self.assertEquals(amazon_items_list[2].price, "4444")
        
    def testPrice(self):
        list_of_products = get_amazon_products(200, 50)
        for prod in list_of_products:
            if len(list_of_products) > 0:
                price = prod.price
                if price < 200 or price > 500:
                    fail

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(AmazonParserTestCase("testParser"))
    test_suite.addTest(AmazonParserTestCase("testPrice"))
    return test_suite

mySuite = suite()
django.setup()
runner = unittest.TextTestRunner
unittest.TextTestRunner(verbosity=2).run(mySuite)


