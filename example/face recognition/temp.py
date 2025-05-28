import os
import sys
sys.path.append(os.path.abspath("."))
from lib import db
import threading
import time

def wait(Threads):
    for t in Threads:
        t.join()

def foo(text):
    counter = 0
    while counter <= 10:
        time.sleep(1)
        counter += 1
        print(f"{text}: {counter}")

def main():
    playerRemained = 2
    playerList = ["Giovanni", "Anna", False, False, False]

    print(playerList[0:playerRemained].copy())

main()