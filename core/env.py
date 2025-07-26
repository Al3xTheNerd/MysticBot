from dotenv import load_dotenv
import os

load_dotenv()

token = os.environ.get('token')
webAddress = os.environ.get('webAddress')
itemSoloAddress = os.environ.get('itemSoloAddress')
itemImageAddress = os.environ.get('itemImageAddress')
databaseFile = os.environ.get('databaseFile')