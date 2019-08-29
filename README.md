# OpenWeatherClock

> A minimalist desktop clock widget that also displays current local weather conditions.

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [FAQ](#faq)
- [Contact](#contact)
- [License](#license)

---

## Installation

- Make sure you have the proper dependencies to package. You will need PyQt4 and pyowm.
- Use PyInstaller or Py2Exe to package dawrelative.pyw into a binary. 
- It is recommended to use PyInstaller's --onefile feature to package a single clean executable.
- You can run the application on startup by placing the executable into your Windows Startup folder.

---
## Features

[![Feature Image](http://i.imgur.com/mdok64M.png)]()

- Displays current time, date, temperature, and weather condition on your desktop.
- Transparent widget. Adjustable font, color, and size.
- Weather condition updates every hour (via OpenWeatherMap)

---
## FAQ

- **Why is the weather not working and tells me that it's disconnected?**
    - You likely haven't set your API key and need to get your own personal key at OpenWeatherMap. 

- **How do I set weather location?**
    - There's 2 ways: You can set the relative location or get the exact coordinates inside the code.
    
- **How do I place the widget in another area of the desktop?**
    - You can fine tune the (x,y) coordinates of the widget in the code.

- **How do I change from Fahrenheit to Celcius?**
    - It can be changed inside the code. A settings and configuration menu is currently in the works.

---

## Contact

Reach out to me at one of the following places!

- Website at <a href="http://fvcproductions.com" target="_blank">`deanlnguyen.com`</a>
- LinkedIn is <a href="https://www.linkedin.com/in/dean-nguyen-43a08b14a/" target="_blank">`here`</a>

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- This project is licensed under the MIT license - see **[MIT license](http://opensource.org/licenses/mit-license.php)** for details