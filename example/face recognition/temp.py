import os
import sys
sys.path.append(os.path.abspath("."))
from lib import db

def main():
    DB = db.DB()
    DB.LoadDB()

    DB.temp()

main()