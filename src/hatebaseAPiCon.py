import requests
import json
import csv

i = 1
with open("hate_speech.csv", 'w') as f:  # Just use 'w' mode in 3.x
    while i <= 6:
        r1 = requests.get("https://api.hatebase.org/v3-0/ef3a4ee03a70cf2c4e4d3ba1c20ccdb1/vocabulary/json/language=eng|page=" + str(i))
        temp = json.loads(r1.text)
        list_t = temp["data"]["datapoint"]    
        for dict_t in list_t:
            w = csv.DictWriter(f, dict_t.keys())
            w.writerow(dict_t)
        i += 1