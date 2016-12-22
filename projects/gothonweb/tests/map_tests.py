from nose.tools import *
from gothonweb.map import *

def test_room():

    # gold is a Room object with parameters name, description
    gold = Room("GoldRoom",
                """This room has gold in it you can grab. There's a
                door to the north.""")

    # gold.name = "GoldRoom"
    assert_equal(gold.name, "GoldRoom")
    assert_equal(gold.paths, {})

def test_room_paths():
    center = Room("Center", "Test room in the center.")
    north = Room("North", "Test room in the north.")
    south = Room("South", "Test room in the south.")

    # call add_paths function with parameters paths, which is a dictionary
    # on the 'center' object
    center.add_paths({'north': north, 'south': south})
    assert_equal(center.go('north'), north)
    assert_equal(center.go('south'), south)

def test_map():
    start = Room("Start", "You can go west and down a hole.")
    west = Room("Trees", "There are trees here, you can go east.")
    down = Room("Dungeon", "It's dark down here, you can go up.")

    start.add_paths({'west': west, 'down': down})
    west.add_paths({'east': start})
    down.add_paths({'up': start})

    assert_equal(start.go('west'), west)
    assert_equal(start.go('west').go('east'), start)
    assert_equal(start.go('down').go('up'), start)

def test_gothon_game_map():

    assert_equal(START.go("shoot!"), shoot_fail)
    assert_equal(START.go("dodge!"), dodge_fail)

    room = START.go('tell a joke')
    assert_equal(room, laser_weapon_armory)

    assert_equal(laser_weapon_armory.go('*'), keypad_fail)
    assert_equal(laser_weapon_armory.go('0132'), the_bridge)

    assert_equal(the_bridge.go('throw the bomb'), bomb_death)
    assert_equal(the_bridge.go('slowly place the bomb'), escape_pod)

    assert_equal(escape_pod.go('*'), the_end_loser)
    assert_equal(escape_pod.go('2'), the_end_winner)
