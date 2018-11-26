def key_value_to_dict(inp_str):

    result = {}
    tokens = inp_str.split("&")

    for param in tokens:
        param_tokens = param.split("=")
        if 2 == len(param_tokens):
            result[param_tokens[0]] = param_tokens[1]

    return result

def get_geo_ip_data(ip_address, use_max_mind_geo_ip=True, geo_ip=None, use_paid_version=False):
    country_code = ''
    city = ''
    state = ''
    postal_code = 0
    country_name = ''
    GEOIP_DB_PATH = 'PLACE YOUR GEOIP DATABASE PATH HERE'
    GEOIP_FILE_NAME = 'GeoLiteCity.dat'
    if use_paid_version:
        GEOIP_FILE_NAME = 'GeoIPCity.dat'
    if ip_address != '':
        try:
            if use_max_mind_geo_ip:
                if not geo_ip:
                    import pygeoip
                    geo_ip = pygeoip.GeoIP(GEOIP_DB_PATH + '/' + GEOIP_FILE_NAME)

                ip_addr_data = geo_ip.record_by_addr(ip_address)
            else:
                '''
                #this flow should be used for http endpoint for domains behind akamai
                # use relevant request libray of framework being used, we have used Flask
                from flask import request
                
                ip_addr_data = request.headers['X-Akamai-Edgescape'] if 'X-Akamai-Edgescape' in request.headers else ""
                ip_addr_data = ip_addr_data.replace(',',"&")
                ip_addr_data = key_value_to_dict(ip_addr_data)
                if ip_addr_data:
                    ip_addr_data["dma_code"] = ip_addr_data.pop('dma') if "dma" in ip_addr_data else ''
                    ip_addr_data["latitude"] = ip_addr_data.pop('lat') if "lat" in ip_addr_data else ''
                    ip_addr_data["area_code"] = ip_addr_data.pop("areacode") if "areacode" in ip_addr_data else ''
                    ip_addr_data["longitude"] = ip_addr_data.pop('long') if "long" in ip_addr_data else ''
                    ip_addr_data["time_zone"] = ip_addr_data.pop('timezone') if "timezone" in ip_addr_data else ''
                    ip_addr_data["metro_code"] = ip_addr_data.pop('city') if 'city' in ip_addr_data else '' +", "+ip_addr_data.pop('region_code') if 'region_code' in ip_addr_data else ''
                    ip_addr_data["postal_code"] = ip_addr_data.pop('zip') if "zip" in ip_addr_data else ''
                    ip_addr_data["country_name"] = ""
                else:
                    ip_addr_data = {}
                '''
                ip_addr_data = {}

            if 'country_code' in ip_addr_data and ip_addr_data['country_code'] is not None and ip_addr_data['country_code'] != '':
                country_code = ip_addr_data['country_code'].upper()
            if '' != country_code:
                if 'city' in ip_addr_data and ip_addr_data['city'] is not None:
                    city = ip_addr_data['city'].upper()

                if 'region_code' in ip_addr_data and ip_addr_data['region_code'] is not None:
                    state = ip_addr_data['region_code'].upper()

                if 'postal_code' in ip_addr_data and ip_addr_data['postal_code'] is not None:
                    postal_code = ip_addr_data['postal_code']

                if 'country_name' in ip_addr_data and ip_addr_data['country_name'] is not None:
                    country_name = ip_addr_data['country_name']
        except Exception,e:
            return {'error' : 'error while doing geoip lookup'}
    
    return {
        'ip_address':ip_address,
        'country_code': country_code,
        'city': city,
        'state': state,
        'postal_code': postal_code,
        'country_name': country_name,
        'raw_data': ip_addr_data
        }


import sys
if len(sys.argv) > 1 and 'get_ip_info.py' == sys.argv[0]:
    ip_address_arr = sys.argv[1:]
    import pygeoip
    import pprint
    geoip = pygeoip.GeoIP('./GeoLiteCity.dat')

    for ip_address in ip_address_arr:
        print("======ip info of ip_addr: " + ip_address + " =========")
        ip_addr_data = get_geo_ip_data(ip_address, use_max_mind_geo_ip=True, geo_ip=geoip)
        pprint.pprint(ip_addr_data)
else:
    print("invalid arguments for the ipinfo")
