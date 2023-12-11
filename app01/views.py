from django.shortcuts import render


# Create your views here.

def index(request):
    import datetime
    s="hello"
    l = [111, 222, 333]  # 列表
    dic = {"name": "lay", "age": 18}  # 字典
    date = datetime.date(2000, 2, 2)  # 日期对象

    class Person(object):
        def __init__(self, name):
            self.name = name

    person_lay = Person("lay")  # 自定义类对象
    person_mona = Person("mona")
    person_joker = Person("joker")

    person_list = [person_mona, person_lay, person_joker]

    return render(request, "index.html", {"l": l, "dic": dic, "date": date, "person_list": person_list})
