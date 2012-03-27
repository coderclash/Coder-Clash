# Coder Clash: Head to Head Coding Challenges

This game is under heavy development. Some of the tech used:

* Tornado
* Socket.IO
* Backbone.js
* Coffeescript
* SASS
* Bootstrap (for that unique look)


## Getting Started

**You will need MongoDB running on the standard ports!**

1. `git clone git@github.com:coderclash/Coder-Clash.git`
2. `cd Coder-Clash`
3. `mkvirtualenv coderclash`
4. `pip install -r requirements.pip`
5. `cp coderclash/__secrets.py coderclash/secrets.py` and edit
5. `python coderclash/bin/app.py`
6. `python tests.py`

You'll also need to run a copy of PythonPie, an internal RESTful
API for running Python code in a sandbox on 127.0.0.1:5000. 

Get it here: https://github.com/coderclash/pythonpie

Further, here are the commands you might useful for compiling
CoffeeScript and SASS:

* `coffee -c -b -o coderclash/static/assets/js --watch coderclash/static/src/coffee`
* `sass --watch coderclash/static/src/sass:coderclash/static/assets/css`