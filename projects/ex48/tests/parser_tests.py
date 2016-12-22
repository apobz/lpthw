from nose.tools import *
from ex48.parser import *
from ex48 import lexicon

def test_Sentence():
    # SUBJECT VERB OBJECT
    #s1 = Sentence([('noun','bear'), ('verb','eat'), ('stop', 'the'), ('noun','princess')])
    s1 = Sentence(('noun','bear'), ('verb','eat'), ('noun','princess'))

    assert_equal(s1.subject, 'bear')
    assert_equal(s1.verb, 'eat')
    assert_equal(s1.object, 'princess')

def test_peek():
    list1 = lexicon.scan("bear eat the princess")
    v = None

    assert_equal(peek(list1), 'noun')
    assert_equal(peek(0), None)
    assert_equal(peek([]), None)
    assert_equal(peek(v), None)

def test_match():
    words1 = ('noun','princess')
    list2 = lexicon.scan("princess run south")

    assert_equal(match(list2, 'noun'), words1)
    assert_equal(match(lexicon.scan("princess run south"), 'direction'), None)

def test_skip():
    list3 = [('noun','bear'), ('verb','eat'), ('noun','princess')]

    assert_equal(skip(lexicon.scan("the bear eat princess"), 'stop'), list3)
    assert_equal(skip(lexicon.scan("bear eat princess"), 'blah'), list3)

def test_parse_verb():
    words2 = ('verb','go')

    assert_equal(parse_verb(lexicon.scan("the go south")), words2)
    assert_raises(ParserError, parse_verb, lexicon.scan("princess go south"))

def test_parse_object():
    words3 = ('direction','east')

    assert_equal(parse_object(lexicon.scan('east')), words3)
    assert_raises(ParserError, parse_object, lexicon.scan("eat east"))

def test_parse_subject():
    words4 = ("noun", 'princess')

    assert_equal(parse_subject(lexicon.scan("princess run")), words4)
    assert_equal(parse_subject(lexicon.scan("eat cabinet")), ('noun','player'))
    assert_raises(ParserError, parse_subject, lexicon.scan("east princess"))

def test_parse_sentence():
    w1, w2, w3 = 'bear', 'eat', 'door'

    assert_equal(parse_sentence(lexicon.scan("bear eat the princess")).subject, w1)

    assert_equal(parse_sentence(lexicon.scan("bear eat the princess")).verb, w2)

    assert_equal(parse_sentence(lexicon.scan("player eat door")).object, w3)
