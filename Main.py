#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import json
import urllib2

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy import Table, MetaData
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound





from tornado.options import define, options


define("port", default=12345, help = "Check localhost:12345", type = int)
application_settings = {"debug": True,
                        "static_path": os.path.join(os.path.dirname(__file__), "static"),
                       }
db = create_engine('postgresql://postgres:root@localhost:5432/postgres')
db_meta = MetaData(bind=db, schema='music_catalog', reflect=True)
orm_session = orm.Session(bind=db)


class Artist(object):
    pass


orm.Mapper(Artist, db_meta.tables['music_catalog.artists'])


class Album(object):
    pass


orm.Mapper(Album, db_meta.tables['music_catalog.albums'])


class HomePageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/home.html",
                    title="Praise the sun!")

class Echo1PageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/examples/echo1.html")

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_body_argument("inputMessage"))


class Echo2PageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/examples/echo2.html")


class ArtistsPageHandler(tornado.web.RequestHandler):
    def get(self):
        artists = (orm_session.query(Artist)
                              .order_by(Artist.name)
                              .filter(Artist.deleted != True))

        self.render("templates/music_catalog/artists.html",
                    artists = artists)

class ArtistPageHandler(tornado.web.RequestHandler):
    def get(self):
        uri = self.request.uri
        artist_name = uri.split('/')[-1]

        albums = (orm_session.query(Album)
                             .join(Artist, Album.artist_id == Artist.id)
                             .filter(func.lower(Artist.name) == artist_name.lower())
                             .order_by(Album.year))

        self.render("templates/music_catalog/albums.html",
            artist_name = urllib2.unquote(artist_name),
            albums = albums)


class AddArtistPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/music_catalog/add_artist.html")


class DeleteArtistPageHandler(tornado.web.RequestHandler):
    def get(self):
        uri = self.request.uri
        artist_id = uri.split('/')[-1]

        try:
            artist = (orm_session.query(Artist)
                                 .filter(Artist.id == artist_id)
                                .one())

            self.render("templates/music_catalog/delete_artist.html",
                        artist = artist)
        except NoResultFound, e:
            pass #TODO сделать ex


class UpdateArtistPageHandler(tornado.web.RequestHandler):
    def get(self):
        uri = self.request.uri
        artist_id = uri.split('/')[-1]

        try:
            artist = (orm_session.query(Artist)
                                 .filter(Artist.id == artist_id)
                                 .one())

            self.render("templates/music_catalog/update_artist.html",
                        artist = artist)
        except NoResultFound, e:
            pass #TODO сделать ex


class AjaxEcho(tornado.web.RequestHandler):
    def get(self):
        function_name = self.get_argument("f", default=None, strip=False)

        handlers = {
            'getSimpleAnswer': self.get_simple_answer,
            'getArtist': self.get_artist,
            'ifArtistExist': self.if_artist_exist,
            'insertArtist': self.insert_artist,
            'deleteArtist': self.delete_artist,
            'updateArtist': self.update_artist,
        }
        default_handler = lambda: {'result': 'not implemented'}

        handler = handlers.get(function_name, default_handler)
        self.write(handler())
        return

    def get_simple_answer(self):
        result = str(datetime.datetime.now().time().isoformat()) + " SimpleAnswer: OK!"
        json_result = json.dumps({"result": result})
        return json_result

    def get_artist(self):
        result = "false"

        artist_id = self.get_argument("id", default=None, strip=False)

        try:
            artist = (orm_session.query(Artist)
                                 .filter(Artist.id == artist_id)
                                 .one())

            json_result = json.dumps({"id": artist.name.id, "name": artist.name})
        except NoResultFound, e:
            json_result = json.dumps({"result": "NoResultFound"})

        return json_result

    def if_artist_exist(self):
        result = "false"

        artist_name = self.get_argument("name", default=None, strip=False)

        artists = (orm_session.query(Artist)
                              .filter(func.lower(Artist.name) == artist_name.lower())
                              .filter(Artist.deleted != True))

        if (artists.count() > 0):
            result = "true"

        json_result = json.dumps({"result": result})
        return json_result

    def insert_artist(self):
        result = -1

        artist_name = self.get_argument("name", default=None, strip=False)

        newArtist = Artist()
        newArtist.name = artist_name

        orm_session.add(newArtist)
        orm_session.commit()

        result = newArtist.id

        json_result = json.dumps({"id": result})
        return json_result

    def delete_artist(self):
        artist_id = self.get_argument("id", default=None, strip=False)

        artist = (orm_session.query(Artist)
                             .filter(Artist.id == artist_id)
                             .one())

        artist.deleted = True
        orm_session.commit()

        json_result = json.dumps({"result": "ok"})

        return json_result

    def update_artist(self):
        artist_id = self.get_argument("id", default=None, strip=False)
        artist_name = self.get_argument("name", default=None, strip=False)

        artist = (orm_session.query(Artist)
                             .filter(Artist.id == artist_id)
                             .one())

        artist.name = artist_name

        orm_session.commit()

        json_result = {"result": "ok"}

        return json_result


def main():
    print "Visit localhost:12345"

    tornado.options.parse_command_line()

    application = tornado.web.Application(
        [
            (r"/", HomePageHandler),
            (r"/server", AjaxEcho),
            (r"/artists", ArtistsPageHandler),
            (r"/artists/", ArtistsPageHandler),
            (r"/AddArtist", AddArtistPageHandler),
            (r"/AddArtist/", AddArtistPageHandler),
            (r"/DeleteArtist/.*", DeleteArtistPageHandler),
            (r"/UpdateArtist/.*", UpdateArtistPageHandler),
            (r"/artists/.*", ArtistPageHandler),
            (r"/examples/echo1.html", Echo1PageHandler),
            (r"/examples/echo2.html", Echo2PageHandler),
        ],
        **application_settings)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()




if __name__ == "__main__":
    main()