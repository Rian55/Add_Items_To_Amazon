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

# xdxd = types.get_definitions_product_type(productType="SHOES", marketplaceIds=['A2NODRKZP88ZB9'])
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
    elif c_code == "sv":
        doc = re.sub('("\w\w_\w\w)"', '"sv_SE"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A2NODRKZP88ZB9"', str(doc))
    elif c_code == "nl":
        doc = re.sub('("\w\w_\w\w)"', '"nl_NL"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1805IZSGTT6HS"', str(doc))
    elif c_code == "au":
        doc = re.sub('("\w\w_\w\w)"', '"en_AU"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A39IBJ37TRP1C6"', str(doc))

    return doc


def patch_uk(sku, text):

    ##############Edit Title###################
    try:
        temp = listing.get_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku,
                                         marketplaceIds=['APJ6JRA9NG5V4']).payload['summaries'][0]['itemName']
        # print(text)
    except:
        print("not found " + sku)
        return

    ###########################################

    ##############Create Keywords##############
    # if "Oguzhan" in text:
    #     keywords = "Männerschuhe; Herrenmode; lässige Schuhe; zwanglos; natürliches Material; Naturleder; veganes Leder; Orthopädie; anatomisch; Nubuk; Sommerschuhe; Frühlingsschuhe; klassische; Kunstleder; handgefertigte Schuhe"
    #     text = text.replace("Oguzhan Schuhe ", "")
    #     if "(" in text:
    #         text = text.replace("(", "- Oguzhan Schuhe (")
    #     else:
    #         text += " - Oguzhan Schuhe"
    # keywords = keywords.lower()
    #print(text)
    #print(keywords)
    ###########################################

    ###############Send Request################
    with open('in_kw_patch.json', 'r+', encoding="utf-8") as file:
        data = file.read()
        data = change_marketplace(data, "it")
    with open('in_kw_patch.json', 'w', encoding="utf-8") as file:
        try:
            text = text.encode('utf', 'ignore').decode('utf')
            data = re.sub('item_name",\n\s+"value":\s\[\n\s+{\n\s+"value":\s"(.+)"',
                          'item_name",\n\t  "value": [\n\t\t{\n\t\t  "value": "' + text + '"', data)
            # data[19] = '\t\t  "value": "'+keywords+'",\n'
            # data[19] = data[19].encode('utf', 'ignore').decode('1252')
            file.writelines(data)
        except:
            text = text.encode('1252', 'ignore').decode('1252')
            data = re.sub('item_name",\n\s+"value":\s\[\n\s+{\n\s+"value":\s"(.+)"',
                          'item_name",\n\t  "value": [\n\t\t{\n\t\t  "value": "' + text + '"', data)
            # data[19] = '\t\t  "value": "' + keywords + '",\n'
            # data[19] = data[19].encode('1252', 'ignore').decode('1252')
            file.writelines(data)
        print(text)

    file = open('in_kw_patch.json', "r+", encoding="utf-8")
    body = json.load(file)
    resp = listing.patch_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku, body=body,
                                       marketplaceIds=['APJ6JRA9NG5V4'])
    print(resp)
    file.close()
    ###########################################


sku_file = open("inv_it.txt", "r+", encoding="utf-8")
skus = sku_file.read().splitlines()
sku_file.close()

counter = 0
total = str(len(skus)/3)
for i in range(0, len(skus), 3):
    counter += 1
    print(str(counter)+" out of "+total)
    patch_uk(skus[i], skus[i+1].title())
