# -*- coding:utf-8 -*-
__author__ = "ljh"
__date__ = "2019-07-16"


class Hotelier(object):
    def __init__(self):
        print('Arranging the Hotel for Marriage?--')

    def __isAvailable(self):
        print('Is the Hotel free for the event on given day?')
        return True

    def book_hotel(self):
        if self.__isAvailable():
            print('Registered the Booking\n\n')


class Florist(object):

    def __init__(self):
        print("Flower Decorations for the event?--")

    def set_flower_requirement(self):
        print("Carnations, Roses and Lilies would be used for Decorations\n\n")


class Caterer(object):
    def __init__(self):
        print('Food Arrangement for the Event?--')


    def set_cuisine(self):
        print('Chinese & Continental Cuisine to be served\n\n')


class Musician(object):
    def __init__(self):
        print('Musician Arrangement for the Event?--')


    def set_musician_type(self):
        print('Jazz and Classical will be played\n\n')


class EventManager(object):

    def __init__(self):
        print('Event manager:: Let me talk to the folks\n\n')

    def arrange(self):
        self.hotelier = Hotelier()
        self.hotelier.book_hotel()

        self.florist = Florist()
        self.florist.set_flower_requirement()

        self.caterer = Caterer()
        self.caterer.set_cuisine()

        self.musician = Musician()
        self.musician.set_musician_type()


class You(object):
    def __init__(self):
        print("You:: Whoa!Marriage Arrangements??!!!")

    def ask_event_manager(self):
        print("You:: Let's Contact the Event Manager")
        manager = EventManager()
        manager.arrange()

    def __del__(self):
        print("You:: Thanks to the Event Manager, all preparations done!Phew!")


if __name__ == "__main__":
    y = You()
    y.ask_event_manager()
