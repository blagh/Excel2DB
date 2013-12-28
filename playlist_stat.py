import argparse, sys
import xlrd, sqlite3
import dateutil.parser
from os import listdir
from os.path import isfile, join
from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# fill database from xls files in directory
def readXls(directory, database, recursive=False):
    
    engine = create_engine(database, echo=True)
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
    

def readXlsFile(fileName, session):
    shows = []
    tracks = []
    
    with open(fileName, 'rb') as f:
        
        wb = xlrd.open_workbook(file_contents=f.read())
        s = wb.sheets()[0]

        readShowHistory(s, session)

    for show in session.query(Show):
        print show.id, show.name, show.dj

    for artist in session.query(Artist):
        print artist.id, artist.name, artist.isCancon

def readShowHistory(sheet, db):
    # get show from database or create
    djName = sheet.cell(2,2).value
    showName = sheet.cell(3,2).value
    showDate = dateutil.parser.parse(sheet.cell(2,8).value)
    showTime = sheet.cell(3,8).value

    show = db.query(Show).filter(Show.dj.like(djName), Show.name.like(showName)).first()
    if (show == None):
        
        show = Show(showName, djName)
        db.add(show)

    print show.id, show.name, show.dj, showDate, showTime

    # create new show history
    # TODO: check for existing show record on same date
    showHistory = ShowHistory(showDate, showTime, show)

    # for each row in playlist area
    for row in range(11, sheet.nrows):
        
        artistName = sheet.cell(row, 1).value
        albumName = sheet.cell(row, 3).value
        
        trackName = sheet.cell(row, 2).value      
        trackDuration = sheet.cell(row, 4)
        
        playOrder = sheet.cell(row, 0)
        playTime = sheet.cell(row, 5)
        
        logCategory = sheet.cell(row, 6)
        try:
            logCategory = int(logCategory.value)
        except ValueError: pass
        
        isCancon = sheet.cell(row, 7)
        isHit = sheet.cell(row, 8)
        isChart = sheet.cell(row, 9)
        chartCategory = sheet.cell(row, 10)

        ordinal = 1

        if (logCategory > 20 and logCategory < 50 # this is a song, not talk or ad content
            and playOrder.ctype==xlrd.XL_CELL_NUMBER # have not yet reached the end of the playlist
            and artistName != "" and trackName != "" # and there is at least artist and track data
            ):

            print playOrder.value, artistName.value, albumName.value, trackTitle.value

            # get or create artist / album / track
            artist = db.query(Artist).filter(Artist.name.like(artistName)).first()
            if (artist == None):
                artist = Artist(artistName, "", "", isCancon != "")

            album = db.query(Album).filter(Album.name.like(albumName) and Album.artist == artist).first()
            if (album == None):
                album = Album(albumName, artist)

            track = db.query(Track).filter(Track.name.like(trackName) and Track.album == album).first()
            if (track == None):
                track = Track(trackName, album)

            # create new play history
            playHistory = PlayHistory(showHistory, track, ordinal)
            ordinal += 1

    # save all
    db.add(showHistory)    

# create database

# output stats (to xls?)
   # top 100 artists/tracks/albums for year/month/arbitrary time period

# given music library, create playlists
# given music library, fill in database


if __name__=="__main__":
    class ArgParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)
    
    parser = ArgParser(description='Playlist Statifier')
    
    parser.add_argument('action', choices=['read', 'create', 'stats', 'fill', 'playlist'])    
    parser.add_argument('-f', '--folder', help='read location of xls files',
                        nargs=1, default='./', metavar='F')
    parser.add_argument('-db', '--database', help='name of the database',
                        nargs=1, default='sqlite:///:memory:', metavar='DB')

    args = parser.parse_args()
    print args

    if args.action == "read":
        readXls(args.folder[0], args.database)
    
    
