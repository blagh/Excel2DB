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
    
    #xls = [ f for f in listdir(directory) if isfile(join(directory,f)) ]
    for fileName in listdir(directory):
        # open file
        fileName = join(directory, fileName)
        
        if isfile(fileName) and \
            (fileName.endswith('.xls') or fileName.endswith('.xlsx')):
            # extract date, show info
            readXlsFile(fileName, session)                
    

def readXlsFile(fileName, session):
    shows = []
    tracks = []
    
    with open(fileName, 'rb') as f:
        
        wb = xlrd.open_workbook(file_contents=f.read())
        s = wb.sheets()[0]

        readShowHistory(s)
        
##	print 'Sheet:',s.name
##	for row in range(s.nrows):
##	    values = []
##	    print '\t'.join(chr(i + 97) for i in range(s.ncols))
##	    for col in range(s.ncols):                
##		values.append(unicode(s.cell(row,col).value))
##	    try: print str(row) + ": " + '\t'.join(values)
##	    except: pass
##	print


def readShowHistory(sheet, db):
    # get show from database or create
    dj = sheet.cell(2,2).value
    showName = sheet.cell(3,2).value
    date = dateutil.parser.parse(sheet.cell(2,8).value)
    time = sheet.cell(3,8).value

    print dj, showName, date, time
    
    # create new show history
    # check for existing show record on same date

    # for each row in playlist area
        # get artist / album / track or create
        # create new track history

    # save all

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
    
    
