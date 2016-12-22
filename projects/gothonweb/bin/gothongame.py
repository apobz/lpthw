import web
from gothonweb import map
from random import randint

urls = (
  '/game', 'GameEngine',
  '/', 'Index',
  '/login', 'User'

)

app = web.application(urls, globals())

#quips[randint(0, len(quips)-1)]

# little hack so that debug mode works with sessions
if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store,
                                  initializer={'room': None})
    web.config._session = session
else:
    session = web.config._session

render = web.template.render('templates/', base="layout",
                                globals={'randint':randint})


class Index(object):
    def GET(self):
        # this is used to "setup" the session with starting values
        session.room = map.START
        web.seeother("/game")


class GameEngine(object):

    def GET(self):
        if session.room:
            return render.show_room(room=session.room)

    def POST(self):
        form = web.input(action=None)

        # there WAS a bug here, I fixed it. I think?
        # checks to see if both a room and action are specified
        if session.room and form.action:
            # checks to see if the go method performed on the room yields a
            # result
            if session.room.go(form.action):
                session.room = session.room.go(form.action)
            # any other action will result in the death case
            else:
                session.room = session.room.go('*')

        web.seeother("/game")

if __name__ == "__main__":
    app.run()
