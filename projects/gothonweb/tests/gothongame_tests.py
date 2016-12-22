from nose.tools import *
from bin.gothongame import app
from tests.tools import assert_response

def test_show_room():
    resp = app.request('/')
    assert_response(resp, status="303 See Other")

    resp = app.request("/game")
    assert_response(resp)

    resp = app.request("/game", method="POST")
    #assert_response(resp, contains="None")

    data = {'action': 'dodge!'}
    resp = app.request("/game", method="POST", data=data)
    assert_response(resp, contains='dodge!')
