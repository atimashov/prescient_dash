# Prescient dashboard
AI dashboard

## Prerequisites
It's simple tutorial how to create **virtual environment** and than **install** automatically there all **necessary packages**.
It's convenient because you can use these packages only in your project boundaries. Any problems related with project will not affec system in general.

### Step 1: Install pip3 if it is already not installed on your system
To check which vesion of pip3 is installed on your system run following command: 

`$ pip3 -V`

If pip is not installed, it's necessary to run the following commands:

`$ sudo apt-get update`

`$ sudo apt install python3-pip`

To install any package use following command:

`$ pip3 install [package-name]`

### Step 1 (a) Install required python version if it's not installed yet
I'll give example for python 3.7
`$ sudo apt install python3.7-minimal`
To install virtual environment with specific python version* it's necessary to run following command as well:
`$ sudo apt-get install python3.7-venv`

* Instead of `python 3 ...` use `python 3.7 ...`

### Step 2: Install Python3-venv and than create a virtual environment
Firstly you have to install *python3-venv* package on your system:
`$ sudo apt install -y python3-venv`

Navigate to directory where your virtual environment will be placed (Usually it's project directory):

`$ cd your_directory`

If you don't have this directory you can create it by:

`$ mkdir environment_directory`

Create virtual environment:

`$ python3 -m venv environment_name`

Activate virtual environment:

`$ source environment_name/bin/activate`

Deactivate virtual environment:

`deactivate`

### Step 3: Working with required / installed packages by *txt file*
If you have file **requirements.txt** with all necessary packages and want to install them:

`$ pip install -r requirements.txt`

If you need to create file **requirements.txt** with all packages that you use for your project:

`pip freeze > requirements.txt`
