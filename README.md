# Creditshelf-Collisions

This application is a Flask application which interactively shows the information of collisions of cyclists and bike stations.

## Installation

Clone the project
```bash
https://github.com/arunkumarry/creditshelf-collisions.git
```
Create a python virtual env with [python3.9](https://www.python.org/downloads/)

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
cd creditshelf-collisions/
pip install virtualenv
python3.9 -m venv venv
pip install -r requirements.txt
```

## Setup MongoDB
For mac
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

For Ubuntu
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl status mongod
```

## Start the application

```bash
export FLASK_APP=run.py
flask run
```

Open [localhost in browser](http://localhost:5000) (Maps may not work fine as the data will be unavailable before running scripts).

## Running the scripts
Running the scripts to get collisions data and bike stations data from external sources and saving in mongodb.(The flask app should be running before running these scripts)

To get collisions data by Borough
```bash
cd scripts/
python get_cycle_collisions_by_borough.py BRONX
```

To get bike stations data by year.(This process takes sometime to extract download csv file and saving to DB)
```bash
cd scripts/
python get_bike_data_by_year.py
```

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License