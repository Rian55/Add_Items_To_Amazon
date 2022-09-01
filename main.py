import json
from configparser import ConfigParser
from sp_api.base import Marketplaces
from sp_api.api import ListingsItems
from sp_api.api import ProductTypeDefinitions
import re
from forex_python.converter import CurrencyRates
import ean13
from googletrans import Translator
import csv

trans = Translator()
CURR_RATES = CurrencyRates()
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
        product_type = xd.payload['productTypes'][int(choice)-1]['name']

    xdxd = types.get_definitions_product_type(productType=product_type, marketplaceIds=[mktplc.marketplace_id])
    print(xdxd)
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
    config.read("./.config.txt")
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


def change_price_details(doc, currency):
    doc = re.sub('("currency": "\w+")', '"currency": "'+currency+'"', str(doc))
    if currency != "USD":
        price = re.search('"value_with_tax": \d+.\d+', doc).group()
        price = price[price.find(": ") + 2:len(price)]
        new_price = float(price) * CURR_RATES.get_rate('USD', currency) * 1.01
        doc = re.sub('("value_with_tax": \d+.\d+)', '"value_with_tax": ' + str("{:.2f}".format(new_price)), str(doc))
    return doc


def change_marketplace(fname, mktplc):
    t_code = ""
    with open(fname, "r", encoding="utf-8") as file:
        doc = file.read()

    if mktplc == Marketplaces.UK:
        doc = re.sub('("\w\w_\w\w)"', '"en_GB"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1F83G8C2ARO7P"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "GBP")
        t_code = "en"
    elif mktplc == Marketplaces.US:
        doc = re.sub('("\w\w_\w\w)"', '"en_US"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "ATVPDKIKX0DER"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "USD")
        t_code = "en"
    elif mktplc == Marketplaces.DE:
        doc = re.sub('("\w\w_\w\w)"', '"de_DE"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1PA6795UKMFR9"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "EUR")
        t_code = "de"
    elif mktplc == Marketplaces.FR:
        doc = re.sub('("\w\w_\w\w)"', '"fr_FR"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A13V1IB3VIYZZH"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "EUR")
        t_code = "fr"
    elif mktplc == Marketplaces.IT:
        doc = re.sub('("\w\w_\w\w)"', '"it_IT"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "APJ6JRA9NG5V4"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "EUR")
        t_code = "it"
    elif mktplc == Marketplaces.ES:
        doc = re.sub('("\w\w_\w\w)"', '"es_ES"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1RKKUPIHCS9HS"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "EUR")
        t_code = "es"
    elif mktplc == Marketplaces.PL:
        doc = re.sub('("\w\w_\w\w)"', '"pl_PL"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1C3SOZRARQ6R3"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "PLN")
        t_code = "pl"
    elif mktplc == Marketplaces.SE:
        doc = re.sub('("\w\w_\w\w)"', '"sv_SE"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A2NODRKZP88ZB9"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "SEK")
        t_code = "sv"
    elif mktplc == Marketplaces.NL:
        doc = re.sub('("\w\w_\w\w)"', '"nl_NL"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1805IZSGTT6HS"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "EUR")
        t_code = "nl"
    elif mktplc == Marketplaces.AU:
        doc = re.sub('("\w\w_\w\w)"', '"en_AU"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A39IBJ37TRP1C6"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "AUD")
        t_code = "en"
    elif mktplc == Marketplaces.CA:
        doc = re.sub('("\w\w_\w\w)"', '"en_CA"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A2EUQ1WTGCTBG2"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "CAD")
        t_code = "en"
    elif mktplc == Marketplaces.MX:
        doc = re.sub('("\w\w_\w\w)"', '"es_MX"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1AM78C64UM0Y8"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "MXN")
        t_code = "es"
    elif mktplc == Marketplaces.TR:
        doc = re.sub('("\w\w_\w\w)"', '"tr_TR"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A33AVAJ2PDY3EV"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "TRY")
        t_code = "tr"
    elif mktplc == Marketplaces.SG:
        doc = re.sub('("\w\w_\w\w)"', '"en_SG"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A19VAU5U5O7RUS"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "SGD")
        t_code = "en"
    elif mktplc == Marketplaces.JP:
        doc = re.sub('("\w\w_\w\w)"', '"ja_JP"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1VC38T7YXB528"', str(doc))
        if '"currency":' in doc:
            doc = change_price_details(doc, "JPY")
        t_code = "ja"

    for x in re.finditer(': "(.+)",\n\s+"language_tag"', doc):
        translatable = x.group()[3:x.group().find('"', 4)]
        translated = trans.translate(translatable.lower(), dest=t_code)
        doc = re.sub(translatable, translated.text.title(), doc)

    # print(doc)
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
    credentials, s_id = get_creds(mktplc)
    listing = ListingsItems(credentials=credentials, marketplace=mktplc)

    with open('saturn_cer.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        random = 437283420938
        count = 0
        for row in reader:
            size = row['size'].split('x')
            products = row['num'].split("-")
            prices = []
            for i in range(9):
                prices.append(row[str(i)])
            for product in products:
                #############Edit Attributes#############
                with open(f_name, "r+", encoding="utf-8") as file:
                    body = json.load(file)

                count += 1

                body['attributes']['item_package_dimensions'][0]['length']['value'] = int(size[0]) + 2
                body['attributes']['item_package_dimensions'][0]['width']['value'] = int(size[0]) + 2
                body['attributes']['item_package_dimensions'][0]['height']['value'] = int(size[0]) + 2
                body['attributes']['item_dimensions'][0]['height']['value'] = int(size[2])
                body['attributes']['item_dimensions'][0]['width']['value'] = int(size[1])
                body['attributes']['item_dimensions'][0]['length']['value'] = int(size[0])
                body['attributes']['item_depth_width_height'][0]['height']['value'] = int(size[2])
                body['attributes']['item_depth_width_height'][0]['width']['value'] = int(size[1])
                body['attributes']['item_depth_width_height'][0]['depth']['value'] = int(size[2])-1

                title = f"Modern Handmade Special Design {color_var[product][1]} {color_var[product][0]} Ceramic Flowerpot {size[0]}*{size[1]}*{size[2]} - Saturn Ceramic"
                body['attributes']['item_name'][0]['value'] = title.title()
                body['attributes']['product_description'][0]['value'] = f"{size[0]} x {size[1]} x {size[2]} cm.\n It is a natural flowerpot.\n There are holes at the bottom of the pots to prevent moisture. There is no pot plate.\n Since it is produced and colored completely handmade, there may be slight changes.\n It is a product that will attract attention in any environment with its stylish design, size and vivid colors.\n It is a special product that you can use in home or office decoration and gift to your loved ones.\n It is recommended to wipe with a damp cloth."
                body['attributes']['externally_assigned_product_identifier'][0]['value'] = ean13.calculate_ean(random)

                img_id = "SCER-FPOT-"
                for i in range(3-len(product)):
                    img_id += "0"
                img_id += product
                body['attributes']['main_product_image_locator'][0]['media_location'] = f"https://seller-central-storage.s3.eu-central-1.amazonaws.com/{img_id}.jpg"

                for i in ups_codes:
                    if mktplc in ups_codes[i]:
                        body['attributes']['list_price'][0]['value_with_tax'] = float(prices[int(i)])
                        body['attributes']['purchasable_offer'][0]['our_price'][0]['schedule'][0]['value_with_tax'] = float(prices[int(i)])

                with open('scer_fpot_add.json', "w", encoding="utf-8") as file:
                    file.write(json.dumps(body, sort_keys=False, indent=2))

                body = json.loads(change_marketplace(f_name, mktplc))
                # print(json.dumps(body, sort_keys=False, indent=2))

                sku = "SCER-FPOT-"
                for i in range(3 - len(str(count))):
                    sku += "0"
                sku += str(count)
                print(sku)
                # resp = listing.put_listings_item(sellerId=s_id, sku=sku, body=body,
                #                                  marketplaceIds=[mktplc.marketplace_id])
                # print(resp)
                #########################################
                random += 1


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

add_item_uk(Marketplaces.AU, "scer_fpot_add.json")
