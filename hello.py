import os
from flask import Flask, request
import plistlib, json
import requests
import xmltodict
app = Flask(__name__)


def get_params_get():
    info = {}
    if request.method == 'GET':
        for key, value in request.args.lists():
            info[key] = value[0]
    else:
        for key, value in request.form.lists():
            info[key] = value[0]
    return info


@app.route('/json-to-plist/', methods=['POST', 'GET'])
def json_to_plist():
    params = get_params_get()
    if params.get('url'):
        status_code, content = make_request(params)
        if 200 >= status_code < 400:
            try:
                info_json = json.loads(content)
                return plistlib.writePlistToString(info_json)
            except:
                return "{\"error\":true}"
        else:
            return "{\"error\":true}"
    else:
        return "{\"error\":true}"


@app.route('/plist-to-json/', methods=['POST', 'GET'])
def plist_to_json():
    params = get_params_get()
    if params.get('url'):
        status_code, content = make_request(params)
        if 200 >= status_code < 400:
            try:
                info_plist = plistlib.readPlistFromString(content)
                return json.dumps(info_plist)
            except Exception, e:
                return "{\"error\":true}"
        else:
            return "{\"error\":true}"
    else:
        return "{\"error\":true}"

@app.route('/xml-to-json/', methods=['POST', 'GET'])
def xml_to_json():
    params = get_params_get()
    if params.get('url'):
        status_code, content = make_request(params)
        if 200 >= status_code < 400:
            try:
                info_xml = xmltodict.parse(content)
                return json.dumps(info_xml)
            except:
                return "{\"error\":true}"
        else:
            return "{\"error\":true}"
    else:
        return "{\"error\":true}"


@app.route('/json-to-xml/', methods=['POST', 'GET'])
def json_to_xml():
    params = get_params_get()
    if params.get('url'):
        status_code, content = make_request(params)
        if 200 >= status_code < 400:
            try:
                info_json = json.loads(content)
                return xmltodict.unparse({"xml":info_json})
            except Exception, e:
                return "{\"error\":true}"
        else:
            return "{\"error\":true}"
    else:
        return "{\"error\":true}"

def make_request(params):
    url = params.get('url')
    del params['url']
    if request.method == 'GET':
        r = requests.get(url, params=params)
    elif request.method == 'POST':
        r = requests.post(url, params=params)
    else:
        return 0, ""
    return r.status_code, r.content


if __name__ == '__main__':
    app.debug = True
    app.run()