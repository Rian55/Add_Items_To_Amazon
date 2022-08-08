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

# xdxd = types.get_definitions_product_type(productType="SHOES", marketplaceIds=['A1F83G8C2ARO7P'])
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
    text = text.replace("eworldpartner Oguzhan Shoes ", "")
    if "(" in text:
        text = text.replace("(", "- Oguzhan Shoes (")
    else:
        text += " - Oguzhan Shoes"

    print(text)
    with open('new.json', 'r') as file:
        data = file.readlines()
    with open('new.json', 'w') as file:
        data[8] = f'\t\t  "value": "{text}",\n'
        file.writelines(data)

    file = open('new.json', "r+")
    body = json.load(file)
    print(body)
    resp = listing.patch_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku, body=body,
                                       marketplaceIds=['A1F83G8C2ARO7P'])
    print(resp)
    file.close()


sku_file = open("skus.txt", "r+")
skus = sku_file.read().splitlines()
sku_file.close()

counter = 0
for sku in skus:
    counter += 1
    print(str(counter)+" out of "+str(len(skus)))
    patch_uk(sku)
