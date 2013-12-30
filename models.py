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
    artist = relationship("Artist", backref = backref("albums", order_by=id))

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
    album = relationship("Album", backref = backref("tracks", order_by=trackNo))

    def __init__(self, name, album, trackNo=0):
        self.name = name
        self.trackNo = trackNo
        self.album = album

    def __repr__(self):
        return self.name


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
    time = Column(String)

    show_id = Column(Integer, ForeignKey('show.id'))
    show = relationship("Show", backref = backref("history", order_by=date))

    def __init__(self, date, time, show):
        self.date = date
        self.show = show
        self.time = time
    

class PlayHistory(Base):
    __tablename__ = 'playHistory'

    id = Column(Integer, primary_key=True)
    ordinal = Column(Integer)

    showHistory_id = Column(Integer, ForeignKey('showHistory.id'))
    showHistory = relationship("ShowHistory", backref = backref("playlist", order_by=ordinal))

    track_id = Column(Integer, ForeignKey('track.id'))
    track = relationship("Track", backref = backref("history", order_by=id))

    def __init__(self, showHistory, track, ordinal):
        self.track = track
        self.showHistory = showHistory
        self.ordinal = ordinal
