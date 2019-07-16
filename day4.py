# -*- coding:utf-8 -*-
__author__ = "ljh"
__date__ = "2019-07-15"

# """
# abstract class use python
# """
#
# from abc import ABCMeta, abstractmethod
#
#
# class Parent(metaclass=ABCMeta):
#     """ abstract class test"""
#
#     def __init__(self, *args):
#         super(Parent, self).__init__(*args)
#
#     @abstractmethod
#     def call_my_name(self):
#         print('this is the parent method')
#
#
# class Son(Parent):
#
#     def call_my_name(self):
#         print('this is the son method')
#         super(Son, self).call_my_name()



# son = Son()
# son.call_my_name()

# from abc import ABCMeta, abstractmethod
#
#
# class Animal(metaclass=ABCMeta):
#     @abstractmethod
#     def do_say(self):
#         pass
#
#
# class Dog(Animal):
#
#     def do_say(self):
#         print('Bhow Bhow!')
#
#
# class Cat(Animal):
#
#     def do_say(self):
#         print('Meow Meow!')
#
#
# class ForestFactory(object):
#
#     def make_sound(self, object_type):
#         return eval(object_type)().do_say()
#
#

from abc import ABCMeta, abstractmethod


class Section(metaclass=ABCMeta):
    @abstractmethod
    def describe(self):
        pass


class PersonalSection(Section):

    def describe(self):
        print("Personal Section")


class AlbumSection(Section):

    def describe(self):
        print("Album Section")


class PatentSection(Section):

    def describe(self):
        print("Patent Section")


class PublicationSection(Section):

    def describe(self):
        print('Publication Section')


class Profile(metaclass=ABCMeta):

    def __init__(self):
        self.section = []
        self.create_profile()

    @abstractmethod
    def create_profile(self):
        pass

    def get_section(self):
        return self.section

    def add_section(self, section):
        self.section.append(section)


class linkedin(Profile):

    def create_profile(self):
        self.add_section(PersonalSection())
        self.add_section(PatentSection())
        self.add_section(PublicationSection())


class facebook(Profile):

    def create_profile(self):
        self.add_section(PersonalSection())
        self.add_section(AlbumSection())


class PizzaFactory(metaclass=ABCMeta):

    @abstractmethod
    def create_veg_pizza(self):
        pass

    @abstractmethod
    def create_non_veg_pizza(self):
        pass


class IndianPizzaFactory(PizzaFactory):

    def create_veg_pizza(self):
        return DeluxVeggiePizza()

    def create_non_veg_pizza(self):
        return ChickenPizza()


class USPizzaFactory(PizzaFactory):

    def create_veg_pizza(self):
        return MexicanaVegPizza()

    def create_non_veg_pizza(self):
        return HamPizza()


class VegPizza(metaclass=ABCMeta):

    @abstractmethod
    def prepare(self, VegPizza):
        pass


class MexicanaVegPizza(VegPizza):

    def prepare(self):
        print('prepare ', type(self).__name__)


class DeluxVeggiePizza(VegPizza):
    def prepare(self):
        print('prepare ', type(self).__name__)


class NonVegPizza(metaclass=ABCMeta):

    @abstractmethod
    def server(self, VegPizza):
        pass


class ChickenPizza(NonVegPizza):
    def server(self, VegPizza):
        print(type(self).__name__, 'is served with chicken on ', type(VegPizza).__name__)


class HamPizza(NonVegPizza):
    def server(self, VegPizza):
        print(type(self).__name__, 'is served with chicken on ', type(VegPizza).__name__)


class Pizzastore:
    def __init__(self):
        pass

    def make_pizza(self):
        for factory in [IndianPizzaFactory(), USPizzaFactory()]:
            self.factory = factory
            self.NonVegPizza = self.factory.create_non_veg_pizza()
            self.VegPizza = self.factory.create_veg_pizza()
            self.VegPizza.prepare()
            self.NonVegPizza.server(self.VegPizza)


if __name__ == "__main__":
    pizza = Pizzastore()
    pizza.make_pizza()
