import json
import os
import shutil
from flask import Flask, render_template, request
from config import PATH_ACCOUNTS
from apps.did import DID 
from apps.rsa import sign_the_credential

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_did')
def new_did():
    list_actor = [{"name":"Driver-A", "pub_key":"", "pri_key":"", "did":""}, \
            {"name":"Driver-B", "pub_key":"", "pri_key":"", "did":""}, \
            {"name":"Car-X", "pub_key":"", "pri_key":"", "did":""}]

    # Reset account dir
    if os.path.exists(PATH_ACCOUNTS):
        shutil.rmtree(PATH_ACCOUNTS)
    os.makedirs(PATH_ACCOUNTS)

    # Generate key pair
    for index in range(len(list_actor)):
        did = DID()
        list_actor[index] = did.new_did(list_actor[index])

    return render_template('new_did.html', list_actor = list_actor)

@app.route('/event', methods=['GET'])
def event():
    actor_from = request.args.get('from')
    code = request.args.get('code')

    template_file = 'event_1.html'
    pic = 'static/imgs/a_conn_to_car.png'
    event = ''
    actor_to = ''

    if int(code) < 4:
        actor_to = 'Driver-A'
        pic = 'static/imgs/a_conn_to_car.png'
    elif int(code) < 7:
        actor_to = 'Driver-B'
        pic = 'static/imgs/b_conn_to_car.png'
    else:
        actor_to = 'Car-X'
        pic = 'static/imgs/verifier.png'

    if code == '1' or code == '4':
        event = 'connect'
    elif code == '2' or code == '5':
        event = 'driving'
    elif code == '3' or code == '6':
        event = 'disconnect'
    else:
        event = 'verified'
        
    # Create DID credential
    with open('credentials/event.json', 'r') as outfile:
        cre_did = json.load(outfile)
        cre_did["credentialSubject"]["degree"]["value"] = event

        credential = cre_did

    # Sign the credential
    cre_did["signature"] = sign_the_credential("Car-X", credential)

    # Write to file
    # credential_filename = "credentials/" + str(code)  + ".json"
    # with open(credential_filename, 'w') as outfile:
    #    outfile.write(str(cre_did))

    return render_template('event.html', actor_from = actor_from, \
            actor_to = actor_to, event = event, credential = credential, \
            pic = pic, next_code = str(int(code) + 1))

@app.route('/verify')
def verify():
    return render_template('verify.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8888, debug = True)
