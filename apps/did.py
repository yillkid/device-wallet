import os
import json
from apps.rsa import gen_key_pair
from config import PATH_ACCOUNTS

class DID():
    def __init__(self):
        return

    def new_did(self, data):
        # Check username exist
        if os.path.isdir(PATH_ACCOUNTS + "/" + data["name"]):
            return {"status":"error","msg":"Account already exist."}

        # Create account folder on local
        os.mkdir(PATH_ACCOUNTS + "/" + data["name"])

        # Generate key-pair
        pub_key, pri_key = gen_key_pair()
        data["pub_key"] = pub_key
        data["pri_key"] = pri_key
        
        with open(PATH_ACCOUNTS + "/" + data["name"] + "/private.pem", 'w') as outfile:
            outfile.write(pri_key)

        with open(PATH_ACCOUNTS + "/" + data["name"] + "/public.pem", 'w') as outfile:
            outfile.write(pub_key)

        # Create DID credential
        with open("credentials/did.json", 'r') as outfile:
            cre_did = json.load(outfile)
            cre_did["authentication"][0]["publicKeyPem"] = data["pub_key"]

            # Set credential
            data["did"] = cre_did

        return data
