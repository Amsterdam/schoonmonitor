import os
#import tempfile
import subprocess
import logging
import argparse
from collections import OrderedDict

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import pandas as pd
#from shapely.geometry import Point, wkb_hex
import pyproj as proj

# setup your projections
crs_wgs = proj.Proj(init='epsg:4326') # assuming you're using WGS84 geographic
crs_rd = proj.Proj(init='epsg:28992') # use a locally appropriate projected CRS


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

LOCAL_POSTGRES_URL = URL(
    drivername='postgresql',
    username='schoonmonitor',
    password='insecure',
    host='database',
    #port='5432',
    database='schoonmonitor'
)


class NonZeroReturnCode(Exception):
    pass


def scrub(l):
    out = []
    for x in l:
        if x.strip().startswith('PG:'):
            out.append('PG: <CONNECTION STRING REDACTED>')
        else:
            out.append(x)
    return out


def run_command_sync(cmd, allow_fail=False):
    logging.debug('Running %s', scrub(cmd))
#    logging.debug('Running %s', cmd)
    p = subprocess.Popen(cmd)
    p.wait()

    if p.returncode != 0 and not allow_fail:
        raise NonZeroReturnCode

    return p.returncode


def wfs2psql(url, pg_str, layer_name, **kwargs):
    cmd = ['ogr2ogr','-overwrite','-t_srs', 'EPSG:4326', '-nln', layer_name, '-F', 'PostgreSQL', pg_str, url]
    run_command_sync(cmd)


def get_pg_str(host, user, dbname, password):
    return 'PG:host={} user={} dbname={} password={}'.format(
        host, user, dbname, password
    )


def esri_json2psql(json_filename, pg_str, layer_name, **kwargs):
    # first attempt:
    # https://gis.stackexchange.com/questions/13029/converting-arcgis-server-json-to-geojson
    cmd = ['ogr2ogr', '-t_srs', 'EPSG:28992', '-nln', layer_name, '-F', 'PostgreSQL', pg_str, json_filename]
    run_command_sync(cmd)

def load_gebieden(pg_str):
    areaNames = ['stadsdeel', 'buurt', 'buurtcombinatie', 'gebiedsgerichtwerken']
    for areaName in areaNames:
        WFS="https://map.data.amsterdam.nl/maps/gebieden?REQUEST=GetFeature&SERVICE=wfs&Version=2.0.0&SRSNAME=EPSG:4326&typename=" + areaName
        wfs2psql(WFS, pg_str , areaName)
        print(areaName + ' loaded into PG.')

# -----------------------------------------------
def load_crow(datadir):
    # This contains knowledge about the data layout
    #CROW_COLUMNS = OrderedDict([
    #    ('BU_CODE', str),
    #    ('Buurt', str),
    #    ('Kleur', str),
    #])

    # datadir = 'data/aanvalsplan_schoon/crow'
    files = os.listdir(datadir)
    files_xls = [f for f in files if f[-4:] == 'xlsx']
    print(files_xls)

    # Load all files into 1 big dataframe with lat lon as 4326
    df = pd.DataFrame()
    for f in files_xls:
        data = pd.read_excel(datadir + '/' + f)
        if ('Schouwronde') not in data.columns:
            data['Schouwronde'] = f
        #print(data.columns)
        # duplicate lat/lon
        if ('Latitude') in data.columns:
            data['lat'] = data['Latitude']
            data['lon'] = data['Longitude']
        # duplicate Breedtegraad
        if ('Breedtegraad') in data.columns:
            data['lat'] = data['Breedtegraad']
            data['lon'] = data['Lengtegraad']
        # convert RD bbox to lat lon, but skip 2014-2017 which is already converted
        if ('minx') in data.columns and ('lat') not in data.columns:
            data['RD-X'] = (data['minx'] + data['maxx']) / 2
            data['RD-Y'] = (data['miny'] + data['maxy']) / 2
            print(data)
            # convert RD N to WGS84 into Series
            #latlon = data.apply(lambda row: proj.transform(crs_rd, crs_wgs, row['RD-X'], row['RD-Y']), axis=1).apply(pd.Series)
            #print(latlon)
            #latlon.rename(columns={0: "lat", 1: "lon"}, inplace=True)
            #print(latlon)
            # Merge with dataFrame
            #data = pd.concat([data,latlon], axis=1)
            #print(data)
        df = df.append(data)
        print("added " + f)
    
    # change column to datatime
    print(df.columns)
    #df['Aanmaakdatum_score']= df['Aanmaakdatum_score'].apply(pd.to_datetime)
    # Create shapely point object
    #geometry = [Point(xy) for xy in zip(df['lat'], df['lon'])]
    # Convert to lossless binary to load properly into Postgis
    #df['geom'] = geometry.wkb_hex
    df.rename(columns={'Well ID (customer)': 'Well ID customer'},inplace=True)


    # Write our data to database
    tableName = 'crowscores'
    engine = create_engine(LOCAL_POSTGRES_URL)
    df.to_sql(tableName, engine, if_exists='replace') #,  dtype={geom: Geometry('POINT', srid='4326')})
    print(tableName + ' added')

def main(datadir):
    pg_str = get_pg_str('database', 'schoonmonitor', 'schoonmonitor', 'insecure')
    #path = os.getcwd()
    load_crow(datadir)
    load_gebieden(pg_str)
if __name__ == '__main__':
    desc = 'Upload crow datasets into PostgreSQL.'
    parser = argparse.ArgumentParser(desc)
    parser.add_argument(
        'datadir', type=str, help='Local data directory', nargs=1)
    args = parser.parse_args()
    main(args.datadir[0])