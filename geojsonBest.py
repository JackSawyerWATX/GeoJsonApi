import urllib.request, urllib.parse, urllib.error
import json
import ssl

def get_place_id(js):
    if 'results' in js and len(js['results']) > 0:
        return js['results'][0]['place_id']
    else:
        return None

api_key = False

if api_key is False:
    api_key = 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json?'
else:
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def main():
    while True:
        address = input('Enter location: ')
        if len(address) < 1:
            break

        parms = dict()
        parms['address'] = address
        if api_key is not False:
            parms['key'] = api_key
        url = serviceurl + urllib.parse.urlencode(parms)

        print('Retrieving', url)
        uh = urllib.request.urlopen(url, context=ctx)
        data = uh.read().decode()
        print('Retrieved', len(data), 'characters')

        try:
            js = json.loads(data)
        except:
            js = None

        if not js or 'status' not in js or js['status'] != 'OK':
            print('==== Failure To Retrieve ====')
            print(data)
            continue

        # print(json.dumps(js, indent=4))

        lat = js['results'][0]['geometry']['location']['lat']
        lng = js['results'][0]['geometry']['location']['lng']
        print('lat', lat, 'lng', lng)
        location = js['results'][0]['formatted_address']
        print(location)
        
        place_id = get_place_id(js)
        if place_id:
            print('Place ID:', place_id)
        else:
            print('No place ID found.')

if __name__ == "__main__":
    main()
