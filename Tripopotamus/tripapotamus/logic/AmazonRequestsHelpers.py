import hmac
import urllib2
import hashlib
import xml.etree.ElementTree
import re
import random
import base64
from Item import AmazonItem
from time import strftime, gmtime

"""
Uses the Amazon product advertising API to generate a list of 0-10 AmazonItem objects chosen from a random category
which each costing between max_price and min_price.

@ptype max_price: int
@ptype min_price: int
@param max_price: a positive number corresponding to the cent value of the upper price amount
@param min_price: a positive number corresponding to the cent value of the lower price amount

@rtype: [AmazonItem]
@return: a list of items from a randomly chosen amazon category which cost between min_price and max_price
"""

def get_amazon_products(max_price, min_price):
    search_params = get_search_parameters()
    parameters = {
        'AssociateTag': 'Tripapotamus-20',
        'AWSAccessKeyId': 'AKIAJI5UAMA6N2KYCMWA',
        'Keywords': search_params['category'],
        'MaximumPrice': str(max_price),
        'MinimumPrice': str(min_price),
        'Operation': 'ItemSearch',
        'ResponseGroup': 'Images,ItemAttributes,OfferFull',    # need to add in offer full to retrieve proper sale price.
        'SearchIndex': search_params['category'],
        'Service': 'AWSECommerceService',
        'Sort': search_params['search_type'],
        'Version': '2011-08-01',
        'VariationPage': str(1),
        'Timestamp': get_timestamp(),
    }
    url = 'http://webservices.amazon.com/onca/xml?'
    cstr = get_canonical_string(parameters)
    sig_param = "&Signature=" + get_signature(cstr)
    response = urllib2.urlopen(url + cstr + sig_param).read()
    #print response
    #print "\n\n"
    amazon_items_list = parse_amazon_products(response)
    #print_titles(amazon_items_list)
    return amazon_items_list


"""
Generates a UTC formatted timestamp (no offset) with precision in seconds.
Example: 015-07-14T23:21:05.000Z
"""
def get_timestamp():
    return strftime("%Y-%m-%dT%H:%M:%S.000Z", gmtime())

"""
Generates a URL-formatted unique signature by hashing the input string with the amazon secret access key using
the SHA256 algorithm

@ptype: String
@param: A canonical string which contains a list of byte sorted parameters and a time stamp
@rtype: String
@return: A URL encoded RFC 2104-compliant HMAC
"""
def get_signature(cstr):
    s = "GET\n" + "webservices.amazon.com\n" + "/onca/xml\n" + cstr
    access_key = "2O8wAJG9Rm87BBhPMeKKaf05rPAP97f8GgGfYUVR"
    hash_thing = hmac.new(access_key, msg=s, digestmod=hashlib.sha256).digest()
    return urllib2.quote(base64.b64encode(hash_thing).decode())



"""
Generates a URL-encoded and byte sorted parameter string using the input dictionary

@ptype {String: String}
@param: a dictionary containing parameters.  Keys are the parameter name, and values are the parameter values.
@rtype String
@return URL encoded parameter string
"""
def get_canonical_string(params_dict):
    params_list = []
    for key in sorted(params_dict):
        params_list.append(key + "=" + params_dict[key])
    return urllib2.quote("&".join(params_list), safe='&=')


"""
Parses an XML string returned from the Amazon Product Advertising API and creates a list of up to 10
AmazonItem objects.  Ignores XML entries which have no listed price (ie: are not for sale) or no medium picture.

@ptype String
@param xmlstr: an XML string returned by the Amazon Product Advertising API using the items search functionality
@rtype [AmazonItem]
@return: A lit of up to 10 AmazonItems contained in the original XML String
"""
def parse_amazon_products(xmlstr):
    products = []
    xmlstr = remove_namespace(xmlstr)
    et = xml.etree.ElementTree
    root = et.fromstring(xmlstr)
    items = root.iter('Item')
    for item in items:
        if is_valid_item(item):
            name = get_item_name(item)
            price = get_item_price(item)
            picture_url = get_item_picture_url(item)
            amazon_url = get_item_amazon_url(item)
            amazon_item = AmazonItem(name, price, picture_url, amazon_url)
            products.append(amazon_item)
    return products

def is_valid_item(item):
    has_price = item.find('ItemAttributes').find('ListPrice') is not None
    has_picture = item.find('MediumImage') is not None
    return has_price and has_picture


def get_item_name(item):
    name = item.find('ItemAttributes').find('Title').text
    return name


def get_item_picture_url(item):
    picture_url = item.find('MediumImage').find('URL').text
    return picture_url


def get_item_amazon_url(item):
    amazon_url = item.find('DetailPageURL').text
    return amazon_url

"""
returns the price of the item which is determined according to the following priority scale
Sale Price >> Offer Price >> List Price
"""
def get_item_price(item):
    if item.find('Offers').find('Offer') is not None:
        offer = item.find('Offers').find('Offer')
        if offer.find('OfferListing').find('SalePrice') is not None:
            price = offer.find('OfferListing').find('SalePrice').find('Amount').text #+ ' SALEPOOPIES'
        else:
            price = offer.find('OfferListing').find('Price').find('Amount').text #+ ' OFFERPOOPIES'
    else:
        price = item.find('ItemAttributes').find('ListPrice').find('Amount').text
    return price



"""
Strips the xml namespace attribute from an xml string.  Makes the string easier to work with using ElementTree
"""
def remove_namespace(xmlstr):
    xmlstr = re.sub(' xmlns="[^"]+"', '', xmlstr, count=1)
    return xmlstr


"""
Randomly picks from a list of valid search indices and returns an valid search type for that index as described
in the Amazon Products API documentation. Example: {category: 'Automotive', search_type: 'salesrank'}

@rtype: {category: String, search_type: String}
@return: a dictionary containing a randomly chosen valid search index and search type.
"""
def get_search_parameters():
    r = 'relevancerank'
    s = 'salesrank'
    search_dict = {
        #'Apparel': [r, s],                  ##
        'Appliances': [r, s],
        'ArtsAndCrafts': [r, s],
        'Automotive': [r, s],
        'Baby': [s],                        ##
        'Beauty': [s],
        'Books': [r, s],                    ## gave a response at least once
        #'Classical': [s],
        'Collectibles': [r, s],
        'DVD': [r, s],
        'Electronics': [s],
        #'Fashion': [r],
        #'FashionBaby': [r],    #blank
        #'FashionBoys': [r],    #b
        #'FashionGirls': [r],   #b
        #'FashionMen': [r],     #b
        #'FashionWomen': [r],   #b
        'GiftCards': [r, s],
        'GourmetFood': [r, s],
        'Grocery': [r, s],
        'HealthPersonalCare': [s],
        'HomeGarden': [s],                  ##
        'Industrial': [s],
        'Jewelry': [s],
        'KindleStore': [r, s], #b
        'Kitchen': [s],                     ##
        'LawnAndGarden': [r, s],
        'Luggage': [r],
        'Miscellaneous': [s],               ##
        'Music': [r, s],                    ##
        'MusicalInstruments': [s],
        'OfficeProducts': [s],              ##
        'OutdoorLiving': [s],  #b
        'PCHardware': [s],     #b
        'PetSupplies': [r, s],              ##
        'Photo': [s],                       ##
        #'Shoes': [r],
        'Software': [s],
        'SportingGoods': [r, s],
        'Tools': [s],
        'Toys': [s],
        'UnboxVideo': [r, s],  #b
        'VHS': [r, s],
        'Video': [r, s],       #b
        'VideoGames': [s],                  ##
        'Watches': [r, s],
        'Wireless': [s],                    ##
        'WirelessAccessories': [s],
    }
    category = random.choice(search_dict.keys())
    search_type = random.choice(search_dict[category])
    return {'category': category,
            'search_type': search_type,
            }

"""
Debugging Function
Prints the titles of items which are returned by usage of get_amazon_products(max_price, min_price)
"""
def print_titles(amazon_item_list):
    for item in amazon_item_list:
        print item.title + " **** " + item.price
        print item.amazon_url
        print "\n"