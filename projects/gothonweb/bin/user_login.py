""" Messing around with a simple user login system using web.py.
web.py has it's own template for authentication, but I am attempting to do this
very simply from scratch.
I could have used a database instead, but this is just for fun. Maybe that can
be added later.
Optional Todo: Beautify html pages
"""
from gothonweb import populator as p
import os.path
import web
from web import form

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


user_db = os.path.join(os.path.expanduser('~'), 'learning', 'lcthw', 'lpthw',
                                'projects', 'gothonweb', 'docs', 'user_db.csv')
p.create_db(user_db)


class Signup(object):
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

class Index(object):
    # Give user the option to logout, or start the game
    def GET(self):
        if not session.get('logged_in', False):
            return """<h1>Logged out!</h1>
                <pre>Proceed to the login page. Or sign up!</pre>
                <a href='/login'>Login</a>
                <a href='/signup'>Sign up</a>"""
        # maybe do this in the game eventually:
        # return render.something() or html text with link to next step: /game

class Login(object):
    def GET(self):
        f = fbox()
        return render.windex(f, None)

    def POST(self):
        f = fbox()

        if not f.validates():
            return render.windex(f, None)

        # authenticate credentials here
        if p.auth(user_db, f.d.Username, f.d.Password):
            session.logged_in = True
            return """<h1>Login success!</h1><pre> Welcome %s.
                </pre><a href="/logout">Logout</a>""" % (f.d.Username)
            # add a link to the next page (back to index maybe)
        else:
            session.logged_in = False
            return '<h1>Login failed!</h1><a href="/">Return to Home</a>'

class Logout(object):
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
