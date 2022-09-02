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

    if t_code != "en":
        for x in re.finditer(': "(.+)",\n\s+"language_tag"', doc):
            translatable = x.group()[3:x.group().find('"', 4)]
            translated = ""
            if " - " in translatable:
                title = translatable.split(" - ")
                f_title = trans.translate(title[0].lower(), dest=t_code)
                translated = f_title.text + " - " + title[1]
            else:
                translated = trans.translate(translatable.lower(), dest=t_code).text
            # print(translated)
            # print(translatable)
            doc = re.sub(translatable, translated.title(), doc)

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

    with open('saturn_cer_sets.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        random = 564539853490
        count = 0
        for row in reader:
            sizes = []
            for x in row['size'].split('-'):
                sizes.append(x.split("x"))
            product = row['num']
            item_count = int(row['items'])
            pattern = row['pattern']
            prices = []
            for i in range(9):
                prices.append(row[str(i)])
            #############Edit Attributes#############
            with open(f_name, "r+", encoding="utf-8") as file:
                body = json.load(file)

            count += 1

            ipd_x, ipd_y, ipd_z, max_x, max_y, max_z = 0, 0, 0, 0, 0, 0
            for i in range(item_count):
                ipd_x += int(sizes[i][0])
                ipd_y += int(sizes[i][1])
                ipd_z += int(sizes[i][2])
                if int(sizes[i][0]) > max_x:
                    max_x = int(sizes[i][0])
                if int(sizes[i][1]) > max_y:
                    max_y = int(sizes[i][1])
                if int(sizes[i][2]) > max_z:
                    max_z = int(sizes[i][2])

            body['attributes']['item_package_dimensions'][0]['length']['value'] = ipd_x + 2
            body['attributes']['item_package_dimensions'][0]['width']['value'] = ipd_y + 2
            body['attributes']['item_package_dimensions'][0]['height']['value'] = ipd_z + 2
            body['attributes']['item_dimensions'][0]['height']['value'] = max_x
            body['attributes']['item_dimensions'][0]['width']['value'] = max_y
            body['attributes']['item_dimensions'][0]['length']['value'] = max_z
            body['attributes']['item_depth_width_height'][0]['height']['value'] = max_z
            body['attributes']['item_depth_width_height'][0]['width']['value'] = max_x
            body['attributes']['item_depth_width_height'][0]['depth']['value'] = max_z-1

            title = f"Modern Handmade Special Design {pattern} Ceramic Flowerpot Set of {item_count} - Saturn Ceramic"
            body['attributes']['item_name'][0]['value'] = title.title()
            size_line = ""
            for i in range(item_count):
                size_line += sizes[i][0]+"x"+sizes[i][1]+"x"+sizes[i][2]+" cm"
                if i != item_count-2:
                    size_line += " and "
                elif i != item_count-1:
                    size_line = size_line
                else:
                    size_line += ", "
            body['attributes']['product_description'][0]['value'] = f"The dimensions of the pots are 15x15x13 cm and 20x20x18 cm respectively.They are natural earthen pots.\nThere are holes at the bottom of the pots of ceramics to prevent moisture, but there is no pot base.\nIt is 100% handmade.There may be slight differences in the same models as they are handmade.\nThey are products that will attract attention in any environment with their stylish designs, sizes and vivid colors.\nThey are special products that you can use in home or office decoration and gift to your loved ones.\nIt is recommended to wipe with a damp cloth for cleaning."
            body['attributes']['externally_assigned_product_identifier'][0]['value'] = ean13.calculate_ean(random)
            body['attributes']['number_of_items'][0]['value'] = item_count
            body['attributes']['capacity'][0]['value'] = float("%.1f" % (max_z*max_x*max_y/1000))

            img_id = "SCER-FSET-"
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
            print(json.dumps(body, sort_keys=False, indent=2))

            sku = "SCER-FSET-"
            for i in range(3 - len(str(count))):
                sku += "0"
            sku += str(count)
            print(sku)
            # resp = listing.put_listings_item(sellerId=s_id, sku=sku, body=body,
            #                                  marketplaceIds=[mktplc.marketplace_id], issueLocale="en_US")
            # print(resp)
            #########################################
            random += 1


add_item_uk(Marketplaces.UK, "scer_fpot_add.json")
# get_attributes("PLANTER", Marketplaces.US)
