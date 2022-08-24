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
credentials = dict(config['JP'])
# seller id us: ARF5K9J5BZD8E
# seller id au: A1YMU57VS9K367
# seller id eu: A2YSV8HF6GQ3SP
# seller id tr: A3EJANLBKLUQ79
# seller id sg: A2PXFALX8WSFCY
# seller id jp: A91TNPYG4TSAR
listing = ListingsItems(credentials=credentials, marketplace=Marketplaces.SG)
types = ProductTypeDefinitions(credentials=credentials, marketplace=Marketplaces.JP)

# xdxd = types.get_definitions_product_type(productType="RUG", marketplaceIds=['A1VC38T7YXB528'])
# print(xdxd)
xd = types.search_definitions_product_types(marketplaceIds=['A1VC38T7YXB528'])
for i in xd.payload['productTypes']:
    print(i['name'])


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
    elif c_code == "ca":
        doc = re.sub('("\w\w_\w\w)"', '"en_CA"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A2EUQ1WTGCTBG2"', str(doc))
    elif c_code == "mx":
        doc = re.sub('("\w\w_\w\w)"', '"es_MX"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1AM78C64UM0Y8"', str(doc))
    elif c_code == "tr":
        doc = re.sub('("\w\w_\w\w)"', '"tr_TR"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A33AVAJ2PDY3EV"', str(doc))
    elif c_code == "sg":
        doc = re.sub('("\w\w_\w\w)"', '"en_SG"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A19VAU5U5O7RUS"', str(doc))
    elif c_code == "jp":
        doc = re.sub('("\w\w_\w\w)"', '"jp_JP"', str(doc))
        doc = re.sub('("marketplace_id": "\w+")', '"marketplace_id": "A1VC38T7YXB528"', str(doc))

    return doc


def patch_uk(sku, mktplc_id, f_name):

    ##############Check Item###################
    text = ""
    try:
        text = listing.get_listings_item(sellerId='A2PXFALX8WSFCY', sku=sku,
                                         marketplaceIds=[mktplc_id]).payload['summaries'][0]['itemName']

        # print(text)
    except:
        print("not found " + sku)
        return
    ###########################################

    ##############Edit Attributes##############
    text = text.replace(" Please message for size information", "")
    text = text.replace(" -", "")
    text = text.replace(" –", "")
    text = text.replace('"', "'")
    text = text.replace(',', "")
    text = text.replace('.', "")
    text = text.replace("eworldpartner ", "")
    text = text.replace("eworldpartner", "")
    text = text.replace("eWorldPartner ", "")
    text = text.replace("EWP ", "")
    text = text.replace("Ewp ", "")
    if "Suds Enjoy" in text:
        text = text.replace("Suds Enjoy ", "")
        text += " - Suds Enjoy"
    elif "Oguzhan Shoes" in text:
        text = text.replace("Oguzhan Shoes ", "")
        if "(" in text:
            text = text.replace("(", "- Oguzhan Shoes (")
        else:
            text += " - Oguzhan Shoes"
    elif "Dermokil" in text:
        text = text.replace("Dermokil ", "")
        text += " - Dermokil"
    elif "Ruel Design" in text:
        text = text.replace("Ruel Design ", "")
        text += " - Ruel Design"
    elif "Akinalbella" in text:
        text = text.replace("Akinalbella ", "")
        text += " - Akinalbella"
    elif "Muslin" in text:
        if "Muslin & Towel" in text:
            text = text.replace("Muslin & Towel ", "")
        else:
            text = text.replace("Muslin ", "")
        text += " - Muslin & Towel"
    elif "Müslin" in text:
        text = text.replace("Müslin ", "")
        text += " - Müslin"
    elif "Latife" in text:
        text = text.replace("Latife ", "")
        text += " - Latife"
    elif "Halil Onat" in text:
        text = text.replace("Halil Onat ", "")
        text += " - Halil Onat"
    elif "Homm Life" in text:
        text = text.replace("Homm Life ", "")
        text += " - Homm Life"
    elif "Iva Natura" in text:
        text = text.replace("Iva Natura ", "")
        text += " - Iva Natura"
    elif "Kutahya" in text:
        text = text.replace("Kutahya Porcelain ", "")
        text = text.replace(" de porcelana Kutahya", "")
        text = text.replace(" Kutahya Porcelain", "")
        text = text.replace("Kutahya ", "")
        text += " - Kutahya Porcelain"
    elif "Kutahya Porselen" in text:
        text = text.replace("Kutahya Porselen ", "")
        text += " - Kutahya Porcelain"
    elif "Sakin Leather Goods" in text:
        text = text.replace("Sakin Leather Goods ", "")
        text += " - Sakin Leather Goods"
    elif "Pasabahce" in text:
        text = text.replace("Pasabahce ", "")
        text += " - Pasabahce"
    elif "Confetti" in text or "Confeti" in text or "confeti" in text:
        text = text.replace("Confetti ", "")
        text = text.replace("Confeti ", "")
        text = text.replace(" de confeti", "")
        text += " - Confetti"
    elif "Pufai" in text:
        text = text.replace("Pufai ", "")
        text += " - Pufai"
    elif "Doxa" in text:
        text = text.replace("Doxa ", "")
        text += " - Doxa"

    text = text.title()

    with open(f_name, 'r+', encoding="utf-8") as file:
        data = file.read()
    with open(f_name, 'w', encoding="utf-8") as file:
        try:
            text = text.encode('utf', 'ignore').decode('utf')
            data = re.sub('item_name",\n\s+"value":\s\[\n\s+{\n\s+"value":\s"(.+)"',
                          'item_name",\n\t  "value": [\n\t\t{\n\t\t  "value": "' + text + '"', data)
            file.writelines(data)
        except:
            text = text.encode('1252', 'ignore').decode('1252')
            data = re.sub('item_name",\n\s+"value":\s\[\n\s+{\n\s+"value":\s"(.+)"',
                          'item_name",\n\t  "value": [\n\t\t{\n\t\t  "value": "' + text + '"', data)
            file.writelines(data)
        print(text)
    ###########################################

    ###############Send Request################
    file = open(f_name, "r+", encoding="utf-8")
    body = json.load(file)
    resp = listing.patch_listings_item(sellerId='A2PXFALX8WSFCY', sku=sku, body=body,
                                       marketplaceIds=[mktplc_id])
    print(resp)
    file.close()
    ###########################################


def select_mktplc(ctry_code, f_name):
    with open("skus.txt", "r+", encoding="utf-8") as sku_file:
        skus = sku_file.read().splitlines()

    with open(f_name, 'r+', encoding="utf-8") as file:
        data = file.read()
        if ctry_code == "gb" or ctry_code == "au" or ctry_code == "us" or ctry_code == "ca" or ctry_code == "sg":
            data = change_marketplace(data, ctry_code, "en")
        elif ctry_code == "mx":
            data = change_marketplace(data, ctry_code, "es")
        else:
            data = change_marketplace(data, ctry_code, ctry_code)

    with open(f_name, 'w', encoding="utf-8") as file:
        file.writelines(data)

    return skus


# file_name = "in_kw_patch.json"
# skus = select_mktplc("sg", file_name)
# counter = 0
# total = str(len(skus))
# for i in range(0, len(skus)):
#     counter += 1
#     print(str(counter)+" out of "+total)
#     patch_uk(skus[i], Marketplaces.SG.marketplace_id, file_name)
