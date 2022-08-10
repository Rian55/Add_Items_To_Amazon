import json
from configparser import ConfigParser
from sp_api.base import Marketplaces
from sp_api.api import ListingsItems
from sp_api.api import ProductTypeDefinitions
from sp_api.api import Inventories

config = ConfigParser()
config.read(".config.txt")
credentials = dict(config['default'])
listing = ListingsItems(credentials=credentials, marketplace=Marketplaces.UK)
listing_us = ListingsItems(credentials=credentials, marketplace=Marketplaces.US)
types = ProductTypeDefinitions(credentials=credentials, marketplace=Marketplaces.UK)
inventories = Inventories(credentials=credentials, marketplace=Marketplaces.UK)
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
    text = text.replace("eWorldPartner ", "")
    text = text.replace("eworldpartner ", "")
    text = text.replace("EWP ", "")
    text = text.replace("Ewp ", "")
    if "Suds Enjoy" in text:
        text = text.replace("Suds Enjoy ", "")
        text += " - Suds Enjoy"
    elif "Dermokil" in text:
        text = text.replace("Dermokil ", "")
        text += " - Dermokil"
    elif "Ruel Design" in text:
        text = text.replace("Ruel Design ", "")
        text += " - Ruel Design"
    elif "Akinalbella" in text:
        text = text.replace("Akinalbella ", "")
        text += " - Akinalbella"
    elif "Muslin & Towel" in text:
        text = text.replace("Muslin & Towel ", "")
        text += " - Muslin & Towel"
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
    elif "Kutahya Porcelain" in text:
        text = text.replace("Kutahya Porcelain ", "")
        text += " - Kutahya Porcelain"
    elif "Sakin Leather Goods" in text:
        text = text.replace("Sakin Leather Goods ", "")
        text += " - Sakin Leather Goods"
    ###########################################

    ##############Create Keywords##############
    # keywords = ""
    # attrib = ""
    # if "Kids" in text:
    #     keywords = "Kids Carpet, Natural Carpet, Natural Rug, Kids Rug, For Kids, Polyamide Rug, Polyamide Carpet, " \
    #                "Carpet, Rug, Aesthetic, Home Decoration, Decorative Carpet, Decorative Rug"
    #     if text.find("Border") < text.find("Kids") and "Border" in text:
    #         attrib = text[0:text.find(" Border")]
    #     else:
    #         attrib = text[0:text.find(" Kids")]
    #
    #     if "Baby Set" in attrib:
    #         attrib = attrib[9:len(attrib)]
    # else:
    #     keywords = "Decorative Carpet, Natural Carpet, Natural Rug, Decorative Rug, Decoration, Polyamide Rug, " \
    #                "Polyamide Carpet, Carpet, Rug, Aesthetic, Home Decoration"
    #     if "Florida" in text:
    #         if "Border" in text:
    #             attrib = text[8:text.find(" Border")]
    #         else:
    #             attrib = text[8:text.find(" Decorative")]
    #     elif "Colorado" in text:
    #         attrib = text[9:text.find(" Border")]
    #     else:
    #         attrib = text[0:text.find(" Decorative")]
    #
    # if attrib != " ":
    #     keywords += ", " + attrib + " Rug, " + attrib + " Carpet"
    # keywords = keywords.replace(",", "")
    # keywords = keywords.lower()
    print(text)
    # print(keywords)
    ###########################################
    with open('patch_demo.json', 'r') as file:
        data = file.readlines()
    with open('patch_demo.json', 'w') as file:
        data[8] = f'\t\t  "value": "{text}",\n'
        # data[50] = f'\t\t  "value": "{keywords}",\n'
        file.writelines(data)

    file = open('patch_demo.json', "r+")
    body = json.load(file)
    # print(body)
    resp = listing.patch_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku, body=body,
                                       marketplaceIds=['A1F83G8C2ARO7P'])
    print(resp)
    file.close()


sku_file = open("uk_mixed.txt", "r+")
skus = sku_file.read().splitlines()
sku_file.close()

counter = 0
for sku in skus:
    counter += 1
    print(str(counter)+" out of "+str(len(skus)))
    patch_uk(sku)



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
#     {
#       "op":"replace",
#       "path":"/attributes/generic_keyword",
#       "value":[
#         {
# 		  "value": "decorative carpet natural carpet natural rug decorative rug decoration polyamide rug polyamide carpet carpet rug aesthetic home decoration  rug  carpet",
#           "language_tag": "en_GB",
#           "marketplace_id": "A1F83G8C2ARO7P"
#         }
#       ]
#     }
#   ]
# }