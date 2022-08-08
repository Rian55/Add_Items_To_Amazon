import json
from configparser import ConfigParser
from sp_api.base import Marketplaces
from sp_api.api import ListingsItems
from sp_api.api import ProductTypeDefinitions

config = ConfigParser()
config.read(".config.txt")
credentials = dict(config['default'])
listing = ListingsItems(credentials=credentials, marketplace=Marketplaces.UK)
listing_us = ListingsItems(credentials=credentials, marketplace=Marketplaces.US)
types = ProductTypeDefinitions(credentials=credentials, marketplace=Marketplaces.UK)
# notifications = Notifications(credentials=credentials, marketplace=Marketplaces.UK)

# xdxd = types.get_definitions_product_type(productType="PERSONALBODYCARE", marketplaceIds=['A1F83G8C2ARO7P'])
# print(xdxd)
# xd = types.search_definitions_product_types(marketplaceIds=['A1F83G8C2ARO7P'])
# print(xd)


def add_item_uk():
    file = open('test3.json', "r+")
    body = json.load(file)
    resp = listing.put_listings_item(sellerId='A2YSV8HF6GQ3SP', sku='EWP-SATURN-CER-2', body=body,
                                     marketplaceIds=['A1F83G8C2ARO7P'])
    print(resp)
    file.close()


def add_item_us():
    file2 = open('test2.json', "r+")
    body2 = json.load(file2)
    resp = listing.put_listings_item(sellerId='A2YSV8HF6GQ3SP', sku='EWP-SATURN-CER-2', body=body2,
                                     marketplaceIds=['ATVPDKIKX0DER'])
    print(resp)
    file2.close()


def patch_uk(sku):
    text = listing.get_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku,
                                     marketplaceIds=['A1F83G8C2ARO7P']).payload['summaries'][0]['itemName']
    ##############Edit Title###################
    text = text + " - Doxa"
    ###########################################

    ##############Create Keywords##############
    keywords = ""
    if "Men" in text:
        keywords = "shampoo, men shampoo, haircare, suitable for all hair types, bath, shower, " \
                   "man shampoo, haircare products"
        text = text.replace("eworldpartner Doxa", "Men Shampoo")
    elif "Shower Gel" in text:
        keywords = "shower gel, personal care, unisex, women, men, bath, shower, cherry milk, mango milk, blackberry " \
                   "milk, avocado milk, fresh, summer edition"
        text = text.replace("eworldpartner Doxa", "Shower Gel")
    elif "Liquid Soap" in text:
        keywords = "vegan liquid soap, organic liquid soap, vegan, organic, liquid soap, personal care, suitable all " \
                   "skin types, unisex, vegan products, organic products"
        text = text.replace("eworldpartner Doxa", "Liquid Soap")
    elif "Baby" in text:
        keywords = "baby, baby soap, baby shampoo, bath time, baby cleaning, bath, mother, shower, new, " \
                   "most purchased, girls, boys, unisex baby soap, solid soap bar, baby soap"
        text = text.replace("eworldpartner Doxa", "Baby Shampoo")
    elif "Beauty Soap" in text:
        keywords = "personal care, women, men, bodycare, soap bar, soap, bar, new, most purchased, set, soap set, " \
                   "fragrance"
        text = text.replace("eworldpartner Doxa", "Soap Bar")
    elif "Vegan Shampoo" in text:
        keywords = "vegan shampoo, organic shampoo, vegan, organic, skincare, bath, shower, argan oil, lemon oil, " \
                   "keratine, olive oil, argan oil shampoo, olive oil shampoo, lemon oil " \
                   "shampoo, women shampoo, haircare products"
        text = text.replace("eworldpartner Doxa", "Vegan Shampoo")

    keywords = keywords.replace(",", ";")
    print(text)
    print(keywords)
    ###########################################
    with open('patch_demo.json', 'r') as file:
        data = file.readlines()
    with open('patch_demo.json', 'w') as file:
        data[8] = f'\t\t  "value": "{text}",\n'
        data[50] = f'\t\t  "value": "{keywords}",\n'
        file.writelines(data)

    file = open('patch_demo.json', "r+")
    body = json.load(file)
    # print(body)
    resp = listing.patch_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku, body=body,
                                       marketplaceIds=['A1F83G8C2ARO7P'])
    print(resp)
    file.close()


sku_file = open("uk_personalbodycare.txt", "r+")
skus = sku_file.read().splitlines()
sku_file.close()

counter = 0
for sku in skus:
    counter += 1
    print(str(counter)+" out of "+str(len(skus)))
    patch_uk(sku)
