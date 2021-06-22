# Oxwall export

Python script to export the data from [Oxwall](https://www.oxwall.com/) sites.
The script does the next steps:

* Extracts the data directly from the database.
* Create the directory structure of projects and groups inside each project
* Fills a json file for each topic inside the group directory containing all the
    posts data.

## Installation

```bash
git clone https://github.com/lyz-code/oxwall-export
cd oxwall-export
virtualenv env
source env/bin/activate
pip install -r requirements
```

## Usage

```bash
python oxwall_export.py
```
