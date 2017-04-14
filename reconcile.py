"""
An OpenRefine reconciliation service for the API provided GeoNames.

GeoNames API documentation: http://www.geonames.org/export/web-services.html

This code is adapted from the wonderful Ted Lawless' work at https://github.com/lawlesst/fast-reconcile
"""
from flask import Flask
from flask import request
from flask import jsonify
import json
from operator import itemgetter
import urllib
from fuzzywuzzy import fuzz
import requests
from sys import version_info

app = Flask(__name__)
app.config.from_object('config')

geonames_username = app.config['GEONAMES_USERNAME']

#If it's installed, use the requests_cache library to
#cache calls to the GeoNames API.
try:
    import requests_cache
    requests_cache.install_cache('geonames_cache')
except ImportError:
    app.logger.debug("No request cache found.")
    pass

#See if Python 3 for unicode/str use decisions
PY3 = version_info > (3,)

#Help text processing
import text
import lc_parse

#Create base URLs/URIs
api_base_url = 'http://api.geonames.org/searchJSON?username=' + geonames_username + '&isNameRequired=yes&'
geonames_uri_base = 'http://sws.geonames.org/{0}'

#Map the GeoNames query indexes to service types
default_query = {
    "id": "/geonames/all",
    "name": "All GeoNames terms",
    "index": "q"
}

refine_to_geonames = [
    {
        "id": "/geonames/name",
        "name": "Place Name",
        "index": "name"
    },
    {
        "id": "/geonames/name_startsWith",
        "name": "Place Name Starts With",
        "index": "name_startsWith"
    },
    {
        "id": "/geonames/name_equals",
        "name": "Exact Place Name",
        "index": "name_equals"
    }
]
refine_to_geonames.append(default_query)


#Make a copy of the GeoNames mappings.
query_types = [{'id': item['id'], 'name': item['name']} for item in refine_to_geonames]

# Basic service metadata. There are a number of other documented options
# but this is all we need for a simple service.
metadata = {
    "name": "GeoNames Reconciliation Service",
    "defaultTypes": query_types,
    "view": {
        "url": "{{id}}"
    }
}

def make_uri(geonames_id):
    """
    Prepare a GeoNames url from the ID returned by the API.
    """
    geonames_uri = geonames_uri_base.format(geonames_id)
    return geonames_uri


def jsonpify(obj):
    """
    Helper to support JSONP
    """
    try:
        callback = request.args['callback']
        response = app.make_response("%s(%s)" % (callback, json.dumps(obj)))
        response.mimetype = "text/javascript"
        return response
    except KeyError:
        return jsonify(obj)


def search(raw_query, query_type='/geonames/all'):
    """
    Hit the GeoNames API for names.
    """
    out = []
    unique_geonames_ids = []
    mid_query = lc_parse.lc2geonames(raw_query, PY3)
    query = text.normalize(mid_query, PY3).strip()
    query_type_meta = [i for i in refine_to_geonames if i['id'] == query_type]
    if query_type_meta == []:
        query_type_meta = default_query
    query_index = query_type_meta[0]['index']
    try:
        if PY3:
            url = api_base_url + query_index  + '=' + urllib.parse.quote(query)
        else:
            url = api_base_url + query_index  + '=' + urllib.quote(query)
        app.logger.debug("GeoNames API url is " + url)
        resp = requests.get(url)
        results = resp.json()
    except getopt.GetoptError as e:
        app.logger.warning(e)
        return out
    for position, item in enumerate(results['geonames']):
        match = False
        name = item.get('name')
        alternate = item.get('toponymName')
        if (len(alternate) > 0):
            alt = alternate[0]
        else:
            alt = ''
        geonames_id = item.get('geonameId')
        geonames_uri = make_uri(geonames_id)
        lat = item.get('lat')
        lng = item.get('lng')
        #Way to cheat + get name + coordinates into results:
        name_coords = name + ' | ' + lat + ', ' + lng
        #Avoid returning duplicates:
        if geonames_id in unique_geonames_ids:
            continue
        else:
            unique_geonames_ids.append(geonames_id)
        score_1 = fuzz.token_sort_ratio(query, name)
        score_2 = fuzz.token_sort_ratio(query, alt)
        score = max(score_1, score_2)
        if query == text.normalize(name, PY3):
            match = True
        elif query == text.normalize(alt, PY3):
            match = True
        resource = {
            "id": geonames_uri,
            "name": name_coords,
            "score": score,
            "match": match,
            "type": query_type_meta
        }
        out.append(resource)
    #Sort this list by score
    sorted_out = sorted(out, key=itemgetter('score'), reverse=True)
    #Refine only will handle top three matches.
    return sorted_out[:3]


@app.route("/reconcile", methods=['POST', 'GET'])
def reconcile():
    # If a 'queries' parameter is supplied then it is a dictionary
    # of (key, query) pairs representing a batch of queries. We
    # should return a dictionary of (key, results) pairs.
    queries = request.form.get('queries')
    if queries:
        queries = json.loads(queries)
        results = {}
        for (key, query) in queries.items():
            qtype = query.get('type')
            if qtype is None:
                return jsonpify(metadata)
            data = search(query['query'], query_type=qtype)
            results[key] = {"result": data}
        return jsonpify(results)
    # If neither a 'query' nor 'queries' parameter is supplied then
    # we should return the service metadata.
    return jsonpify(metadata)

if __name__ == '__main__':
    from optparse import OptionParser
    oparser = OptionParser()
    oparser.add_option('-d', '--debug', action='store_true', default=False)
    opts, args = oparser.parse_args()
    app.debug = opts.debug
    app.run(host='0.0.0.0')
