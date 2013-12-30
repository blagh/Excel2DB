import argparse, sys
import xlrd, sqlite3
import dateutil.parser
from os import listdir
from os.path import isfile, join
from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.sql import func

# fill database from xls files in directory
def readXls(directory, database, recursive=False):
    
    engine = create_engine(database, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    # TODO: check if tables already exist
    Base.metadata.create_all(engine)
    
    for fileName in listdir(directory):
        # open file
        fileName = join(directory, fileName)
        
        if isfile(fileName) and \
            (fileName.endswith('.xls') or fileName.endswith('.xlsx')):
            # extract show info
            readXlsFile(fileName, session)

    session.commit()

##    for show in session.query(Show):
##        print show.id, show.name, show.dj
##
##    for artist in session.query(Artist).order_by(Artist.name):
##        print artist.id, artist.name, artist.isCancon
    
    playHistory = session.query(Album.id, func.count('*').label('play_count')) \
                         .join(Track).join(PlayHistory) \
                         .group_by(Album.id) \
                         .subquery()

    #albumCount = session.query(Album, func.sum(playHistory.play_count).label('album_count')) \
    #                    .join(trackAlias, Album.tracks)

    i = 1
    #for track, count in session.query(Track, playHistory.c.play_count).\
    #                            outerjoin(playHistory, Track.id==playHistory.c.track_id).\
    #                            order_by(playHistory.c.play_count):
    #    print i, count, track.album.artist.name, track.album.name, track.name
    for album, count in session.query(Album, playHistory.c.play_count).\
                                outerjoin(playHistory, Album.id==playHistory.c.id).\
                                order_by(playHistory.c.play_count.desc())[:100]:
        print i, ":", count, "x", album.artist.name, "/", album.name, "\n\t", album.tracks
        i += 1
    

def readXlsFile(fileName, session):
    shows = []
    tracks = []
    
    with open(fileName, 'rb') as f:
        
        wb = xlrd.open_workbook(file_contents=f.read())
        s = wb.sheets()[0]

        readShowHistory(s, fileName, session)

def readShowHistory(sheet, fileName, db):
    # get show from database or create
    djName = sheet.cell(2,2).value
    showName = sheet.cell(3,2).value
    showDate = None
    try:
        showDate = dateutil.parser.parse(sheet.cell(2,8).value)
    except:
        try:
            showDate = dateutil.parser.parse(fileName[-14:-4])
        except:
            print fileName[-14:-4]
            print "Could not get show date from " + fileName
            return
    showTime = sheet.cell(3,8).value

    show = db.query(Show).filter(Show.dj.like(djName), Show.name.like(showName)).first()
    if (show == None):
        
        show = Show(showName, djName)
        db.add(show)

    #print show.id, show.name, show.dj, showDate, showTime

    # create new show history
    # TODO: check for existing show history on same date / time. merge / ignore?
    showHistory = ShowHistory(showDate, showTime, show)

    # for each row in playlist area
    ordinal = 1
    for row in range(11, sheet.nrows):
        
        artistName = clean(sheet.cell(row, 1).value)
        albumName = clean(sheet.cell(row, 3).value)
        
        trackName = clean(sheet.cell(row, 2).value)
        trackDuration = sheet.cell(row, 4)
        
        playOrder = sheet.cell(row, 0)
        playTime = sheet.cell(row, 5)
        
        logCategory = sheet.cell(row, 6)
        try:
            logCategory = int(logCategory.value)
        except ValueError: pass
        
        isCancon = sheet.cell(row, 7).value != ""
        isHit = sheet.cell(row, 8)
        isChart = sheet.cell(row, 9)
        chartCategory = sheet.cell(row, 10)

        if (logCategory > 20 and logCategory < 50 # this is a song, not talk or ad content
            and playOrder.ctype==xlrd.XL_CELL_NUMBER # have not yet reached the end of the playlist
            and artistName != "" and trackName != "" # and there is at least artist and track data
            ):

            #print
            #print "******", playOrder.value, artistName, albumName, trackName, isCancon
            #print

            # get or create artist / album / track
            artist = db.query(Artist).filter(Artist.name.like(artistName)).first()            
            if (artist == None):
                artist = Artist(artistName, "", "", isCancon != "")

            album = None
            if (artist.id > 0):
                album = db.query(Album).filter(Album.name.like(albumName)).filter(Album.artist_id == artist.id).first()
            if (album == None):
                album = Album(albumName, artist)

            track = None
            if (album.id > 0):
                track = db.query(Track).filter(Track.name.like(trackName)).filter(Track.album_id == album.id).first()
            if (track == None):
                track = Track(trackName, album)

            # create new play history
            playHistory = PlayHistory(showHistory, track, ordinal)
            ordinal += 1

    # save all
    db.add(showHistory)    

# output stats (to xls?)
   # top 100 artists/tracks/albums for year/month/arbitrary time period

# given music library, create playlists
# given music library, fill in database

def clean(name):    
    # replace '&' with 'and'    
    name = name.replace("&", "and")
    
    # remove periods, commas, hyphens, exclamation points
    name = name.replace(". ", " ")
    name = name.replace(".", " ")
    name = name.replace(", ", " ")
    name = name.replace(",", " ")
    name = name.replace("- ", " ")
    name = name.replace("-", " ")
    name = name.replace("!", "")

    # remove EP from end of album
    if name[-3:] == " EP": name = name[:-3]

    # title case
    name = name.title()

    # remove leading/trailing whitespace
    name = name.strip()

    return name

if __name__=="__main__":
    class ArgParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)
    
    parser = ArgParser(description='Playlist Statifier')
    
    parser.add_argument('action', choices=['read', 'create', 'stats', 'fill', 'playlist'])    
    parser.add_argument('-f', '--folder', help='read location of xls files',
                        default='./', metavar='F')
    parser.add_argument('-db', '--database', help='name of the database',
                        default='sqlite:///:memory:', metavar='DB')

    args = parser.parse_args()
    print args

    if args.action == "read":
        readXls(args.folder, args.database)
    
    
