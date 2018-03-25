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
        datavalue_db = [ind,  # valueid
                        datavalue_csv[2],  # datavalue
                        '',  # valueaccuracy
                        datavalue_csv[3],  # localdatetime
                        datavalue_csv[4],  # utcoffset
                        datavalue_csv[5],  # datetimeutc
                        siteid,  # siteid
                        variableid,  # variableid
                        '',  # offsetvalue
                        '',  # offsettypeid
                        datavalue_csv[7],  # censorcode
                        '',  # qualifierid
                        methodid,  # methodid
                        sourceid,  # sourceid
                        '',  # sampleid
                        '',  # derivedfromid
                        datavalue_csv[6]  # qualitycontrollevelid
                        ]
        nvarchars = [3, 5, 10]  # no 2 b/c empty
        datavalue_labels = ['VALUEID', 'DATAVALUE', 'VALUEACCURACY',
                            'LOCALDATETIME', 'UTCOFFSET', 'DATETIMEUTC',
                            'SITEID', 'VARIABLEID', 'OFFSETVALUE',
                            'OFFSETTYPEID', 'CENSORCODE', 'QUALIFIERID',
                            'METHODID', 'SOURCEID', 'SAMPLEID', 'DERIVEDFROMID',
                            'QUALITYCONTROLLEVELID']
        datavalue_db = format_fields(datavalue_db, nvarchars)
        print('INSERT INTO DataValues ({}) VALUES ({});'.format(
            ', '.join(datavalue_labels), ', '.join(datavalue_db)))


def post_methods(cursor, methods_csv):
    for ind, method_csv in enumerate(methods_csv, start=1):
        method_csv = convert_to_list(method_csv)
        method_db = [ind,  # methodid
                     method_csv[1],  # methoddescription
                     '',  # methodlink
                     method_csv[0]  # methodcode
                     ]
        nvarchars = [1, 3]  # no 2 b/c empty
        method_labels = ['METHODID', 'METHODDESCRIPTION', 'METHODLINK', 'METHODCODE']
        method_db = format_fields(method_db, nvarchars)
        print('INSERT INTO Methods ({}) VALUES ({});'.format(
            ', '.join(method_labels), ', '.join(method_db)))


def post_sources(cursor, sources_csv):
    for ind, source_csv in enumerate(sources_csv, start=1):
        source_csv = convert_to_list(source_csv)
        source_db = [ind,  # sourceid
                     source_csv[1],  # organization
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
        nvarchars = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13]
        source_labels = ['SOURCEID', 'ORGANIZATION', 'SOURCEDESCRIPTION',
                         'SOURCELINK', 'CONTACTNAME', 'PHONE', 'EMAIL',
                         'ADDRESS', 'CITY', 'STATE', 'ZIPCODE', 'CITATION',
                         'METADATAID', 'SOURCECODE']
        source_db = format_fields(source_db, nvarchars)
        print('INSERT INTO Sources ({}) VALUES ({});'.format(
            ', '.join(source_labels), ', '.join(source_db)))


def post_sites(cursor, sites_csv):
    for ind, site_csv in enumerate(sites_csv, start=1):
        site_csv = convert_to_list(site_csv)
        latlongdatumid = convert_to_id(cursor, 'SpatialReferences', 'SRSNAME',
                                       site_csv[6], 'SpatialReferenceID')
        site_db = [ind,  # siteid
                   site_csv[0],  # sitecode
                   site_csv[1],  # sitename
                   site_csv[2],  # latitude
                   site_csv[3],  # longitude
                   latlongdatumid,  # latlongdatumid
                   site_csv[7],  # elevation_m
                   '',  # vertical_datum
                   '',  # localx
                   '',  # localy
                   '',  # localprojectionid
                   '',  # posaccuracy_m
                   site_csv[5],  # state
                   site_csv[4],  # county
                   '',  # comments
                   site_csv[8]  # site_type
                   ]
        nvarchars = [1, 2, 15]  # no 7, 12, 13, or 14 b/c empty
        site_labels = ['SITEID', 'SITECODE', 'SITENAME', 'LATITUDE', 'LONGITUDE',
                       'LATLONGDATUMID', 'ELEVATION_M', 'VERTICAL_DATUM', 'LOCALX',
                       'LOCALY', 'LOCALPROJECTIONID', 'POSACCURACY_M', 'STATE',
                       'COUNTY', 'COMMENTS', 'SITE_TYPE']
        site_db = format_fields(site_db, nvarchars)
        print('INSERT INTO Sites ({}) VALUES ({});'.format(
            ', '.join(site_labels), ', '.join(site_db)))


def post_variables(cursor, variables_csv):
    for ind, variable_csv in enumerate(variables_csv, start=1):
        variable_csv = convert_to_list(variable_csv)
        variableunitsid = convert_to_id(cursor, 'Units', 'UNITSNAME',
                                        variable_csv[2], 'UNITSID')
        timeunitsid = convert_to_id(cursor, 'Units', 'UNITSNAME',
                                    variable_csv[8], 'UNITSID')
        variable_db = [ind,  # variableid
                       variable_csv[0],  # variablecode
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
        nvarchars = [1, 2, 3, 5, 6, 10, 11]
        variable_labels = ['VARIABLEID', 'VARIABLECODE', 'VARIABLENAME',
                           'SPECIATION', 'VARIABLEUNITSID', 'SAMPLEMEDIUM',
                           'VALUETYPE', 'ISREGULAR', 'TIMESUPPORT', 'TIMEUNITSID',
                           'DATATYPE', 'GENERALCATEGORY', 'NODATAVALUE']
        variable_db = format_fields(variable_db, nvarchars)
        print('INSERT INTO Variables ({}) VALUES ({});'.format(
            ', '.join(variable_labels), ', '.join(variable_db)))


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
