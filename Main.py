#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import datetime
from sqlalchemy import create_engine
import urllib2


from tornado.options import define, options


define("port", default=12345, help = "Check localhost:12345", type = int)
application_settings = {"debug": True,
                        "static_path": os.path.join(os.path.dirname(__file__), "static"),
                       }
db = create_engine('postgresql://postgres:root@localhost:5432/postgres')


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
        artists = db.execute('SELECT * FROM music_catalog.artists WHERE deleted <> TRUE ORDER BY name')

        self.render("templates/music_catalog/artists.html",
                    artists = artists)

class ArtistPageHandler(tornado.web.RequestHandler):
    def get(self):
        uri = self.request.uri
        artist_name = uri.split('/')[-1]
        albums = db.execute('SELECT * FROM music_catalog.albums WHERE artist_id = (SELECT id FROM music_catalog.artists WHERE lower(name) = lower(%s) AND deleted != TRUE)', artist_name)

        self.render("templates/music_catalog/albums.html",
                    artist_name = urllib2.unquote(artist_name),
                    albums = albums)


class AjaxEcho(tornado.web.RequestHandler):
    #@is_ajax # is_ajax decorators.
    def get(self):
        if (self.get_argument("f", default=None, strip=False) == "getSimpleAnswer"):
            result = str(datetime.datetime.now().time().isoformat()) + " SimpleAnswer: OK!"
            json_result = '{{"result": "{0}"}}'.format(result)
            self.write(json_result)
        else:
            result = str(datetime.datetime.now().time().isoformat()) + " This function is not implemented yet"
            json_result = '{{"result": "{0}"}}'.format(result)
            self.write(json_result)


def main():
    print "Visit localhost:12345"

    tornado.options.parse_command_line()

    application = tornado.web.Application(
        [
            (r"/", HomePageHandler),
            (r"/server", AjaxEcho),
            (r"/artists/", ArtistsPageHandler),
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