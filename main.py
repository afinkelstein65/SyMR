import numpy as np
import argparse
from argparse import ArgumentParser
from tkinter import *
from functions import *

if __name__ == "__main__":

    parse = ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    args = parse.parse_args()

    GUI = GUI('lemon')
    GUI.run()
