import argparse
import os
import pyodbc

parser = argparse.ArgumentParser()
parser.add_argument("--datavalues")
parser.add_argument("--methods")
parser.add_argument("--sites")
parser.add_argument("--sources")
parser.add_argument("--variables")
args = parser.parse_args()

batch_size = 500


def get_csv_data(csv_name):
    with open(csv_name, "r") as csv_file:
        csv_lines = csv_file.readlines()
    csv_lines = [csv_line.replace("\n", "") for csv_line in csv_lines]
    return csv_lines[1:]  # header row not needed


def convert_to_list(csv_line):
    csv_list = csv_line.split('","')
    csv_list = [csv_item.replace('"', "") for csv_item in csv_list]
    return csv_list


def pull_metadata_table(cursor, table):
    cursor.execute("SELECT * FROM {};".format(table))
    columns = [column[0] for column in cursor.description]
    return [tuple(columns)] + cursor.fetchall()


def convert_to_id(cursor, metadata_caches, table, cv_label, cv_value, id_label):
    table = metadata_caches[table]
    cv_col = table[0].index(cv_label)
    id_col = table[0].index(id_label)
    target_row = [i for i in range(0, len(table)) if table[i][cv_col] == cv_value][0]
    return table[target_row][id_col]


def format_fields(fields, nvarchars):
    formatted_fields = []
    for ind, field in enumerate(fields, 0):
        if ind in nvarchars:
            formatted_fields.append("'{}'".format(field))
        else:
            formatted_fields.append(str(field))
    return formatted_fields


def post_datavalues(cursor, datavalues_csv, metadata_caches):
    for ind, datavalue_csv in enumerate(datavalues_csv, start=1):
        datavalue_csv = convert_to_list(datavalue_csv)
        methodid = convert_to_id(
            cursor,
            metadata_caches,
            "methods",
            "MethodCode",
            datavalue_csv[8],
            "MethodID",
        )
        siteid = convert_to_id(
            cursor, metadata_caches, "sites", "SiteCode", datavalue_csv[0], "SiteID"
        )
        sourceid = convert_to_id(
            cursor,
            metadata_caches,
            "sources",
            "SourceCode",
            datavalue_csv[9],
            "SourceID",
        )
        variableid = convert_to_id(
            cursor,
            metadata_caches,
            "variables",
            "VariableCode",
            datavalue_csv[1],
            "VariableID",
        )
        datavalue_db = [
            datavalue_csv[2],  # datavalue
            datavalue_csv[3],  # localdatetime
            datavalue_csv[4],  # utcoffset
            datavalue_csv[5],  # datetimeutc
            siteid,  # siteid
            variableid,  # variableid
            datavalue_csv[7],  # censorcode
            methodid,  # methodid
            sourceid,  # sourceid
            datavalue_csv[6],  # qualitycontrollevelid
        ]
        nvarchars = [1, 3, 6]
        datavalue_db = format_fields(datavalue_db, nvarchars)
        if ind % batch_size == 1:
            datavalue_labels = [
                "DATAVALUE",
                "LOCALDATETIME",
                "UTCOFFSET",
                "DATETIMEUTC",
                "SITEID",
                "VARIABLEID",
                "CENSORCODE",
                "METHODID",
                "SOURCEID",
                "QUALITYCONTROLLEVELID",
            ]
            insert_cmd = "INSERT INTO DataValues ({}) VALUES ({})".format(
                ", ".join(datavalue_labels), ", ".join(datavalue_db)
            )
        else:
            insert_cmd += ", ({})".format(", ".join(datavalue_db))
        if ind % batch_size == 0 or ind == len(datavalues_csv):
            insert_cmd += ";"
            cursor.execute(insert_cmd)
            cursor.commit()


def post_methods(cursor, methods_csv):
    for ind, method_csv in enumerate(methods_csv, start=1):
        method_csv = convert_to_list(method_csv)
        method_db = [method_csv[1], method_csv[0]]  # methoddescription  # methodcode
        nvarchars = [0, 1]
        method_labels = ["METHODDESCRIPTION", "METHODCODE"]
        method_db = format_fields(method_db, nvarchars)
        cursor.execute(
            "INSERT INTO Methods ({}) VALUES ({});".format(
                ", ".join(method_labels), ", ".join(method_db)
            )
        )
    cursor.commit()


def post_sites(cursor, sites_csv, metadata_caches):
    for ind, site_csv in enumerate(sites_csv, start=1):
        site_csv = convert_to_list(site_csv)
        latlongdatumid = convert_to_id(
            cursor,
            metadata_caches,
            "spatialreferences",
            "SRSName",
            site_csv[6],
            "SpatialReferenceID",
        )
        site_db = [
            site_csv[0],  # sitecode
            site_csv[1],  # sitename
            site_csv[2],  # latitude
            site_csv[3],  # longitude
            latlongdatumid,  # latlongdatumid
            site_csv[7],  # elevation_m
            site_csv[5],  # state
            site_csv[4],  # county
            site_csv[8],  # sitetype
        ]
        nvarchars = [0, 1, 6, 7, 8]
        site_labels = [
            "SITECODE",
            "SITENAME",
            "LATITUDE",
            "LONGITUDE",
            "LATLONGDATUMID",
            "ELEVATION_M",
            "STATE",
            "COUNTY",
            "SITETYPE",
        ]
        site_db = format_fields(site_db, nvarchars)
        cursor.execute(
            "INSERT INTO Sites ({}) VALUES ({});".format(
                ", ".join(site_labels), ", ".join(site_db)
            )
        )
    cursor.commit()


def post_sources(cursor, sources_csv):
    for ind, source_csv in enumerate(sources_csv, start=1):
        source_csv = convert_to_list(source_csv)
        source_db = [
            source_csv[1],  # organization
            source_csv[2],  # sourcedescription
            source_csv[3],  # sourcelink
            source_csv[4],  # contactname
            "Unknown",  # phone
            source_csv[5],  # email
            "Unknown",  # address
            "Unknown",  # city
            "Unknown",  # state
            "Unknown",  # zipcode
            source_csv[6],  # citation
            "0",  # metadataid
            source_csv[0],  # sourcecode
        ]
        nvarchars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
        source_labels = [
            "ORGANIZATION",
            "SOURCEDESCRIPTION",
            "SOURCELINK",
            "CONTACTNAME",
            "PHONE",
            "EMAIL",
            "ADDRESS",
            "CITY",
            "STATE",
            "ZIPCODE",
            "CITATION",
            "METADATAID",
            "SOURCECODE",
        ]
        source_db = format_fields(source_db, nvarchars)
        cursor.execute(
            "INSERT INTO Sources ({}) VALUES ({});".format(
                ", ".join(source_labels), ", ".join(source_db)
            )
        )
    cursor.commit()


def post_variables(cursor, variables_csv, metadata_caches):
    for ind, variable_csv in enumerate(variables_csv, start=1):
        variable_csv = convert_to_list(variable_csv)
        variableunitsid = convert_to_id(
            cursor, metadata_caches, "units", "UnitsName", variable_csv[2], "UnitsID"
        )
        timeunitsid = convert_to_id(
            cursor, metadata_caches, "units", "UnitsName", variable_csv[8], "UnitsID"
        )
        variable_db = [
            variable_csv[0],  # variablecode
            variable_csv[1],  # variablename
            "Not applicable",  # speciation
            variableunitsid,  # variableunitsid
            variable_csv[4],  # samplemedium
            variable_csv[5],  # valuetype
            "1" if variable_csv[6] == "TRUE" else "0",  # isregular
            variable_csv[7],  # timesupport
            timeunitsid,  # timeunitsid
            variable_csv[3],  # datatype
            variable_csv[9],  # general category
            variable_csv[10],  # nodatavalue
        ]
        nvarchars = [0, 1, 2, 4, 5, 9, 10]
        variable_labels = [
            "VARIABLECODE",
            "VARIABLENAME",
            "SPECIATION",
            "VARIABLEUNITSID",
            "SAMPLEMEDIUM",
            "VALUETYPE",
            "ISREGULAR",
            "TIMESUPPORT",
            "TIMEUNITSID",
            "DATATYPE",
            "GENERALCATEGORY",
            "NODATAVALUE",
        ]
        variable_db = format_fields(variable_db, nvarchars)
        cursor.execute(
            "INSERT INTO Variables ({}) VALUES ({});".format(
                ", ".join(variable_labels), ", ".join(variable_db)
            )
        )
    cursor.commit()


driver = "{ODBC Driver 13 for SQL Server}"
sql_server = os.environ["GENSERVER"]
db_name = os.environ["GENDB"]
user = os.environ["GENUSER"]
passwd = os.environ["GENPASSWD"]
cnxn = pyodbc.connect(
    "DRIVER={};PORT={};".format(driver, 1433)
    + "SERVER={};PORT={};".format(sql_server, 1443)
    + "DATABASE={};UID={};PWD={};".format(db_name, user, passwd)
)
cursor = cnxn.cursor()

spatial_references = pull_metadata_table(cursor, "SpatialReferences")
metadata_caches = {"spatialreferences": spatial_references}

if args.methods is not None:
    methods = get_csv_data(args.methods)
    post_methods(cursor, methods)
if args.sites is not None:
    sites = get_csv_data(args.sites)
    post_sites(cursor, sites, metadata_caches)
if args.sources is not None:
    sources = get_csv_data(args.sources)
    post_sources(cursor, sources)

metadata_caches["methods"] = pull_metadata_table(cursor, "Methods")
metadata_caches["sites"] = pull_metadata_table(cursor, "Sites")
metadata_caches["sources"] = pull_metadata_table(cursor, "Sources")
metadata_caches["units"] = pull_metadata_table(cursor, "Units")

if args.variables is not None:
    variables = get_csv_data(args.variables)
    post_variables(cursor, variables, metadata_caches)

metadata_caches["variables"] = pull_metadata_table(cursor, "Variables")

if args.datavalues is not None:
    datavalues = get_csv_data(args.datavalues)
    post_datavalues(cursor, datavalues, metadata_caches)
