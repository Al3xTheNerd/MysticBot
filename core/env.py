from dotenv import load_dotenv
import os

load_dotenv()

token = os.environ.get('TOKEN')
webAddress = os.environ.get('WEBADDRESS')
itemSoloAddress = os.environ.get('ITEMSOLOADDRESS')
itemImageAddress = os.environ.get('ITEMIMAGEADDRESS')
databaseFile = os.environ.get('DATABASEFILE')
server_name = os.environ.get('MC_SERVER_NAME')

devMode: str | None = os.environ.get('DEV')
if devMode == "True":
    DEV_MODE: bool = True
else:
    DEV_MODE = False