""" Messing around with a simple user login system using web.py
"""

import web
from web import form

urls = (
    '/', 'Index',
    '/login', 'Login',
    '/logout', 'Logout',
)

web.config.debug = False
app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'))

render = web.template.render('templates/', base="layout_3")

fbox = form.Form(
    form.Textbox('username', form.notnull),
    form.Password('password',form.notnull),
    form.Button('Login'),
)

allowed = (
    ('foo', 'bar'),
    ('baz', 'qux')
)

class Index:
    # Give user the option to logout, or start the game
    def GET(self):
        if not session.get('logged_in', False):
            return """<h1>Logged out!</h1>
                <pre>Proceed to the login page.</pre>
                <a href='/login'>Login</a>"""

class Login:
    def GET(self):
        f = fbox()
        return render.windex(f)

    def POST(self):
        f = fbox()

        if not f.validates():
            return render.windex(f)

        usrnm = f['username'].value
        pwd = f['password'].value
        if (usrnm, pwd) in allowed:
            session.logged_in = True
            # raise web.seeother('/')
            return """<h1>Login success!</h1><pre> Welcome %s.
                </pre><a href="/logout">Logout</a>""" % (f.d.username)
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
