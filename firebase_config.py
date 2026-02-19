files=[]
locations={}

def upload_file(path,name):

    files.append(name)

def get_files():

    return files

def save_location(user,lat,lng):

    locations[user]=[lat,lng]

def get_locations():

    return locations
