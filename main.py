import json
from configparser import ConfigParser
from sp_api.base import Marketplaces
from sp_api.api import ListingsItems
from sp_api.api import ProductTypeDefinitions
import re
from googletrans import Translator

trans = Translator()
config = ConfigParser()
config.read(".config.txt")
credentials = dict(config['default'])
listing = ListingsItems(credentials=credentials, marketplace=Marketplaces.UK)
listing_us = ListingsItems(credentials=credentials, marketplace=Marketplaces.US)
types = ProductTypeDefinitions(credentials=credentials, marketplace=Marketplaces.UK)

# xdxd = types.get_definitions_product_type(productType="RUG", marketplaceIds=['A1F83G8C2ARO7P'])
# print(xdxd)
# xd = types.search_definitions_product_types(marketplaceIds=['A1F83G8C2ARO7P'])
# for i in xd.payload['productTypes']:
#     print(i['name'])


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

def change_marketplace(doc, c_code, t_code):
    if t_code:
        for x in re.finditer(': "(.+)",\n\s+"language_tag"', doc):
            translatable = x.group()[3:x.group().find('"', 4)]
            translated = trans.translate(translatable.lower(), dest=t_code)
            doc = re.sub(translatable, translated.text.title(), doc)

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


def patch_uk(sku, mktplc_id, f_name):

    ##############Check Item###################
    text = ""
    try:
        text = listing.get_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku,
                                         marketplaceIds=[mktplc_id]).payload['summaries'][0]['itemName']

        # print(text)
    except:
        print("not found " + sku)
        return
    ###########################################

    ##############Edit Attributes##############
    # text = text.replace("eworldpartner ", "")
    # color = re.search(" (\w+) - ", text)
    # if color:
    #     color = color.group()
    #     color = color[1:len(color)-3]
    # else:
    #     color = ""
    #
    # with open(f_name, 'r+', encoding="utf-8") as file:
    #     data = file.read()
    # with open(f_name, 'w', encoding="utf-8") as file:
    #     try:
    #         text = text.encode('utf', 'ignore').decode('utf')
    #         data = re.sub('color",\n\s+"value":\s\[\n\s+{\n\s+"value":\s"(.+)"',
    #                       'color",\n\t  "value": [\n\t\t{\n\t\t  "value": "' + color.title() + '"', data)
    #         file.writelines(data)
    #     except:
    #         text = text.encode('1252', 'ignore').decode('1252')
    #         data = re.sub('color",\n\s+"value":\s\[\n\s+{\n\s+"value":\s"(.+)"',
    #                       'color",\n\t  "value": [\n\t\t{\n\t\t  "value": "' + color.title() + '"', data)
    #         file.writelines(data)
    #     print(text)
    ###########################################

    ###############Send Request################
    file = open(f_name, "r+", encoding="utf-8")
    body = json.load(file)
    resp = listing.patch_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku, body=body,
                                       marketplaceIds=[mktplc_id])
    print(resp)
    file.close()
    ###########################################


def select_mktplc(ctry_code, f_name):
    with open("skus.txt", "r+", encoding="utf-8") as sku_file:
        skus = sku_file.read().splitlines()

    with open(f_name, 'r+', encoding="utf-8") as file:
        data = file.read()
        if ctry_code == "gb" or ctry_code == "au" or ctry_code == "us":
            data = change_marketplace(data, ctry_code, "en")
        else:
            data = change_marketplace(data, ctry_code, ctry_code)

    with open(f_name, 'w', encoding="utf-8") as file:
        file.writelines(data)

    return skus


file_name = "in_kw_patch.json"
skus = select_mktplc("sv", file_name)
counter = 0
total = str(len(skus))
for i in range(0, len(skus)):
    counter += 1
    print(str(counter)+" out of "+total)
    patch_uk(skus[i], Marketplaces.SE.marketplace_id, file_name)
