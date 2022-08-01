import json
from configparser import ConfigParser
from sp_api.base import Marketplaces
from sp_api.api import Feeds
from sp_api.api import ListingsItems
from sp_api.api import ProductTypeDefinitions
from sp_api.api import Notifications
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
from time import sleep

config = ConfigParser()
config.read(".config.txt")
credentials = dict(config['default'])
feed = Feeds(credentials=credentials, marketplace=Marketplaces.PL)
listing = ListingsItems(credentials=credentials, marketplace=Marketplaces.UK)
types = ProductTypeDefinitions(credentials=credentials, marketplace=Marketplaces.UK)
notifications = Notifications(credentials=credentials, marketplace=Marketplaces.UK)

# shoes = types.get_definitions_product_type(productType="SHOES", marketplaceIds=['A1F83G8C2ARO7P'])
# print(shoes)

xdd = notifications.get_destinations()
print(xdd)

# file = open('test2.json', "r+")
# body = json.load(file)
# resp = listing.put_listings_item(sellerId='A2YSV8HF6GQ3SP', sku='TR-TE5T-5WO9', body=body,
#                                  marketplaceIds=['A1F83G8C2ARO7P'])
# file.close()
# print(resp)





def create_product_xml():
    root = ET.Element("AmazonEnvelope", {"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
                                         "xsi:noNamespaceSchemaLocation":"amznenvelope.xsd"})
    header = ET.SubElement(root, "Header")
    doc_ver = ET.SubElement(header, "DocumentVersion")
    doc_ver.text = "1.01"
    merch_id = ET.SubElement(header, "MerchantIdentifier")
    merch_id.text = "A2YSV8HF6GQ3SP"
    msg_type = ET.SubElement(root, "MessageType")
    msg_type.text = "Product"
    P_and_R = ET.SubElement(root, "PurgeAndReplace")
    P_and_R.text = "false"

    message = ET.SubElement(root, "Message")
    msg_id = ET.SubElement(message, "MessageID")
    op_type = ET.SubElement(message, "OperationType")
    op_type.text = "Update"
    product = ET.SubElement(message, "Product")
    SKU = ET.SubElement(product, "SKU")
    prdct_tax_code = ET.SubElement(product, "ProductTaxCode")
    launch_date = ET.SubElement(product, "LaunchDate")
    description_data = ET.SubElement(product, "DescriptionData")
    title = ET.SubElement(description_data, "Title")
    brand = ET.SubElement(description_data, "Brand")
    description = ET.SubElement(description_data, "Description")
    #for... ET.SubElement(description_data, "BulletPoint")
    manufacturer = ET.SubElement(description_data, "Manufacturer")
    #for... ET.SubElement(description_data, "SearchTerms")
    item_type = ET.SubElement(description_data, "ItemType")
    gift_wrap = ET.SubElement(description_data, "IsGiftWrapAvailable")
    gift_msg = ET.SubElement(description_data, "IsGiftMessageAvailable")
    #if zone == ... ET.SubElement(description_data, "RecommendedBrowseNode")
    product_data = ET.SubElement(product, "ProductData")

    xmlstr = parseString(ET.tostring(root)).toprettyxml(indent="\t")
    with open("product_feed.xml", "w+") as f:
        f.write(xmlstr)


#create_product_xml()
    # file = open("test.xml", "r+")
# response1, response2 = feed.submit_feed(feed_type='POST_PRODUCT_DATA', file=file, AWS_ENV="SANDBOX")
# file.close()
# print(response1, " ", response2)
#print(feed.get_feed_document(50023019201))