import os
path = os.path.dirname(__file__)

with open(f"{path}/all-geocodes-v2017.csv", "r", encoding='utf-8') as f:
    codes = f.readlines()

with open(f"{path}/FIPS_codes.csv", "w") as f:
    f.write(",".join(["State Code", "County Code", "Area Name"]))
    for line in codes:
        line = line.split(",")
        
        if line[3] != '00000' or line[4] != '00000' or line[5] != '00000':
            continue
        
        state_code = line[1]
        county_code = line[2]
        area_name = line[6]

        f.write(",".join([state_code, county_code, area_name]))

import json

d = {}
for line in codes:
    line = line.split(",")

    if line[3] != '00000' or line[4] != '00000' or line[5] != '00000':
        continue
    
    state_code = line[1]
    county_code = line[2]
    area_name = line[6].rstrip()
    if county_code == '000':
        d[state_code] = {"state": area_name}
    else:
        d[state_code][county_code] = area_name

with open(f"{path}/FIPS_codes2.json", "w") as f:
    json.dump(d, f)
    