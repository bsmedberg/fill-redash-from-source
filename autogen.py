import sys, os, json
import argparse
import urllib2

base_url = "https://sql.telemetry.mozilla.org/api/"

def check_or_update_list(queries, user_api_key):
    def api_get(*path):
        url = base_url + '/'.join(map(str, path))
        r = urllib2.Request(url)
        r.add_header('Authorization', 'Key ' + user_api_key)
        fd = urllib2.urlopen(r)
        return json.load(fd)

    def api_post(d, *path):
        url = base_url + '/'.join(map(str, path))
        r = urllib2.Request(url, json.dumps(d))
        r.add_header('Authorization', 'Key ' + user_api_key)
        fd = urllib2.urlopen(r)
        return json.load(fd)

    datasources = api_get('data_sources')
    dsmap = {}
    for ds in datasources:
        dsmap[ds['name']] = ds

    def check_or_update_query(q):
        id = q['id']
        name = q['name']
        ds = q['data_source']
        qs = q['query']
        api_key = q['api_key']

        updates = {}

        r = api_get('queries', id)
        if r['name'] != name:
            updates['name'] = name
        if r['data_source_id'] != dsmap[ds]['id']:
            updates['data_source_id'] = dsmap[ds]['id']
        if r['query'] != qs:
            updates['query'] = qs
        if r['api_key'] != api_key:
            raise ValueError("API key for query [{}]: {} doesn't match.".format(id, name))

        if not len(updates):
            print "[{}] {}: Up to date".format(id, name)
            return

        print "[{}] {}: Updating {}".format(id, name, ','.join(updates.keys()))
        api_post(updates, 'queries', id)

        if 'query' in updates:
            api_post({}, 'queries', id, 'refresh')

    for q in queries:
        check_or_update_query(q)

if __name__ == "__main__":
    a = argparse.ArgumentParser(description="Update sql.telemetry.mozilla.org queries")
    a.add_argument("manifest", metavar="manifest.json", help="Path to autogen.json")
    a.add_argument("apikey", help="Your sql.telemetry.mozilla.org API key")
    args = a.parse_args()

    d = json.load(open(args.manifest))
    check_or_update_list(d['queries'], args.apikey)
