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
    def GET(self):
        f = fbox()
        #authReq = True
        return render.windex(f)

    def POST(self):
        f = fbox()
        #authReq = True

        if not f.validates():
            return render.windex(f)

        usrnm = f['username'].value
        pwd = f['password'].value
        if (usrnm, pwd) in allowed:
            session.logged_in = True
            #authReq = False
            return '<h1>Login success!</h1><pre Welcome %s. </pre><a href="/logout">Logout</a>' % (f.d.username)
        else:
            session.logged_in = False
            return '<h1>Login failed!</h1><a href="/">Back to login page</a>'
#            return render.windex(f, authReq)


"""        if session.get('logged_in', False):
            return render.windex(f)
        return '<h1>You are not logged in.</h1><a href="/login">Login now</a>'
"""

class Logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/')
"""
class Login:
    # press the login button after entering credentials
    def GET(self):
        # if credentials are valid
        session.logged_in = True
        raise web.seeother('/')

class Logout:
    # press logout button
    def GET(self):
        # redirects to index page, or login page
        session.logged_in = False
        raise web.seeother('/')
"""

# Hack to make session play nice with the reloader (in debug mode)
if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store)
    web.config._session = session
else:
    session = web.config._session

if __name__ == '__main__':
    app.run()
