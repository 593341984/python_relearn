# -*- coding:utf-8 -*-
__author__ = "ljh"
__date__ = "2019-07-05"


def temperature():
    f = float(input('input F:'))
    c = (f - 32) / 1.8
    print '%.1fC = %.1fF' % (c, f)


def circle_area():
    import math
    radius = float(input('radius:'))
    perimeter = 2 * radius * math.pi
    area = radius * radius * math.pi
    print 'perimeter: %.2f' % perimeter
    print 'area: %.2f' % area


def year_leap():
    year = input('year:')
    print year % 4 == 0 and year % 100 != 0 or year % 400 == 0


class A:
    def a1(self):
        print 'a1'


class B(A):

    def b(self):
        print 'b'


if __name__ == '__main__':
    b = B()
    b.a1()
