import json
from configparser import ConfigParser
from sp_api.base import Marketplaces
from sp_api.api import ListingsItems
from sp_api.api import ProductTypeDefinitions
import re
import ean13
from googletrans import Translator
import csv

trans = Translator()
ups_codes = {
    "0": [Marketplaces.TR],
    "1": [Marketplaces.DE],
    "2": [Marketplaces.IT, Marketplaces.UK, Marketplaces.FR, Marketplaces.ES, Marketplaces.NL],
    "3": [Marketplaces.PL, Marketplaces.SE],
    "4": [],
    "5": [Marketplaces.MX, Marketplaces.CA, Marketplaces.US],
    "6": [Marketplaces.SG],
    "7": [Marketplaces.AU],
    "8": [Marketplaces.AE, Marketplaces.JP]
}


def get_attributes(product_type="", mktplc=Marketplaces.UK):
    credentials, s_id = get_creds(mktplc=mktplc)
    types = ProductTypeDefinitions(credentials=credentials, marketplace=mktplc)

    if product_type == "":
        xd = types.search_definitions_product_types(marketplaceIds=[mktplc.marketplace_id])
        count = 0
        for i in xd.payload['productTypes']:
            count += 1
            print(str(count) + " " + i['name'])
        choice = input()

    # xdxd = types.get_definitions_product_type(productType=product_type, marketplaceIds=[mktplc.marketplace_id])
    # print(xdxd)
    # attributes = []
    # for i in xdxd.payload['propertyGroups']:
    #     prop_names = xdxd.payload['propertyGroups'][i]['propertyNames']
    #     for name in prop_names:
    #         attributes.append(name)
    #
    # for i in attributes:
    #     print(i)


def get_creds(mktplc):
    config = ConfigParser()
    config.read(".config.txt")
    if mktplc == Marketplaces.US or mktplc == Marketplaces.MX or mktplc == Marketplaces.CA:
        return dict(config['US']), dict(config['MID_US'])['id']
    elif mktplc == Marketplaces.AU:
        return dict(config['AU']), dict(config['MID_AU'])['id']
    elif mktplc == Marketplaces.JP:
        return dict(config['JP']), dict(config['MID_JP'])['id']
    elif mktplc == Marketplaces.TR:
        return dict(config['TR']), dict(config['MID_TR'])['id']
    elif mktplc == Marketplaces.SG:
        return dict(config['SG']), dict(config['MID_SG'])['id']
    else:
        return dict(config['EU']), dict(config['MID_EU'])['id']


def change_marketplace(doc, mktplc):
    t_code = ""

    if mktplc == Marketplaces.UK:
        doc = re.sub('("\w\w_\w\w)"', '"en_GB"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1F83G8C2ARO7P"', str(doc))
        t_code = "en"
    elif mktplc == Marketplaces.US:
        doc = re.sub('("\w\w_\w\w)"', '"en_US"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "ATVPDKIKX0DER"', str(doc))
        t_code = "en"
    elif mktplc == Marketplaces.DE:
        doc = re.sub('("\w\w_\w\w)"', '"de_DE"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1PA6795UKMFR9"', str(doc))
        t_code = "de"
    elif mktplc == Marketplaces.FR:
        doc = re.sub('("\w\w_\w\w)"', '"fr_FR"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A13V1IB3VIYZZH"', str(doc))
        t_code = "fr"
    elif mktplc == Marketplaces.IT:
        doc = re.sub('("\w\w_\w\w)"', '"it_IT"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "APJ6JRA9NG5V4"', str(doc))
        t_code = "it"
    elif mktplc == Marketplaces.ES:
        doc = re.sub('("\w\w_\w\w)"', '"es_ES"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1RKKUPIHCS9HS"', str(doc))
        t_code = "es"
    elif mktplc == Marketplaces.PL:
        doc = re.sub('("\w\w_\w\w)"', '"pl_PL"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1C3SOZRARQ6R3"', str(doc))
        t_code = "pl"
    elif mktplc == Marketplaces.SE:
        doc = re.sub('("\w\w_\w\w)"', '"sv_SE"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A2NODRKZP88ZB9"', str(doc))
        t_code = "sv"
    elif mktplc == Marketplaces.NL:
        doc = re.sub('("\w\w_\w\w)"', '"nl_NL"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1805IZSGTT6HS"', str(doc))
        t_code = "nl"
    elif mktplc == Marketplaces.AU:
        doc = re.sub('("\w\w_\w\w)"', '"en_AU"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A39IBJ37TRP1C6"', str(doc))
        t_code = "en"
    elif mktplc == Marketplaces.CA:
        doc = re.sub('("\w\w_\w\w)"', '"en_CA"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A2EUQ1WTGCTBG2"', str(doc))
        t_code = "en"
    elif mktplc == Marketplaces.MX:
        doc = re.sub('("\w\w_\w\w)"', '"es_MX"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1AM78C64UM0Y8"', str(doc))
        t_code = "es"
    elif mktplc == Marketplaces.TR:
        doc = re.sub('("\w\w_\w\w)"', '"tr_TR"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A33AVAJ2PDY3EV"', str(doc))
        t_code = "tr"
    elif mktplc == Marketplaces.SG:
        doc = re.sub('("\w\w_\w\w)"', '"en_SG"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A19VAU5U5O7RUS"', str(doc))
        t_code = "en"
    elif mktplc == Marketplaces.JP:
        doc = re.sub('("\w\w_\w\w)"', '"ja_JP"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1VC38T7YXB528"', str(doc))
        t_code = "ja"

    for x in re.finditer(': "(.+)",\n\s+"language_tag"', doc):
        translatable = x.group()[3:x.group().find('"', 4)]
        translated = trans.translate(translatable.lower(), dest=t_code)
        doc = re.sub(translatable, translated.text.title(), doc)

    return doc


def patch_uk(sku, mktplc, f_name):
    credentials, s_id = get_creds(mktplc)
    listing = ListingsItems(credentials=credentials, marketplace=mktplc)

    ##############Check Item###################
    try:
        text = listing.get_listings_item(sellerId=s_id, sku=sku,
                                         marketplaceIds=[mktplc.marketplace_id]).payload['summaries'][0]['itemName']
        # print(text)
    except:
        print("not found " + sku)
        return
    ###########################################

    ##############Edit Attributes##############
    # with open(f_name, 'r+', encoding="utf-8") as file:
    #     data = file.read()
    # with open(f_name, 'w', encoding="utf-8") as file:
    #     try:
    #         text = text.encode('utf', 'ignore').decode('utf')
    #         data = re.sub('item_name",\n\s+"value":\s\[\n\s+{\n\s+"value":\s"(.+)"',
    #                       'item_name",\n\t  "value": [\n\t\t{\n\t\t  "value": "' + text + '"', data)
    #         file.writelines(data)
    #     except:
    #         text = text.encode('1252', 'ignore').decode('1252')
    #         data = re.sub('item_name",\n\s+"value":\s\[\n\s+{\n\s+"value":\s"(.+)"',
    #                       'item_name",\n\t  "value": [\n\t\t{\n\t\t  "value": "' + text + '"', data)
    #         file.writelines(data)
    #     print(text)
    ###########################################

    ###############Send Request################
    file = open(f_name, "r+", encoding="utf-8")
    body = json.load(file)
    # resp = listing.patch_listings_item(sellerId=s_id, sku=sku, body=body,
    #                                    marketplaceIds=[mktplc.marketplace_id])
    # print(resp)
    file.close()
    ###########################################


def add_item_uk(mktplc, f_name):
    with open('saturn_cer.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
    credentials, s_id = get_creds(mktplc)
    listing = ListingsItems(credentials=credentials, marketplace=mktplc)
    # for row in reader:
    #     print(row)

    file = open('scer_fpot_add.json', "r+")
    body = json.load(file)
    count = 0
    sku = "SCER-FPOT-" + str(count)
    resp = listing.put_listings_item(sellerId=s_id, sku='EWP-SATURN-CER-2', body=body,
                                     marketplaceIds=[mktplc])
    print(resp)
    file.close()


color_var = {
    "1": ["multicolor", "patterned"],
    "2": ["multicolor", "patterned"],
    "3": ["yellow", "dotted"],
    "4": ["white and gray", "striped"],
    "5": ["red", "striped"],
    "6": ["black and white", "striped"],
    "7": ["light blue and white", "striped"],
    "8": ["black", "striped"],
    "9": ["black and grey", "striped"],
    "10": ["white and grey", "striped"],
    "11": ["brown", "striped"],
    "12": ["white", "patterned"],
    "13": ["white", "patterned"],
    "14": ["green and beige", "striped"],
    "15": ["grey and white", "striped"],
    "16": ["black", "patterned"],
    "17": ["black", "patterned"],
    "18": ["multicolor", "patterned"],
    "19": ["multicolor", "patterned"],
    "20": ["white", "patterned"],
    "21": ["green and beige", "striped"],
    "22": ["black", "striped"],
    "23": ["black and white", "striped"],
    "24": ["grey and black", "striped"],
    "25": ["white and black", "striped"],
    "26": ["black and grey", "striped"],
    "27": ["multicolor", "patterned"],
    "28": ["multicolor", "patterned"],
    "29": ["beige", "striped"],
    "30": ["multicolor", "patterned"]
}

# get_attributes()
