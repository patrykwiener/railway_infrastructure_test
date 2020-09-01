# Railway Infrastructure Test

[![patrykwiener](https://circleci.com/gh/patrykwiener/railway_infrastructure_test/tree/master.svg?style=svg)](https://circleci.com/gh/patrykwiener/railway_infrastructure_test/tree/master)

## Setup
Required Python version:
* [Python 3.8](https://www.python.org/downloads/) or higher.

Install external depencencies:
```bash
$ pip install -r requirements.txt
```

## Run

```bash
# simple run
python runner.py <params>

# display help
python runner.py -h
```
### Params
Required params:
* ```-in```, ```--input_database``` - railway object infrastructure database url containing table 'przebiegi' with test data
* ```-out```, ```--output_database``` - existing or not results database url

Additional params:
* ```-r```, ```--route_max_length``` - route max length

### Sample usage
```bash
python runner.py -in sqlite:///input_database.tdb2 -out sqlite:///output_database.tdb2 -r 5
```

### Run tests
```bash
python -m unittest discover -s tests
```
