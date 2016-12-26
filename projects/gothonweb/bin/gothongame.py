from gothonweb import map, populator as p
import os.path
from random import randint
import web
from web import form

urls = (
  '/start', 'Start',
  '/game', 'GameEngine',
  '/', 'Index',
  '/login', 'Login',
  '/logout', 'Logout',
  '/signup', 'Signup',
)

app = web.application(urls, globals())

# Hack to make session play nice with the reloader (in debug mode)
if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store,
                                  initializer={'room': None})
    web.config._session = session
else:
    session = web.config._session

render = web.template.render('templates/', base="layout",
                             globals={'randint': randint})


fbox = form.Form(
    form.Textbox('Username', form.notnull),
    form.Password('Password', form.notnull),
    form.Button('Login'),
)

sign = form.Form(
    form.Textbox('Username', form.notnull),
    form.Password('Password', form.notnull),
    form.Password('password_rep', form.notnull),
    form.Button('Register'),
    validators = {
        form.Validator("Passwords did not match.",
        lambda i: i.Password == i.password_rep)
    }
)

user_db = os.path.join(os.path.expanduser('~'), 'learning', 'lcthw', 'lpthw',
                                'projects', 'gothonweb', 'docs', 'user_db.csv')
p.create_db(user_db)

class Index(object):
    # Give user the option to logout, or start the game
    def GET(self):
        if session.get('logged_in', False):
            return """<h1>You are already logged in!</h1>
                    <a href="/logout">Logout</a>
                    or
                    <a href='/start'>Start the game!</a>"""

        return """<h1>Gothons from Planet Percal #25</h1>
            <pre>You are not logged in. To begin, go to the login page. Or
            sign up!</pre>
            <a href='/login'>Login</a>
            <a href='/signup'>Sign up</a>"""
        # maybe do this in the game eventually:
        # return render.something() or html text with link to next step: /game

class Signup:

    def GET(self):
        s = sign()
        return render.windex(s, None)

    def POST(self):
        s = sign()

        if s.validates():
            # check for duplicate usernames
            vals = {'usrnm': s.d.Username, 'pw': s.d.Password, 'h_score': 0}
            is_accepted = p.popl(user_db, vals)
            # if popl returns False, username is unique
            if not is_accepted:
                # take POST data and add to user db
                session.logged_in = True
                return """<h1>You've signed up!</h1><pre> Welcome %s.
                    </pre><a href="/logout">Logout</a>""" % (s.d.Username)
            else:
                return render.windex(s, is_accepted)
        else:
            return render.windex(s, None)

class Login(object):

    def GET(self):
        if session.get('logged_in', False):
            raise web.seeother('/start')

        f = fbox()
        return render.windex(f, None)

    def POST(self):
        f = fbox()

        if not f.validates():
            return render.windex(f, None)

        # authenticate credentials here
        if p.auth(user_db, f.d.Username, f.d.Password):
            session.logged_in = True
            return """<h1>Login success!</h1><pre> Welcome %s.</pre>
                    <a href="/logout">Logout</a>
                    or
                    <a href='/start'>Start the game!</a>""" % (f.d.Username)

            # creds = p.get_creds()
            # return render.start(creds)
        else:
            session.logged_in = False
            return """<h1>Login failed!</h1>
                   <a href='/login'>Return to login</a> Don't have a profile?
                   <a href='/signup'>Signup!</a>"""

class Logout(object):

    def GET(self):
        session.logged_in = False
        session.kill()
        raise web.seeother('/')

class Start(object):

    def GET(self):
        if not session.get('logged_in', False):
            raise web.seeother('/')

        session.room = map.START
        raise web.seeother('/game')

class GameEngine(object):

    def GET(self):
        if not session.get('logged_in', False):
            raise web.seeother('/')

        if session.room:
            return render.show_room(room=session.room)

    def POST(self):
        move = web.input(action=None)

        # there WAS a bug here, I fixed it. I think?
        # checks to see if both a room and action are specified
        if session.room and move.action:
            # checks to see if the go method performed on the room yields a
            # result
            if session.room.go(move.action):
                session.room = session.room.go(move.action)
            # any other action will result in the death case
            else:
                session.room = session.room.go('*')

        web.seeother("/game")


if __name__ == "__main__":
    app.run()
