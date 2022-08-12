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

xdxd = types.get_definitions_product_type(productType="RUG", marketplaceIds=['A1F83G8C2ARO7P'])
print(xdxd)
# xd = types.search_definitions_product_types(marketplaceIds=['A1F83G8C2ARO7P'])
# print(xd)


# def add_item_uk():
#     file = open('test3.json', "r+")
#     body = json.load(file)
#     resp = listing.put_listings_item(sellerId='A2YSV8HF6GQ3SP', sku='EWP-SATURN-CER-2', body=body,
#                                      marketplaceIds=['A1F83G8C2ARO7P'])
#     print(resp)
#     file.close()
#
#
# def add_item_us():
#     file2 = open('test2.json', "r+")
#     body2 = json.load(file2)
#     resp = listing.put_listings_item(sellerId='A2YSV8HF6GQ3SP', sku='EWP-SATURN-CER-2', body=body2,
#                                      marketplaceIds=['ATVPDKIKX0DER'])
#     print(resp)
#     file2.close()


def patch_uk(sku, keywords, text):

    ##############Edit Title###################
    try:
        listing.get_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku,
                                  marketplaceIds=['A1C3SOZRARQ6R3'])
        print("found")
    except:
        print("not found")
        return
    ###########################################

    ##############Create Keywords##############

    keywords = keywords.lower()
    print(text)
    print(keywords)
    ###########################################

    ###############Send Request################
    with open('patch_demo.json', 'r') as file:
        data = file.readlines()
    with open('patch_demo.json', 'w') as file:
        try:
            data[8] = '\t\t  "value": "'+text+'",\n'
            data[8] = data[8].encode('utf', 'ignore').decode('1252')
            data[19] = '\t\t  "value": "'+keywords+'",\n'
            data[19] = data[19].encode('utf', 'ignore').decode('1252')
            file.writelines(data)
        except:
            data[8] = '\t\t  "value": "' + text + '",\n'
            data[8] = data[8].encode('1252', 'ignore').decode('1252')
            data[19] = '\t\t  "value": "' + keywords + '",\n'
            data[19] = data[19].encode('1252', 'ignore').decode('1252')
            file.writelines(data)

    file = open('patch_demo.json', "r+")
    body = json.load(file)
    # print(body)
    resp = listing.patch_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku, body=body,
                                       marketplaceIds=['A1C3SOZRARQ6R3'])
    print(resp)
    file.close()
    ###########################################


# sku_file = open("inv_pl.txt", "r+", encoding="utf-8")
# skus = sku_file.read().splitlines()
# sku_file.close()
#
# counter = 0
# total = str(len(skus)/3)
# for i in range(0, len(skus), 3):
#     counter += 1
#     print(str(counter)+" out of "+total)
#     patch_uk(skus[i], skus[i+2], skus[i+1])

# {
#   "productType":"PERSONALBODYCARE",
#   "patches":[
#     {
#       "op":"replace",
#       "path":"/attributes/item_name",
#       "value":[
#         {
# 		  "value": "Colorado Border Decorative Carpet Beige - Confetti",
#           "marketplace_id": "A1F83G8C2ARO7P"
#         }
#       ]
#     },
#     {
#       "op": "replace",
#       "path": "/attributes/item_package_dimensions",
#       "value": [
#         {
#           "length": {
#             "value": 30,
#             "unit": "centimeters"
#           },
#           "height": {
#             "value": 140,
#             "unit": "centimeters"
#           },
#           "width": {
#             "value": 30,
#             "unit": "centimeters"
#           },
#           "marketplace_id": "A1F83G8C2ARO7P"
#         }
#       ]
#     },
#     {
#       "op":"replace",
#       "path":"/attributes/item_package_weight",
#       "value":[
#         {
#           "value": 8,
#           "unit": "kilograms",
#           "marketplace_id": "A1F83G8C2ARO7P"
#         }
#       ]
#     },
#   ]
# }
