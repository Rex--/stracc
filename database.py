# Simple database, loads and saves data in weeks. Saves files in json format:
#   {
#       'week' : [int corresponding to the week number] (same as filename)
#       'days' : {
#                    '[date - "D/M/Y"]' : {
#                                             'dow' : [string of the day of week(Monday, etc.)],
#                                             'doy' : [int of the day of the year],
#                                             'tests' : {
#                                                           '[time - "H:M:S"]' : '[data]'
#                                                       },
#                                             'shots' : {
#                                                           '[time - "H:M:S"]' : '[data]'
#                                                       }
#                                         }
#                }
#   }
#

import os
from datetime import date, datetime
import json

class Database:

    def __init__(self, ptdb, name=None):
        self._date_format = '%d/%m/%Y'
        self._time_format = '%H:%M:%S'
        self._path_to_db = ptdb
        self._db_filename = self._path_to_db.split('/')[-1]
        if name != None:
            self._db_name = name
        else:
            self._db_name = self._db_filename
        self._root_db_file = os.path.join(self._path_to_db, self._db_filename + '.json')
        self._Database = self.__loadDB()


    def __loadDB(self):
        if not os.path.exists(self._path_to_db):
            self.__createDB()
        dbFile = open(self._root_db_file, 'rw')
        dbString = dbFile.read()
        dbFile.close()
        return json.loads(dbString)


    def __createDB(self):
        os.mkdir(self._path_to_db)
        today = date.today().strftime(self._date_format)
        dbFile = open(self._root_db_file, 'w')
        dbRootFile = {
            'name': self._db_name,
            'created': today,
            'updated': today
        }
        json.dump(dbRootFile, dbFile, indent=2)
        dbFile.close()

    def __updateDB(self, date):
        self._Database['updated'] = date

    # Checks to see if the datafile for the data exists. If it does, it does nothing,
    #   if it doesnt, it creates an empty file ready to call open() on
    # if weekNum is not None then it will use the current year unless
    #   weekYear is set.
    def __touchDataFile(self, date=None, weekNum=None, weekYear=None):
        if date != None:
            dateObj = datetime.strptime(date, self._date_format)
        elif weekNum != None:
            if weekYear == None:
                weekYear = datetime.today().strftime('%Y')
            dateObj = datetime.strptime('0'+'/'+weekNum+'/'+weekYear, '%w/%U/%Y')
        else:
            dateObj = datetime.today().strftime(self._date_format)
        dateYear = dateObj.strftime('%Y')
        dateMonth = dateObj.strftime('%B')
        dateWeek = dateObj.strftime('%U')
        dataFilePath = os.path.join(self._path_to_db, dateYear, dateMonth, dateWeek + '.json')
        # [year]/[month]/[weeknumber].json
        if not os.path.exists(dataFilePath):
            # [year]/[month]
            if not os.path.exists(os.path.join(self._path_to_db, dateYear, dateMonth)):
                # [year]
                if not os.path.exists(os.path.join(self._path_to_db, dateYear)):
                    # make year dir
                    os.mkdir(os.path.join(self._path_to_db, dateYear))
                # make month dir
                os.mkdir(os.path.join(self._path_to_db, dateYear, dateMonth))
            skelly = {
                'week': dateWeek,
                'days': {}
            }
            with open(dataFilePath, 'w') as dataFile:
                json.dump(skelly, dataFile, indent=2)
        return dataFilePath

    # To be called if the data is not the latest or for safety
    #   This function is slower than addNewData, but is safer.
    # date = a string of the date in format: %d/%m/%Y (ex. 05/12/2015)(or 'now')
    # time = a string of the 24 hour time in format: %H:%M:%S (ex. 12:30:45)(or 'now')
    # dtype = type of data (tests or shots)
    # data = a string of the data to be stored.
    def addData(self, date, time, dtype, data):
        if str(date) == 'today':
            date = datetime.today().strftime(self._date_format)
        if str(time) == 'now':
            time = datetime.now().strftime(self._time_format)
        dateObj = datetime.strptime(date, self._date_format)
        dataFilePath = self.__touchDataFile(date)
        dataFile = open(dataFilePath, 'r+')
        dataFileString = dataFile.read()    # Read db file
        dataFile.seek(0)    # Insert cursor at the beginning of the file
        week = json.loads(dataFileString)
        if date not in week['days']:
            week['days'][date] = {
                'dow': dateObj.strftime('%A'),
                'doy': dateObj.strftime('%j'),
                'tests': {},
                'shots': {}
            }
        week['days'][date][dtype][time] = data
        dataFileString = json.dumps(week, indent=2)
        dataFile.write(dataFileString)
        dataFile.truncate()
        dataFile.close()
        self.__updateDB(datetime.today().strftime(self._date_format))

    # Used to get a data point at a specific point in time
    def getData(self, date='today', time='all', dtype='tests'):
        if date == 'today':
            date = datetime.today().strftime(self._date_format)
        dateObj = datetime.strptime(date, self._date_format)
        dateYear = dateObj.strftime('%Y')
        dateMonth = dateObj.strftime('%B')
        dateWeek = dateObj.strftime('%U')
        dataFilePath = os.path.join(self._path_to_db, dateYear, dateMonth, dateWeek + '.json')
        with open(dataFilePath, 'r') as dataFile:
            dataFileString = dataFile.read()
            week = json.loads(dataFileString)
        if time != 'all':
            return week['days'][date][dtype][time]
        elif time == 'all':
            return week['days'][date][dtype]
        else:
            return 'Bad time.'

    # Returns a dictionary corresponding to the week number,
    # you can also specify a specific date and it will get that week.
    # If no records for the week exists, it will create it and return an empty week.
    # A call with no arguments returns this week.
    def getWeek(self, date=None, weekNum=None, weekYear=None):
        if date != None:
            dataFilePath = self.__touchDataFile(date=date)
            dateObj = datetime.strptime(date, self._date_format)
        elif weekNum != None:
            if weekYear == None:
                weekYear = datetime.today().strftime('%Y')
            dataFilePath = self.__touchDataFile(weekNum=weekNum, weekYear=weekYear)
            dateObj = datetime.strptime('0'+'/'+weekNum+'/'+weekYear, '%w/%U/%Y')
        else:
            dateObj = datetime.today()
            dataFilePath = self.__touchDataFile()
        dataFile = open(dataFilePath, 'r')
        dataFileString = dataFile.read()
        return json.loads(dataFileString)


    # To Be called if the data is the latest -- will not work if database has some older
    #   Faster than calling addData as it just appends it to the latest file
    #def addNewData(date, time, data):
