
from datetime import datetime
import typing

import pydantic
import dataclasses
from dataclasses import dataclass, field, make_dataclass
import attrs


from lorgs.lib import s3_store
from lorgs.logger import timeit

# @dataclass
@dataclass
class Item:
    name: str
    value: int = 0


@dataclass
class User(s3_store.BaseModel):
    name: str
    level: int
    updated: datetime = field(default_factory=datetime.utcnow)
    items: list[Item] = field(default_factory=list)

    # class meta:
    key_fmt: typing.ClassVar[str] = "{name}"


################################################################################

def test_get_key_1():

    # Define a basic test class
    class Foo(s3_store.BaseModel):
        key_fmt = "{one}#{two}"

    assert Foo.get_key(one="A", two="value2") == "foo/a#value2"


def test_get_key_2():

    # Define a basic test class
    class Foo(s3_store.BaseModel):
        key_fmt = "{one}<>{two}"

        def dict(self):
            return {"one": "Apple", "two": "Banana"}

    foo = Foo()
    assert foo.key == "foo/apple<>banana"


def test_get_key_3():

    # Define a basic test class
    class FooBarClass(s3_store.BaseModel):
        key_fmt = "{x}"

    assert FooBarClass.get_key(x=1) == "foo_bar_class/1"


################################################################################

def test_save() -> None:
    user = User(
        name="John",
        level=10,
        items = [
            Item(name="Bow", value=3),
            Item(name="Axe", value=8),
        ]
    )

    # x = attrs.asdict(user)
    # print("X", x)
    # j = json.dumps(x)
    # print("J", j)
    # print(user.ttl)
    print("user.dict", user.dict())
    # print(user.s3_object)
    


    # user.save()

def main() -> None:
    pass
    # test_save()
    # user = User(name="Arrg", spec="Druid", level=60)
    # print(user.dict())


if __name__ == "__main__":
    main()


