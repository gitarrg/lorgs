


from lorgs.models import base


class TestModel(base.Model):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<TestModel({self.name})>"



def test1():

    print(TestModel.all)
    a = TestModel(name="A")
    b = TestModel(name="B")
    print(TestModel.all)


def test2():
    print(TestModel.all)



if __name__ == '__main__':
    test1()
    test2()





