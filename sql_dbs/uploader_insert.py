import argparse
import os
import pyodbc

parser = argparse.ArgumentParser()
parser.add_argument('--datavalues')
parser.add_argument('--methods')
parser.add_argument('--sites')
parser.add_argument('--sources')
parser.add_argument('--variables')
args = parser.parse_args()


def get_csv_data(csv_name):
    with open(csv_name, 'r') as csv_file:
        csv_lines = csv_file.readlines()
    csv_lines = [csv_line.replace('\n', '') for csv_line in csv_lines]
    return csv_lines[1:]  # header row not needed


def convert_to_list(csv_line):
    csv_list = csv_line.split('","')
    csv_list = [csv_item.replace('"', '') for csv_item in csv_list]
    return csv_list


def convert_to_id(cursor, table, cv_label, cv_value, id_label):
    cursor.execute("""
    SELECT {} FROM {} WHERE {}='{}';
    """.format(id_label, table, cv_label, cv_value))
    return cursor.fetchone()[0]


def format_fields(fields, nvarchars):
    formatted_fields = []
    for ind, field in enumerate(fields, 0):
        if ind in nvarchars:
            formatted_fields.append("'{}'".format(field))
        else:
            formatted_fields.append(str(field))
    return formatted_fields


def post_datavalues(cursor, datavalues_csv):
    for ind, datavalue_csv in enumerate(datavalues_csv, start=1):
        datavalue_csv = convert_to_list(datavalue_csv)
        methodid = convert_to_id(cursor, 'Methods', 'METHODCODE',
                                 datavalue_csv[8], 'METHODID')
        siteid = convert_to_id(cursor, 'Sites', 'SITECODE',
                               datavalue_csv[0], 'SITEID')
        sourceid = convert_to_id(cursor, 'Sources', 'SOURCECODE',
                                 datavalue_csv[9], 'SOURCEID')
        variableid = convert_to_id(cursor, 'Variables', 'VARIABLECODE',
                                   datavalue_csv[1], 'VARIABLEID')
        datavalue_db = [datavalue_csv[2],  # datavalue
                        datavalue_csv[3],  # localdatetime
                        datavalue_csv[4],  # utcoffset
                        datavalue_csv[5],  # datetimeutc
                        siteid,  # siteid
                        variableid,  # variableid
                        datavalue_csv[7],  # censorcode
                        methodid,  # methodid
                        sourceid,  # sourceid
                        datavalue_csv[6]  # qualitycontrollevelid
                        ]
        nvarchars = [1, 3, 6]
        datavalue_labels = ['DATAVALUE', 'LOCALDATETIME', 'UTCOFFSET', 'DATETIMEUTC',
                            'SITEID', 'VARIABLEID', 'CENSORCODE',
                            'METHODID', 'SOURCEID',
                            'QUALITYCONTROLLEVELID']
        datavalue_db = format_fields(datavalue_db, nvarchars)
        cursor.execute('INSERT INTO DataValues ({}) VALUES ({});'.format(
            ', '.join(datavalue_labels), ', '.join(datavalue_db)))
    cursor.commit()


def post_methods(cursor, methods_csv):
    for ind, method_csv in enumerate(methods_csv, start=1):
        method_csv = convert_to_list(method_csv)
        method_db = [method_csv[1],  # methoddescription
                     method_csv[0]  # methodcode
                     ]
        nvarchars = [0, 1]
        method_labels = ['METHODDESCRIPTION', 'METHODCODE']
        method_db = format_fields(method_db, nvarchars)
        cursor.execute('INSERT INTO Methods ({}) VALUES ({});'.format(
            ', '.join(method_labels), ', '.join(method_db)))
    cursor.commit()


def post_sources(cursor, sources_csv):
    for ind, source_csv in enumerate(sources_csv, start=1):
        source_csv = convert_to_list(source_csv)
        source_db = [source_csv[1],  # organization
                     source_csv[2],  # sourcedescription
                     source_csv[3],  # sourcelink
                     source_csv[4],  # contactname
                     'Unknown',  # phone
                     source_csv[5],  # email
                     'Unknown',  # address
                     'Unknown',  # city
                     'Unknown',  # state
                     'Unknown',  # zipcode
                     source_csv[6],  # citation
                     '0',  # metadataid
                     source_csv[0]  # sourcecode
                     ]
        nvarchars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
        source_labels = ['ORGANIZATION', 'SOURCEDESCRIPTION',
                         'SOURCELINK', 'CONTACTNAME', 'PHONE', 'EMAIL',
                         'ADDRESS', 'CITY', 'STATE', 'ZIPCODE', 'CITATION',
                         'METADATAID', 'SOURCECODE']
        source_db = format_fields(source_db, nvarchars)
        cursor.execute('INSERT INTO Sources ({}) VALUES ({});'.format(
            ', '.join(source_labels), ', '.join(source_db)))
    cursor.commit()


def post_sites(cursor, sites_csv):
    for ind, site_csv in enumerate(sites_csv, start=1):
        site_csv = convert_to_list(site_csv)
        latlongdatumid = convert_to_id(cursor, 'SpatialReferences', 'SRSNAME',
                                       site_csv[6], 'SpatialReferenceID')
        site_db = [site_csv[0],  # sitecode
                   site_csv[1],  # sitename
                   site_csv[2],  # latitude
                   site_csv[3],  # longitude
                   latlongdatumid,  # latlongdatumid
                   site_csv[7],  # elevation_m
                   site_csv[5],  # state
                   site_csv[4],  # county
                   site_csv[8]  # sitetype
                   ]
        nvarchars = [0, 1, 6, 7, 8]
        site_labels = ['SITECODE', 'SITENAME', 'LATITUDE', 'LONGITUDE',
                       'LATLONGDATUMID', 'ELEVATION_M', 'STATE',
                       'COUNTY', 'SITETYPE']
        site_db = format_fields(site_db, nvarchars)
        print('INSERT INTO Sites ({}) VALUES ({});'.format(
            ', '.join(site_labels), ', '.join(site_db)))
        cursor.execute('INSERT INTO Sites ({}) VALUES ({});'.format(
            ', '.join(site_labels), ', '.join(site_db)))
    cursor.commit()


def post_variables(cursor, variables_csv):
    for ind, variable_csv in enumerate(variables_csv, start=1):
        variable_csv = convert_to_list(variable_csv)
        variableunitsid = convert_to_id(cursor, 'Units', 'UNITSNAME',
                                        variable_csv[2], 'UNITSID')
        timeunitsid = convert_to_id(cursor, 'Units', 'UNITSNAME',
                                    variable_csv[8], 'UNITSID')
        variable_db = [variable_csv[0],  # variablecode
                       variable_csv[1],  # variablename
                       'Not applicable',  # speciation
                       variableunitsid,  # variableunitsid
                       variable_csv[4],  # samplemedium
                       variable_csv[5],  # valuetype
                       '1' if variable_csv[6] == 'TRUE' else '0',  # isregular
                       variable_csv[7],  # timesupport
                       timeunitsid,  # timeunitsid
                       variable_csv[3],  # datatype
                       variable_csv[9],  # general category
                       variable_csv[10]  # nodatavalue
                       ]
        nvarchars = [0, 1, 2, 4, 5, 9, 10]
        variable_labels = ['VARIABLECODE', 'VARIABLENAME',
                           'SPECIATION', 'VARIABLEUNITSID', 'SAMPLEMEDIUM',
                           'VALUETYPE', 'ISREGULAR', 'TIMESUPPORT', 'TIMEUNITSID',
                           'DATATYPE', 'GENERALCATEGORY', 'NODATAVALUE']
        variable_db = format_fields(variable_db, nvarchars)
        cursor.execute('INSERT INTO Variables ({}) VALUES ({});'.format(
            ', '.join(variable_labels), ', '.join(variable_db)))
    cursor.commit()


driver = '{ODBC Driver 13 for SQL Server}'
sql_server = os.environ['GENSERVER']
db_name = os.environ['GENDB']
user = os.environ['GENUSER']
passwd = os.environ['GENPASSWD']
cnxn = pyodbc.connect('DRIVER={};PORT={};'.format(driver, 1433) +
                      'SERVER={};PORT={};'.format(sql_server, 1443) +
                      'DATABASE={};UID={};PWD={};'.format(db_name, user, passwd))
cursor = cnxn.cursor()

if args.methods is not None:
    methods = get_csv_data(args.methods)
    post_methods(cursor, methods)
if args.sites is not None:
    sites = get_csv_data(args.sites)
    post_sites(cursor, sites)
if args.sources is not None:
    sources = get_csv_data(args.sources)
    post_sources(cursor, sources)
if args.variables is not None:
    variables = get_csv_data(args.variables)
    post_variables(cursor, variables)

if args.datavalues is not None:
    datavalues = get_csv_data(args.datavalues)
    post_datavalues(cursor, datavalues)
