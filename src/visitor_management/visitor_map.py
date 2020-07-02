import os

def create_visitor_rid_file(visitor):
    visitor_token = visitor["visitor"]["token"]

    visitor_folder_path = os.path.join(os.getcwd(), "visitor_map")
    if not os.path.isdir(visitor_folder_path):
        os.mkdirs(visitor_folder_path)

    try:
        visitor_file = open("visitor_map/{}".format(visitor_token), "r")
    #file does not exist
    except:
        visitor_file = open("visitor_map/{}".format(visitor_token), "w")
        visitor_file.write(visitor_token)
        visitor_file.close()
        visitor_file = open("visitor_map/{}".format(visitor_token), "r")
    finally:
        rid = visitor_file.read()
        visitor_file.close()
        return rid

def update_visitor_rid_file(visitor_token, room, rid):
    if room["_id"] != rid:
        visitor_file = open("visitor_map/{}".format(visitor_token), "w")
        visitor_file.write(room["_id"])
        visitor_file.close()
