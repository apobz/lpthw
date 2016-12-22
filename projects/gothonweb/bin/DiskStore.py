import web


urls = (
    '/', 'Index',
    '/login', 'Login',
    '/logout', 'Logout',
)

web.config.debug = False
app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'))

render = web.template.render('templates/', base="layout_3")

class Index:
    def GET(self):
        if session.get('logged_in', False):
            return render.windex()
        return '<h1>You are not logged in.</h1><a href="/login">Login now</a>'

class Login:
    def GET(self):
        session.logged_in = True
        raise web.seeother('/')

class Logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/')


if __name__ == '__main__':
    app.run()
