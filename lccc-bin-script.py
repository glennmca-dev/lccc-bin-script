#!/home/pi/.myvenv/bin/python
# If you are using a VENV you will need to point to your python install using a shebang as shown above
# If not delete the comments/ shebang on lines 1-3 of this script
from os import environ
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
from datetime import timedelta
import re

# Decision to send notification:
notify = False

# Get raw HTML
raw_response = requests.get('YOUR_URL')
# Parse HTML and get section with next collection info
parsed_html = BeautifulSoup(raw_response.text, "html.parser")
collections = parsed_html.body.find('div', attrs={'id':'nextCollectionSection'}).text.split("\n")
# Remove any empty lines or non-useful info like headings
collections = list(filter(None, collections))
collections.remove(collections[0])
# Get current date
current_date = dt.now().date()
# Find index of the 3 collection dates (useful for working in between later for Bin info)
date_regex = "\w{1,}\s\d{1,2}\w{2}\s\w{1,}"
date_indicies = []
for item in collections:
    if re.match(date_regex, item):
        date_indicies.append(collections.index(item))

# prepare the date string for formatting into a datetime object
next_collection_date = collections[date_indicies[0]].split(' ')
next_collection_date[1] = re.sub('[a-zA-z]','',next_collection_date[1])
next_collection_date = str(str.join(' ', next_collection_date) + " " + str(current_date.year))

# Create datetime object with next collection date
next_collection = dt.strptime(next_collection_date, "%A %d %B %Y").date()

# check if date is < 1 day away from now
days_til_collection = next_collection - current_date
one_day = timedelta(days=1)
zero_day = timedelta(days=0)
if days_til_collection == one_day:
    notify = True

# Check which bin is going out:
bins_to_go_out = []
for item in collections[date_indicies[0]+1:date_indicies[1]]:
    bins_to_go_out.append(item.strip(' '))

# Build Notification message:
message = f"BINS: Your"
if len(bins_to_go_out) >= 0:
    bin_string = ""
    for i in bins_to_go_out:
        bin_name = ""
        # i = i.strip(" ")
        match i:
            case "BrownBin":
                bin_name = "Brown Bin"
            case "RecycleBin":
                bin_name = "Recycling Bin"
            case "ResidualBin":
                bin_name = "Black Bin"
            case _: # Default
                bin_name = i
        bin_string += f" {bin_name}"
        if i != bins_to_go_out[-1]:
            bin_string += " and"
    message += bin_string
    message += f" need left out for collection on, {next_collection_date}"
print(message)
    
   
# if true notify phone
if notify:
    print('notification sent')
    requests.post('https://api.mynotifier.app', 
                {    
                    "apiKey": "YOUR_API_KEY",    
                    "message": message,    
                    "description": "Bin Notification from RasPi",    
                    "type": "info", # info, error, warning or success
                })
else:
    # else exit
    exit(0)


    