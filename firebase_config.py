import json
import os

FILES="files_db.json"
LOC="location_db.json"

# create if not exist

if not os.path.exists(FILES):

    with open(FILES,"w") as f:

        json.dump([],f)

if not os.path.exists(LOC):

    with open(LOC,"w") as f:

        json.dump({},f)


def upload_file(path,name):

    with open(FILES) as f:

        data=json.load(f)

    data.append(name)

    with open(FILES,"w") as f:

        json.dump(data,f)


def get_files():

    with open(FILES) as f:

        return json.load(f)


def save_location(user,lat,lng):

    with open(LOC) as f:

        data=json.load(f)

    data[user]={

        "Latitude":lat,
        "Longitude":lng

    }

    with open(LOC,"w") as f:

        json.dump(data,f)


def get_locations():

    with open(LOC) as f:

        return json.load(f)
