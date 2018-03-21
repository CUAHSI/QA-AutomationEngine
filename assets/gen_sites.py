""" Generates sites for HIS system testing based on random data (seeded) """
import argparse
import random
import string

parser = argparse.ArgumentParser()
parser.add_argument('--count')
args = parser.parse_args()

count = int(args.count)

with open('sites.csv', 'w') as sites_file:
    sites_file.write('SiteCode,SiteName,Latitude,Longitude,County,SiteState,' +
                     'LatLongDatumSRSName,Elevation,SiteType\n')

random.seed(4)

for i in range(0, count):
    site_code = str(i+1)
    site_name = [random.choice(string.ascii_letters) for i in range(0, 20)]
    site_name = ''.join(site_name)
    latitude = str(90*random.random()-90*random.random())[:8]
    longitude = str(180*random.random()-180*random.random())[:8]
    county = ''
    site_state = ''
    datum_srs = 'WGS84'
    elevation = str(random.randint(1, 500))
    site_type = 'Stream'
    unquoted_row = [site_code, site_name, latitude, longitude, county, site_state,
                    datum_srs, elevation, site_type]
    row = ['"{}"'.format(field) for field in unquoted_row]
    with open('sites.csv', 'a') as sites_file:
        sites_file.write(','.join(row) + '\n')
