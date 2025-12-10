'''
# 基本用法 — 定义类与创建实例
class Person:
    def __init__(self, name, age):
        self.name = name        #实例属性
        self.age = age

    def greet(self):  #普通方法，第一个参数是self
        return f"Hi, I'm {self.name}, {self.age} years old."

p = Person("Huadong Li", 30)

print(p.greet())

#类属性 vs 实例属性
class Counter:
    total = 0 #类属性

    def __init__(self):
        Counter.total += 1
        self.id = Counter.total #实例属性

a = Counter()
b = Counter()
print(a.id, b.id,Counter.total)

#继承与重写、super():子类继承父类的方法/属性，可重写并用 super() 调用父类实现。
class Animal:
    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return "Miao"

c = Cat()
print(c.speak())
#带 super():
class Base:
    def __init__(self,x):
        self.x = x

class Sub(Base):
    def __init__(self,x,y):
        super().__init__(x)
        self.y = y
'''
#类方法、静态方法与属性（@classmethod\@staticmethod\@propetry）
#@classmethod：第一个参数是类（cls）,常用于工厂方法或者修改类状态。
#@staticmethod:不接收 self/cls，像普通函数放在类命名空间下。
#@property：把方法当成属性访问（只读或可设定setter）。

class Circle:
    pi = 3.1415926

    def __init__(self,r):
        self.r = r

    @property
    def area(self):
        return Circle.pi*(self.r**2)

    @classmethod
    def from_diameter(cls,d):
        return cls(d/2)

    @staticmethod
    def unit():
        return "radius"

a = Circle(3)
print(a.area)

a2 = Circle.from_diameter(6)
print(a2.area)
print(a2.unit())

#特殊方法（魔术方法）—— 让对象表现得像内建类型
class Vec:
    def __init__(self,x,y):
        self.x,self.y = x,y
    def __repr__(self):
        return f"Vec({self.x},{self.y})"
    def __add__(self,other):
        return Vec(self.x + other.x, self.y + other.y)

v1 = Vec(1,2)
v2 = Vec(3,4)
print(v1 +v2) # Vec(4,6)

#dataclass（简化类定义，自动生成构造器等）



