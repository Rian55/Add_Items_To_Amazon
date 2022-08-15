import json
from configparser import ConfigParser
from sp_api.base import Marketplaces
from sp_api.api import ListingsItems
from sp_api.api import ProductTypeDefinitions
import re

config = ConfigParser()
config.read(".config.txt")
credentials = dict(config['default'])
listing = ListingsItems(credentials=credentials, marketplace=Marketplaces.UK)
listing_us = ListingsItems(credentials=credentials, marketplace=Marketplaces.US)
types = ProductTypeDefinitions(credentials=credentials, marketplace=Marketplaces.UK)
# notifications = Notifications(credentials=credentials, marketplace=Marketplaces.UK)

# xdxd = types.get_definitions_product_type(productType="RUG", marketplaceIds=['A1F83G8C2ARO7P'])
# print(xdxd)
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

def change_marketplace(doc, c_code):
    if c_code == "gb":
        doc = re.sub('("\w\w_\w\w)"', '"en_GB"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1F83G8C2ARO7P"', str(doc))
    elif c_code == "us":
        doc = re.sub('("\w\w_\w\w)"', '"en_US"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "ATVPDKIKX0DER"', str(doc))
    elif c_code == "de":
        doc = re.sub('("\w\w_\w\w)"', '"de_DE"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1PA6795UKMFR9"', str(doc))
    elif c_code == "fr":
        doc = re.sub('("\w\w_\w\w)"', '"fr_FR"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A13V1IB3VIYZZH"', str(doc))
    elif c_code == "it":
        doc = re.sub('("\w\w_\w\w)"', '"it_IT"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "APJ6JRA9NG5V4"', str(doc))
    elif c_code == "es":
        doc = re.sub('("\w\w_\w\w)"', '"es_ES"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1RKKUPIHCS9HS"', str(doc))
    elif c_code == "pl":
        doc = re.sub('("\w\w_\w\w)"', '"pl_PL"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1C3SOZRARQ6R3"', str(doc))
    elif c_code == "sw":
        doc = re.sub('("\w\w_\w\w)"', '"sv_SW"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A2NODRKZP88ZB9"', str(doc))
    elif c_code == "nl":
        doc = re.sub('("\w\w_\w\w)"', '"nl_NL"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1805IZSGTT6HS"', str(doc))
    elif c_code == "au":
        doc = re.sub('("\w\w_\w\w)"', '"en_AU"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A39IBJ37TRP1C6"', str(doc))

    return doc


def patch_uk(sku):

    ##############Edit Title###################
    text = ""
    try:
        text = listing.get_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku,
                                         marketplaceIds=['A1F83G8C2ARO7P']).payload['summaries'][0]['itemName']
        print(text)
    except:
        print("not found " + sku)
        return

    ###########################################

    ##############Create Keywords##############
    # keywords = ""
    # if "Oguzhan" in text:
    #     keywords = "Männerschuhe; Herrenmode; lässige Schuhe; zwanglos; natürliches Material; Naturleder; veganes Leder; Orthopädie; anatomisch; Nubuk; Sommerschuhe; Frühlingsschuhe; klassische; Kunstleder; handgefertigte Schuhe"
    #     text = text.replace("Oguzhan Schuhe ", "")
    #     if "(" in text:
    #         text = text.replace("(", "- Oguzhan Schuhe (")
    #     else:
    #         text += " - Oguzhan Schuhe"
    # keywords = keywords.lower()
    # print(text)
    # print(keywords)
    ###########################################

    ###############Send Request################
    with open('patch_demo.json', 'r+') as file:
        data = file.readlines()
    # with open('patch_demo.json', 'w') as file:
    #     try:
    #         data[8] = '\t\t  "value": "'+text+'",\n'
    #         data[8] = data[8].encode('utf', 'ignore').decode('1252')
    #         # data[19] = '\t\t  "value": "'+keywords+'",\n'
    #         # data[19] = data[19].encode('utf', 'ignore').decode('1252')
    #         file.writelines(data)
    #     except:
    #         data[8] = '\t\t  "value": "' + text + '",\n'
    #         data[8] = data[8].encode('1252', 'ignore').decode('1252')
    #         # data[19] = '\t\t  "value": "' + keywords + '",\n'
    #         # data[19] = data[19].encode('1252', 'ignore').decode('1252')
    #         file.writelines(data)

    file = open('patch_demo.json', "r+")
    body = json.load(file)
    # resp = listing.patch_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku, body=body,
    #                                    marketplaceIds=['A1F83G8C2ARO7P'])
    # print(resp)
    file.close()
    ###########################################


# sku_file = open("skus.txt", "r+", encoding="utf-8")
# skus = sku_file.read().splitlines()
# sku_file.close()
#
# counter = 0
# total = str(len(skus))
# for sku in skus:
#     counter += 1
#     print(str(counter)+" out of "+total)
#     patch_uk(sku)
