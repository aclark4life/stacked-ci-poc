from hello import greet


def test_greet():
    assert greet() == "hello, world!"
    assert greet("stacked") == "hello, stacked!"
