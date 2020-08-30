from math import pi
from turtle import Turtle
import time

rad = float(input("Please enter the radius of the flower: "))
ang = float(input("Please enter angle of the angle in between petals: "))
leaf = float(input("Please enter number of leaves: "))

julie = Turtle()
julie.speed(250)

def flower(radius, angle, leaves):
    def arc(radius, angle):
        julie.circle(radius, angle, 100)

    def leaf(radius, angle):
        julie.right(angle / 2)
        arc(radius, angle)
        julie.left(180 - angle)
        arc(radius, angle)
        julie.left(180 - angle + angle / 2)

    i = 1

    while i <= leaves:
        leaf(radius, angle)
        julie.left(360 / leaves)
        i += 1

julie.left(90)

#flower(100,150,9)
flower(rad, ang, leaf)
time.sleep(15)