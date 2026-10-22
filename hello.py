def greet(name: str = "world") -> str:
    return f"hello, {name}!"


if __name__ == "__main__":
    print(greet())


# Changed on main after the stack was opened: forces a rebase of s1/s2/s3.
def version() -> str:
    return "2.0"


def farewell(name: str = "world") -> str:
    return f"goodbye, {name}!"
