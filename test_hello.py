from hello import farewell, greet, shout


def test_greet():
    assert greet() == "hello, world!"
    assert greet("stacked") == "hello, stacked!"


def test_farewell():
    assert farewell() == "goodbye, world!"


def test_greet_shout():
    assert shout(greet()) == "HELLO, WORLD!"
