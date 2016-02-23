from AmazonRequestsHelpers import *
import random
import jsonpickle


"""
Repeatedly calls the Amazon Product Advertising API with random item categories until a list of AmazonItem objects
is received.  Then picks one of those AmazonItem at random and returns it.

Slow as molasses.

ptype: max_price: int, min_price: int
@param max_price: a positive int corresponding to the maximum price of an item in cents
@param min_price: a positive int corresponding to the minimum price of an item in cents
@rtype: AmazonItem
@return: An AmazonItem chosen from a random category
"""
def request_amazon_product(max_price, min_price):
    products = []
    while not products:
        products = get_amazon_products(max_price, min_price)
    return random.choice(products)


"""
Returns a JSON String containing a single randomly chosen AmazonItem

@ptype max_price: int, min_price: int
@param max_price: a positive int corresponding to the maximum price of an item in cents
@param min_price: a positive int corresponding to the minimum price of an item in cents
@rtype String
@return: JSON formatted AmazonItem as a String
"""
def request_amazon_product_json(max_price, min_price):
    amazon_item = jsonpickle.encode(request_amazon_product(max_price, min_price))
    return amazon_item

# Get this thing started
# request_amazon_product(1085, 21)
