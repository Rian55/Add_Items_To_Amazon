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
    # text = text.replace("Confetti ", "")
    # text += " - Confetti"
    ###########################################

    ##############Create Keywords##############
    keywords = ""
    attrib = ""
    if "Kids" in text:
        keywords = "Kids Carpet, Natural Carpet, Natural Rug, Kids Rug, For Kids, Polyamide Rug, Polyamide Carpet, " \
                   "Carpet, Rug, Aesthetic, Home Decoration, Decorative Carpet, Decorative Rug"
        if text.find("Border") < text.find("Kids") and "Border" in text:
            attrib = text[0:text.find(" Border")]
        else:
            attrib = text[0:text.find(" Kids")]

        if "Baby Set" in attrib:
            attrib = attrib[9:len(attrib)]
    else:
        keywords = "Decorative Carpet, Natural Carpet, Natural Rug, Decorative Rug, Decoration, Polyamide Rug, " \
                   "Polyamide Carpet, Carpet, Rug, Aesthetic, Home Decoration"
        if "Florida" in text:
            if "Border" in text:
                attrib = text[8:text.find(" Border")]
            else:
                attrib = text[8:text.find(" Decorative")]
        elif "Colorado" in text:
            attrib = text[9:text.find(" Border")]
        else:
            attrib = text[0:text.find(" Decorative")]

    if attrib != " ":
        keywords += ", " + attrib + " Rug, " + attrib + " Carpet"
    keywords = keywords.replace(",", "")
    keywords = keywords.lower()
    print(text)
    # print(keywords)
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


sku_file = open("uk_rug.txt", "r+")
skus = sku_file.read().splitlines()
sku_file.close()

counter = 0
for sku in skus:
    counter += 1
    print(str(counter)+" out of "+str(len(skus)))
    patch_uk(sku)
