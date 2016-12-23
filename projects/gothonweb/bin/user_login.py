""" Messing around with a simple user login system using web.py
"""
import os.path
from gothonweb import populator as p
import web
from web import form

registry = os.path.join(os.path.expanduser('~'), 'learning', 'lcthw', 'lpthw',
                                'projects', 'gothonweb', 'docs', 'user_db.csv')
                                
urls = (
    '/', 'Index',
    '/login', 'Login',
    '/logout', 'Logout',
    '/signup', 'Signup',
)

web.config.debug = False
app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'))

render = web.template.render('templates/', base="layout_3")

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

a = [
    {'usrnm': 'foo', 'pw': 'bar', 'h_score': 0},
    {'usrnm': 'baz', 'pw': 'qux', 'h_score': 0},
]

allowed = (
    ('foo', 'bar'),
    ('baz', 'qux')
)


class Signup:
    def GET(self):
        s = sign()
        return render.windex(s)

    def POST(self):
        s = sign()

        usrnm = s['Username'].value
        pw = s['Password'].value
        if s.validates():
            # take POST data and add to user registry
            session.logged_in = True
            vals = {'usrnm': s.d.Username, 'pw': s.d.Password, 'h_score': 0}
            p.popl(registry, vals)
            return """<h1>You've signed up!</h1><pre> Welcome %s.
                </pre><a href="/logout">Logout</a>""" % (s.d.Username)
            # return "username: %s, password: %s" % (s.d.Username, s.d.Password)
        else:
            return render.windex(s)
            # return "<pre>For some reason you ended up here :/</pre>"


class Index:
    # Give user the option to logout, or start the game
    def GET(self):
        if not session.get('logged_in', False):
            return """<h1>Logged out!</h1>
                <pre>Proceed to the login page. Or sign up!</pre>
                <a href='/login'>Login</a>
                <a href='/signup'>Sign up</a>"""
        # maybe do this
        # return render.something() or html text with link to next step: /game

class Login:
    def GET(self):
        f = fbox()
        return render.windex(f)

    def POST(self):
        f = fbox()

        if not f.validates():
            return render.windex(f)

        usrnm = f['Username'].value
        pw = f['Password'].value
        if (usrnm, pw) in allowed:
            session.logged_in = True
            # raise web.seeother('/')
            return """<h1>Login success!</h1><pre> Welcome %s.
                </pre><a href="/logout">Logout</a>""" % (f.d.Username)
            # add a link to the next page (back to index maybe)
        else:
            session.logged_in = False
            return '<h1>Login failed!</h1><a href="/">Return to Home</a>'

class Logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/')


# Hack to make session play nice with the reloader (in debug mode)
if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store)
    web.config._session = session
else:
    session = web.config._session

if __name__ == '__main__':
    app.run()
