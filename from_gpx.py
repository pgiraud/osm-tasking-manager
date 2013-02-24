#!/Users/pierregiraud/Sites/osm-tasking-manager/env/bin/python
__requires__ = 'OSMTM'

import os
import sys
import transaction
import pyproj
from xml.dom import minidom

from sqlalchemy import create_engine

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from OSMTM.models import (
    DBSession,
    Job,
    Tile,
    TileHistory,
    Base,
    )

from OSMTM.utils import *

z = 15

engine = create_engine('sqlite:///OSMTM.db')
DBSession.configure(bind=engine)
with transaction.manager:
    job = DBSession.query(Job).filter(Job.id==194).one()
    DBSession.delete(job)
    job = DBSession.query(Job).filter(Job.id==196).one()
    DBSession.delete(job)
    
    jobs = DBSession.query(Job).all()
    print jobs

    job = Job(u'Mali buildings (crowdsource)', 'MULTIPOLYGON(((0 0, 0 1, 1 1, 0 0)))', z)
    DBSession.add(job)

    xmldoc = minidom.parse('/tmp/missingplaces-new.gpx')

    coords = []
    minx = None
    miny = None
    maxx = None
    maxy = None
    for wpt  in xmldoc.getElementsByTagName('wpt'):
        lon = float(wpt.attributes['lon'].value)
        lat = float(wpt.attributes['lat'].value)
        p1 = pyproj.Proj(init='epsg:4326')
        p2 = pyproj.Proj(init='epsg:3857')
        lon, lat = pyproj.transform(p1, p2, lon, lat)
        minx = min(minx, lon) if minx is not None else lon
        miny = min(miny, lat) if miny is not None else lat
        maxx = max(maxx, lon) if maxx is not None else lon
        maxy = max(maxy, lat) if maxy is not None else lat

        step = max_/(2**(z - 1))
        x = int(floor((lon+max_)/step))
        y = int(floor((lat+max_)/step))
        if not (x, y) in coords:
            coords.append((x, y))
    job.geometry = 'MULTIPOLYGON(((%f %f, %f %f, %f %f, %f %f, %f %f)))' % \
        (minx, miny, minx, maxy, maxx, maxy, maxx, miny, minx, miny)
    DBSession.add(job)

    tiles = []
    for x, y in coords:
        tiles.append(Tile(x, y, z))
    job.tiles = tiles
