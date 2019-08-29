# -*- coding: cp1252 -*-
from PyQt4 import QtGui
from PyQt4 import QtCore
from pyowm import OWM
import time, requests, sys, os, socket

# DO NOT RELEASE TO PUBLIC (PERSONAL WEATHER API KEY)
API_key1 = '[INSERT API KEY FROM OPENWEATHERMAP HERE]'
owm = OWM(API_key1)

def resource_path(relative_path):
     # Help's Pyinstaller refer to images packaged.
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)


class ClockThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            current_time = time.strftime("%#I:%M", time.localtime())
            current_ampm = time.strftime("%p", time.localtime())
            current_date = time.strftime("%a, %b %d, %Y", time.localtime())
            self.emit(QtCore.SIGNAL('current_time_data'), (current_time + " " + "<span style='font-size:30pt'><b>"
                                                           + current_ampm + "</b></span>"))
            self.emit(QtCore.SIGNAL('current_date_data'), current_date)
            time.sleep(1)


class WeatherThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.internet_connection = False

    def __del__(self):
        self.wait()

    def init_connection(self):
        '''Checks for valid internet connection, returns True if connected, False if no internet'''
        try:
            host = socket.gethostbyname("www.google.com")
            s = socket.create_connection((host, 80), 2)
            # print('Connection succeeded!')
            self.internet_connection = True
        except:
            # print('Not connected...')
            time.sleep(2)

    def getweather(self):
        # set_location_relative = owm.weather_at_place('Fountain Valley, US')
        # set_location_coord = owm.weather_at_coords(33.7296275, -117.9307587)  # Exact coordinates of 11381 HOME
        set_location_coord = owm.weather_at_coords(33.860360, -118.241930)    # Exact coordinates of CARSON WORK
        location = set_location_coord.get_location()
        weather = set_location_coord.get_weather()
        temperature = weather.get_temperature('fahrenheit')  # {'temp_max', 'temp', 'temp_min'}
        climate_text = weather.get_detailed_status()
        weather_format = '{}, {}°F'.format(climate_text.title(), temperature['temp'])
        self.emit(QtCore.SIGNAL('current_weather_data'), weather_format)
        self.emit(QtCore.SIGNAL('current_location_data'), location.get_name().upper())

    def run(self):
        while not self.internet_connection:     # If no internet, try to check for internet connection
            self.init_connection()
        while self.internet_connection:     # If internet connection found, return weather data
            try:
                self.getweather()
                time.sleep(3600)    # Timeout update weather data every hour
            except:
                self.getweather()


class ApplicationWindow(QtGui.QFrame):
    def __init__(self):

        # Initialize Window
        super(QtGui.QFrame, self).__init__()
        self.vbox = QtGui.QVBoxLayout()

        self.setWindowTitle("Dean's Weatherclock 2.0")
        self.setWindowIcon(QtGui.QIcon(resource_path("weather.ico")))
        self.resize(200, 100)

        self.tray_icon = QtGui.QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon(resource_path("weather.ico")))
        show_action = QtGui.QAction("Show", self)
        quit_action = QtGui.QAction("Exit", self)
        hide_action = QtGui.QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QtGui.QApplication.quit)
        tray_menu = QtGui.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Set Fonts
        self.fonttime = QtGui.QFont("Segoe UI Light", 55)
        self.fontdate = QtGui.QFont("Segoe UI Light", 30)
        self.fontweather = QtGui.QFont("Segoe UI Light", 30)
        self.fontlocation = QtGui.QFont("Segoe UI Light", 15)

        # Declare Labels
        self.timeLabel = QtGui.QLabel('Time', self)
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setStyleSheet('color:white')
        self.timeLabel.setFont(self.fonttime)

        self.dateLabel = QtGui.QLabel('Date', self)
        self.dateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dateLabel.setStyleSheet('color:white')
        self.dateLabel.setFont(self.fontdate)

        self.weatherLabel = QtGui.QLabel("Disconnected", self)   # Weather label
        self.weatherLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.weatherLabel.setStyleSheet('color:white')
        self.weatherLabel.setFont(self.fontweather)

        self.locationLabel = QtGui.QLabel("Connecting to Internet...", self)     #Location Label
        self.locationLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.locationLabel.setStyleSheet('color:white')
        self.locationLabel.setFont(self.fontlocation)
        
        # Add Widgets
        self.vbox.addWidget(self.timeLabel)
        self.vbox.addWidget(self.dateLabel)
        self.vbox.addWidget(self.weatherLabel)
        self.vbox.addWidget(self.locationLabel)

        # Set PyQt Layout
        self.setLayout(self.vbox)

        # Create thread objects for clock and weather
        self.clockThread = ClockThread()
        self.weatherThread = WeatherThread()

        # Connect passthrough signals from thread and call on update functions
        self.connect(self.clockThread, QtCore.SIGNAL('current_time_data'), self.updateTime)
        self.connect(self.clockThread, QtCore.SIGNAL('current_date_data'), self.updateDate)
        self.connect(self.weatherThread, QtCore.SIGNAL('current_weather_data'), self.updateWeather)
        self.connect(self.weatherThread, QtCore.SIGNAL('current_location_data'), self.updateLocation)
        self.start()

    # Update the time
    def updateTime(self, current_time_string):
        self.timeLabel.setText(current_time_string)

    # Update the date
    def updateDate(self, current_date_string):
        self.dateLabel.setText(current_date_string)

    # Update the weather
    def updateWeather(self, current_weather_string):
        self.weatherLabel.setText(current_weather_string)

    # Update the location
    def updateLocation(self, current_location_string):
        self.locationLabel.setText(current_location_string)

    # Start thread objects
    def start(self):
        self.clockThread.start()
        self.weatherThread.start()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    instance = ApplicationWindow()

    instance.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    instance.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    screen_size = QtGui.QDesktopWidget().availableGeometry()
    window_size = instance.geometry()

    instance.move(100, screen_size.height()-(window_size.height()*2)-100) # SETS WHERE TO APPEAR ON DESKTOP ON START-UP (X,Y)
    instance.show()
    sys.exit(app.exec_())
