import json
from configparser import ConfigParser
from sp_api.base import Marketplaces
from sp_api.api import Feeds
from sp_api.api import ListingsItems
from sp_api.api import ProductTypeDefinitions

config = ConfigParser()
config.read(".config.txt")
credentials = dict(config['default'])
feed = Feeds(credentials=credentials, marketplace=Marketplaces.UK)
listing = ListingsItems(credentials=credentials, marketplace=Marketplaces.UK)
types = ProductTypeDefinitions(credentials=credentials, marketplace=Marketplaces.UK)
# notifications = Notifications(credentials=credentials, marketplace=Marketplaces.UK)

# xdxd = types.get_definitions_product_type(productType="BUCKLE", marketplaceIds=['A1F83G8C2ARO7P'])
# print(xdxd)
# xd = types.search_definitions_product_types(marketplaceIds=['A1F83G8C2ARO7P'])
# print(xd)

file = open('test2.json', "r+")
body = json.load(file)
resp = listing.put_listings_item(sellerId='A2YSV8HF6GQ3SP', sku='EWP-SATURN-CER-0001', body=body,
                                 marketplaceIds=['A1F83G8C2ARO7P'])
print(resp)
file.close()


# file2 = open('test2.json', "r+")
# body2 = json.load(file2)
# response = feed.submit_feed(feed_type='JSON_LISTINGS_FEED', file=file2, content_type='text/json')
# for i in response:
#     print(i)
# file2.close()

# print(feed.get_feeds(feedTypes="JSON_LISTINGS_FEED"))
