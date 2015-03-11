# Generates information files to be used for chart.js charts

import datetime
import json
import os


date_format = '%d/%m/%Y'
time_format = '%H:%M:%S'
chart_data_path = 'web-assets/chart-data'

# chartgen can be 'today', 'thisweek', 'thismonth', 'thisyear', 'alltime', or 'all'
def updateChart(chart, db, charttogen='today', dtype='tests'):
    if charttogen == 'today':
        print 'Not supported'
    elif charttogen == 'thisweek':
        thisWeek = db.getWeek()
        chart.genWeek(thisWeek, os.path.join(chart_data_path, 'thisweek.json'), dtype=dtype)
    elif charttogen == 'thismonth':
        thisMonth = db.getMonth()
        chart.genMonth(thisMonth, os.path.join(chart_data_path, 'thismonth.json'), dtype=dtype)
    elif charttogen == 'thisyear':
        print 'not supported'
    elif charttogen == 'all':
        thisWeek = db.getWeek()
        thisMonth = db.getMonth()
        chart.genWeek(thisWeek, os.path.join(chart_data_path, 'thisweek.json'), dtype=dtype)
        chart.genMonth(thisMonth, os.path.join(chart_data_path, 'thismonth.json'), dtype=dtype)
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
    def genWeek(self, week, path, dtype='tests'):
        data = {
            'chartData': [],
            'chartLabels': []
        }
        total = 0
        for date in sorted(week['days'], key=lambda x: datetime.datetime.strptime(x, date_format)):
            dateObj = datetime.datetime.strptime(date, date_format)
            for time in sorted(week['days'][date][dtype], key=lambda x: datetime.datetime.strptime(x, time_format)):
                timeObj = datetime.datetime.strptime(time, time_format)
                data['chartLabels'].append(dateObj.strftime('%a')+'@'+timeObj.strftime('%I:%M%p'))
                data['chartData'].append(week['days'][date][dtype][time])
                if dtype == 'tests':
                    total += week['days'][date][dtype][time]
        if dtype == 'tests':
            data['chartDataAvg'] = total / len(data['chartData'])

        with open(path, 'w') as chartDataFile:
            json.dump(data, chartDataFile, indent=2)


    def genMonth(self, month, path, dtype='tests'):
        data = {
            'chartLabels': [],
            'chartData': []
        }
        total = 0
        for week in sorted(month):
            for date in sorted(month[week]['days'], key=lambda x: datetime.datetime.strptime(x, date_format)):
                dateObj = datetime.datetime.strptime(date, date_format)
                for time in sorted(month[week]['days'][date][dtype], key=lambda x: datetime.datetime.strptime(x, time_format)):
                    timeObj = datetime.datetime.strptime(time, time_format)
                    data['chartLabels'].append(dateObj.strftime('%a')+'@'+timeObj.strftime('%I:%M %p'))
                    data['chartData'].append(month[week]['days'][date][dtype][time])
                    if dtype == 'tests':
                        total += month[week]['days'][date][dtype][time]
        if dtype == 'tests':
            data['chartDataAvg'] = total / len(data['chartData'])

        with open(path, 'w') as chartDataFile:
            json.dump(data, chartDataFile, indent=2)


#class RadarChart:

    #def genWeek:
