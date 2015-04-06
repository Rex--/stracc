# Generates information files to be used for chart.js charts

import datetime
import json
import os


date_format = '%d/%m/%Y'
times_of_day = ['Breakfast', 'Lunch', 'Dinner', 'Bedtime']
chart_data_path = 'web-assets/chart-data'

# chartgen can be 'today', 'thisweek', 'thismonth', 'thisyear', 'alltime', or 'all'
def updateChart(chart, db, charttogen='today', dtype='bloodsugar'):
    if charttogen == 'today':
        today = db.getDay()
        chart.genToday(today, os.path.join(chart_data_path, 'today'), dtype=dtype)
    elif charttogen == 'thisweek':
        thisWeek = db.getWeek()
        chart.genWeek(thisWeek, os.path.join(chart_data_path, 'thisweek'), dtype=dtype)
    elif charttogen == 'thismonth':
        thisMonth = db.getMonth()
        chart.genMonth(thisMonth, os.path.join(chart_data_path, 'thismonth'), dtype=dtype)
    elif charttogen == 'thisyear':
        print 'not supported'
    elif charttogen == 'all':
        today = db.getToday()
        thisWeek = db.getWeek()
        thisMonth = db.getMonth()
        chart.genToday(today, os.path.join(chart_data_path, 'today'), dtype=dtype)
        chart.genWeek(thisWeek, os.path.join(chart_data_path, 'thisweek'), dtype=dtype)
        chart.genMonth(thisMonth, os.path.join(chart_data_path, 'thismonth'), dtype=dtype)
    else:
        print "not supported"


class LineChart:

    # week = dict of a week data. Can be passed in directly from data file. Structure:
    #   { weeknum: int
    #     days: {
    #       dow: string
    #       doy: int
    #}}
    # path = full path to save the file
    def genWeek(self, week, path, dtype='bloodsugar'):
        data = {
            'chartLabels': [],
            'chartData': {
                'Breakfast': [],
                'Lunch': [],
                'Dinner': [],
                'Bedtime': []
            }
        }
        total = 0
        totalNums = 0
        for date in sorted(week['days'], key=lambda x: datetime.datetime.strptime(x, date_format)):
            dateObj = datetime.datetime.strptime(date, date_format)
            data['chartLabels'].append(dateObj.strftime('%A'))
            for time in times_of_day:
                data['chartData'].append(week['days'][date][time][dtype])
                if dtype == 'bloodsugar':
                    total += week['days'][date][time][dtype]
                    totalNums += 1
        if dtype == 'bloodsugar':
            data['chartDataAvg'] = total / totalNums

        with open(os.path.join(path, 'linechart.json'), 'w') as chartDataFile:
            json.dump(data, chartDataFile, separators=(',',':'))

    def genMonth(self, month, path, dtype='bloodsugar'):
        data = {
            'chartLabels': [],
            'chartData': {
                'Breakfast': [],
                'Lunch': [],
                'Dinner': [],
                'Bedtime': []
            }
        }
        total = 0
        totalNums = 0
        for week in sorted(month):
            for date in sorted(month[week]['days'], key=lambda x: datetime.datetime.strptime(x, date_format)):
                dateObj = datetime.datetime.strptime(date, date_format)
                data['chartLabels'].append(dateObj.strftime('%m/%d'))
                for time in times_of_day:
                    data['chartData'].append(month[week]['days'][date][time][dtype])
                    if dtype == 'bloodsugar':
                        total += month[week]['days'][date][time][dtype]
                        totalNums += 1
        if dtype == 'bloodsugar':
            data['chartDataAvg'] = total / totalNums

        with open(os.path.join(path, 'linechart.json'), 'w') as chartDataFile:
            json.dump(data, chartDataFile, separators=(',',':'))


class RadarChart:

    def genToday(self, today, path, dtype='bloodsugar'):
        data = {
            'bloodsugarData': [],
            'bloodsugarHigh': int
        }
        for time in times_of_day:
            data['bloodsugarData'].append(today[time][dtype])
        data['bloodsugarHigh'] = max(data['bloodsugarData'])

        with open(os.path.join(path, 'radarchart.json'), 'w') as chartDataFile:
            json.dump(data, chartDataFile, separators=(',',':'))
