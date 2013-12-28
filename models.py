from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    city = Column(String)
    isCancon = Column(Boolean)

    def __init__(self, name, country, city, isCancon=False):
        self.name = name
        self.country = country
        self.city = city
        self.isCancon = isCancon or country == 'Canada'    

class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    artistID = Column(Integer, ForeignKey('artist.id'))
    albumDate = Column(Date)
    isCompilation = Column(Boolean)

    def __init__(self, name, artistID, date, isCompilation=False):
        self.name = name
        self.artistID = artistID
        self.albumDate = date
        self.isCompilation = isCompilation


class Track(Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True)
    albumID = Column(Integer, ForeignKey('album.id'))
    name = Column(String)
    trackNo = Column(Integer)

    def __init__(self, name, trackNo, albumID, albumArtist=None):
        self.name = name
        self.trackNo = trackNo
        self.albumID = albumID
        self.albumArtist = albumArtist


class Show(Base):
    __tablename__ = 'show'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    dj = Column(String)

    def __init__(self, name, dj):
        self.name = name
        self.dj = dj

class ShowHistory(Base):
    __tablename__ = 'showHistory'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    showID = Column(Integer, ForeignKey('show.id'))

    def __init__(self, date, showID):
        self.date = date
        self.showID = showID
    

class PlayHistory(Base):
    __tablename__ = 'playHistory'

    id = Column(Integer, primary_key=True)
    trackID = Column(Integer, ForeignKey('track.id'))
    showHistoryID = Column(Integer, ForeignKey('showHistory.id'))
    ordinal = Column(Integer)

    def __init__(self, trackID, showHistoryID, ordinal):
        self.track = trackID
        self.showHistoryID = showHistoryID
        self.ordinal = ordinal
