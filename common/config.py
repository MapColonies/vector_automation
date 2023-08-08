import os

featureType = 'buildings'
exceptions = ("text/xml", "application/json", "text/javascript")

outputFormat = ("application/xml", "application/json")


bbox_x = [29.73756916597569, 33.35012435913086]
bbox_y = [34.21269226074219, 35.87874221801758]

version = os.getenv("VERSION", "2.0.0")
header_user = os.getenv("USER", 'x-api-key')
header_pass = token = os.getenv("TOKEN")
headers_auth = {header_user: header_pass}
numbers_of_req = os.getenv("REQ_AMOUNT", 25)
by_date = os.getenv("date_label", "date")  # last_update_date
feature_name = os.getenv('FEATURES', 'features')
gfid = os.getenv("GFID", 'id')  # gfid
by_date_filter = ('&count=', f'&sortBy={by_date}&count=')
low_time = int(os.getenv("LOW_VALUE", 100))
med_time = int(os.getenv("MED_VALUE", 500))
custom_path = os.getenv("path_dir_source", "Results")
