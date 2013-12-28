from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship, backref
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
    albumDate = Column(Date, nullable=True)
    isCompilation = Column(Boolean)

    artist_id = Column(Integer, ForeignKey('artist.id'))
    artist = relationship("artist", backref = backref("albums", order_by=id))

    def __init__(self, name, artist, date=None, isCompilation=False):
        self.name = name
        self.artist = artist
        self.albumDate = date
        self.isCompilation = isCompilation


class Track(Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    trackNo = Column(Integer)

    album_id = Column(Integer, ForeignKey('album.id'))
    album = relationship("album", backref = backref("tracks", order_by=trackNo))

    def __init__(self, name, album, trackNo=0):
        self.name = name
        self.trackNo = trackNo
        self.album = album


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
    time = Column(String)

    show = relationship("show", backref = backref("history", order_by=date))

    def __init__(self, date, time, show):
        self.date = date
        self.show = show
        self.time = time
    

class PlayHistory(Base):
    __tablename__ = 'playHistory'

    id = Column(Integer, primary_key=True)
    ordinal = Column(Integer)

    showHistoryID = Column(Integer, ForeignKey('showHistory.id'))
    showHistory = relationship("showHistory", backref = backref("playlist", order_by=ordinal))

    trackID = Column(Integer, ForeignKey('track.id'))
    track = relationship("track", backref = backref("history", order_by=id))

    def __init__(self, showHistory, track, ordinal):
        self.track = track
        self.showHistory = showHistory
        self.ordinal = ordinal
