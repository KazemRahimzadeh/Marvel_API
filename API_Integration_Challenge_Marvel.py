# """"""""""Libraries and Modules"""""""""""

import json
import urllib.parse
import hashlib
import requests
import os

# """"""""""Authentication"""""""""""

timestamp = '1'  # the time given for the API calls, required for generating md5 hash
public_key = input("Enter your public key: ")  # asking for public key
private_key = input("Enter your private key: ")  # asking for private key
md5_prerequisites = timestamp + private_key + public_key  # prerequisites
generated_md5_hash = hashlib.md5(md5_prerequisites.encode())  # generating the md5 hash

api = "http://gateway.marvel.com/v1/public/characters?"  # Making a variable for the API requests URL

os.system("CLS")  # clearing the given login parameters on windows, use 'Clear' for Linux OS

# """"""""""Searching in API and handling errors"""""""""""
search_count = 1

while True:
    name = input(str(search_count) + "- Which character do you want to gain info about?(press enter to end) ")
    search_count += 1
    if name == "":
        break
    url = api + urllib.parse.urlencode(
        {"name": name, "ts": timestamp, "apikey": public_key,
         "hash": generated_md5_hash.hexdigest()})  # hexdigest() : Returns the encoded data in hexadecimal format.
    # Collected Json data from the given name
    json_data = requests.get(url).json()
    json_status = json_data["code"]
    if json_status == 200:
        if json_data["data"]["total"] == 0:
            print("Nothing found :(")
        else:
            print("Looking for: " + name)
            print("Description: " + str(json_data["data"]["results"][0]["description"]))
            print(name + " appears in the comics below:\n")
            counter = 0
            print("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
            # Looping through different comics in db and printing them out line by line:
            for each in json_data["data"]["results"][0]["comics"]["items"]:
                counter += 1
                print(str(counter).rjust(2) + "- " + each["name"])
            print("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄\n")
    #  Error handling according to the given statuses
    elif json_status == 409:
        print("API key, hash of timestamp is not given.")
    elif json_status == 401:
        print("timestamp of de referer is not correctly given.")
    elif json_status == 405:
        print("This methode is not allowed!")
    elif json_status == 403:
        print("No access!")
    else:
        print("Unfortunately something went wrong, please try again.")
