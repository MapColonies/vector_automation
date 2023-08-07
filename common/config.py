import os

featureType = 'buildings'
exceptions = ("text/xml", "application/json", "text/javascript")

outputFormat = ("application/xml", "application/json")

t = 'eyJkIjpbInJhc3RlciIsInJhc3RlcldtcyIsInJhc3RlckV4cG9ydCIsImRlbSIsInZlY3RvciIsIjNkIl0sImlhdCI6MTY2Mzg2MzM0Mywic3ViIjoiTWFwQ29sb25pZXNRQSIsImlzcyI6Im1hcGNvbG9uaWVzLXRva2VuLWNsaSJ9.U_sx0Rsy96MA3xpIcWQHJ76xvK0PlHa--J1YILBYm2fCwtDdM4HLGagwq-OQQnBqi2e8KwktQ7sgt27hOJIPBHuONQS0ezBbuByk6UqN2S7P8WERdt8_lejuR1c94owQq7FOkhEaj_PKJ64ehXuMMHskfNeAIBf8GBN6QUGEenVx2w5k2rYBULoU30rpFkQVo8TtmiK2yGx0Ssx2k6LqSgCZfyZJbFzZ2MH3BPeCVleP1-zypaF9DS7SxS-EutL-gZ1e9bEccNktxQA4VMcjeTv45KYJLTIrccs_8gtPlzfaeNQFTIUKD-cRD1gyd_uLatPsl0wwHyFZIgRuJtcvfw'

bbox_x = [29.73756916597569, 33.35012435913086]
bbox_y = [34.21269226074219, 35.87874221801758]

version = os.getenv("VERSION", "2.0.0")
header_user = os.getenv("USER", 'x-api-key')
header_pass = token = os.getenv("TOKEN", t)
headers_auth = {header_user: header_pass}
numbers_of_req = os.getenv("REQ_AMOUNT", 25)
by_date = os.getenv("date_label", "date")  # last_update_date
feature_name = os.getenv('FEATURES', 'features')
gfid = os.getenv("GFID", 'id')  # gfid
by_date_filter = ('&count=', f'&sortBy={by_date}&count=')
low_time = int(os.getenv("LOW_VALUE", 100))
med_time = int(os.getenv("MED_VALUE", 500))
custom_path = os.getenv("path_dir_source", "Results")
