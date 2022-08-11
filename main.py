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
    inventory_file = open("inv_uk.txt", "a+")
    text = ""
    try:
        text = listing.get_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku,
                                        marketplaceIds=['A1F83G8C2ARO7P']).payload['summaries'][0]['itemName']
    except:
        print("******************Not Found*********************")
    ##############Edit Title###################
    text = text.replace("eworldpartner ", "")
    ###########################################

    ##############Create Keywords##############
    keywords = ""
    if "Suds Enjoy" in text:
        if "Bath Bomb" in text:
            keywords = "bath care, bath bomb, bath bomb set, personal care, fragrances, bath ball, bathroom, bodycare, natural, natural oil"
    elif "Ruel Design" in text:
        keywords = "ruel design, designer, silver, accessory, ruby, emerald, gold, ring, luxury, jewelry, diamond, gemstone, sapphire, women, lux, fashion, rich lifestyle"
    elif "Muslin & Towel" in text:
        keywords = "kid, baby, toddler, poncho, bath, beach, organic, cotton, muslin, fabric, towel, organic fabric, baby clothes"
    elif "Latife" in text:
        if "Brush" in text:
            keywords = "personal care, daily, natural, brush, health, skin, skincare, body, bodycare"
        elif "Cream" in text:
            keywords = "personal care, daily, natural, cream, argan oil, natural, moisturizer, health, skin, skincare, body, bodycare"
        elif "Soap" in text:
            keywords = "latife, natural, rice, handmade, soap, organic, body, daily, personal care"
    elif "Ethnic Pattern" in text:
        keywords = "zipper closure, cotton, beach, summer season, women accessories, mother, baby, beach bag"
    elif "Halil Onat" in text:
        keywords = "handmade, ceramic, vase, decoration, home, flowers, home accessory"
    elif "Homm Life" in text:
        keywords = "homm life, daily, organic, face, body, moisturizing, cream, skincare, scrub, oil, personal care, skin, acne"
    elif "Iva Natura" in text:
        if "Tonic" in text:
            keywords = "iva natura, daily, organic, vegan, face, tonic, refreshing, skincare, personal care, skin"
        elif "Cream" in text:
            keywords = "iva natura, daily, organic, vegan, face, antiaging, cream, skincare, personal care, skin, body, hands, moisturizing"
    elif "Kutahya Porcelain" in text:
        keywords = "dinnerware, set, dishes, kutahya porcelain, porcelain, ceramic, plate, decorative, dinner service, dinner, supper, lunch, breakfast"
    elif "Sakin Leather Goods" in text:
        keywords = "leather, purse, wallet, man wallet, men accessories, vegan leather, natural leather, cardholder"
    elif "No Installation Required Battery Led Flut" in text:
        keywords = "lamp, illumination, decoration, home, garden, office, elegant design, daylight, led, flut sconce"
    elif "Men's" in text:
        keywords = "men outfit, men clothes, tshirt, daily tshirt, cotton, round collar, basic, tshirt set"
    elif "City" in text:
        keywords = "wine cooler, cocktail shaker, bartender, pub, bar, drink, wine, alcohol"
    elif "Doxa" in text:
        if "Men" in text:
            keywords = "shampoo, men shampoo, haircare, suitable for all hair types, bath, shower, " \
                       "man shampoo, haircare products"
        elif "Shower Gel" in text:
            keywords = "shower gel, personal care, unisex, women, men, bath, shower, cherry milk, mango milk, blackberry " \
                       "milk, avocado milk, fresh, summer edition"
        elif "Liquid Soap" in text:
            keywords = "vegan liquid soap, organic liquid soap, vegan, organic, liquid soap, personal care, suitable all " \
                       "skin types, unisex, vegan products, organic products"
        elif "Baby" in text:
            keywords = "baby, baby soap, baby shampoo, bath time, baby cleaning, bath, mother, shower, new, " \
                       "most purchased, girls, boys, unisex baby soap, solid soap bar, baby soap"
        elif "Beauty Soap" in text:
            keywords = "personal care, women, men, bodycare, soap bar, soap, bar, new, most purchased, set, soap set, " \
                       "fragrance"
        elif "Vegan Shampoo" in text:
            keywords = "vegan shampoo, organic shampoo, vegan, organic, skincare, bath, shower, argan oil, lemon oil, " \
                       "keratine, olive oil, argan oil shampoo, olive oil shampoo, lemon oil " \
                       "shampoo, women shampoo, haircare products"
    elif "Confetti" in text:
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

    keywords = keywords.replace(",", ";")
    keywords = keywords.lower()
    print(text)
    print(keywords)
    inventory_file.write(sku+"\n"+text+"\n"+keywords+"\n")
    inventory_file.close()
    ###########################################

    ###############Send Request################
    # with open('patch_demo.json', 'r') as file:
    #     data = file.readlines()
    # with open('patch_demo.json', 'w') as file:
    #     data[8] = f'\t\t  "value": "{text}",\n'
    #     data[18] = f'\t\t  "value": "{keywords}",\n'
    #     file.writelines(data)
    #
    # file = open('patch_demo.json', "r+")
    # body = json.load(file)
    # # print(body)
    # resp = listing.patch_listings_item(sellerId='A2YSV8HF6GQ3SP', sku=sku, body=body,
    #                                    marketplaceIds=['A1F83G8C2ARO7P'])
    # print(resp)
    # file.close()
    ###########################################


sku_file = open("skus.txt", "r+")
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
#   ]
# }