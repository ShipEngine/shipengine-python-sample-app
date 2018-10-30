ShipEngine Python Sample App
====================================

This is a ShipEngine sample app, written in Python 3.  It demonstrates how easy it is to use various parts of the ShipEngine API in Python.


Installation & Usage
-------------------------------------
You can run the sample app directly on your system if you have [Python 3](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/) installed.  Or, if you have [Docker](https://www.docker.com/products/docker-desktop) installed, then you can run the app as a Docker container.


### Local installation
You can run the app on your local system if you have [Python 3](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/) installed.


**1. Install dependencies**
```
pip install -r requirements.txt
```


**2. Run the app**
```
python app.py
```


### Docker
If you have [Docker](https://www.docker.com/products/docker-desktop) installed, then you can run the app as a Docker container.

**1. Build the image**
```
docker build --tag se_python_sample_app .
```

> **Note:* Don't forget the period (`.`) at the end of this command


**2. Run the container**
```
docker run -it se_python_sample_app
```
