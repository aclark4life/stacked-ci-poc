from hello import farewell, greet


def test_greet():
    assert greet() == "hello, world!"
    assert greet("stacked") == "hello, stacked!"


def test_farewell():
    assert farewell() == "goodbye, world!"


def test_greet_shout():
    assert greet().upper() == "HELLO, WORLD!"
