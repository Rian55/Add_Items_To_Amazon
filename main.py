from sp_api.api import Feeds
from configparser import ConfigParser

config = ConfigParser()
config.read("./.config.txt")
credentials = dict(config['default'])
