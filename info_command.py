import nextcord
import datetime
import random


def random_colour():
    colours = [nextcord.Colour.red(),
               nextcord.Colour.orange(),
               nextcord.Colour.yellow(),
               nextcord.Colour.green(),
               nextcord.Colour.blue(),
               nextcord.Colour.purple(),
               nextcord.Colour.dark_purple()]
    random.seed(datetime.datetime.now().timestamp())
    return colours[random.randint(0, 6)]