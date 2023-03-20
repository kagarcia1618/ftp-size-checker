# FTP Size Checker

> Tested Working on: Python3.9.9

## Description

This tool is built for the purpose of identifying the total file size of a specific directory on a remote FTP server. 

## Getting Started

1. Clone this repository and create your own virtual environment.

```
git clone https://github.com/kagarcia1618/ftp-size-checker.git 
cd ftp-size-checker
python3.9 -m venv venv
source venv/bin/activate
```

2. Install the requirements.

```
pip install -r requirements.txt
```

## Usage

To use the script, simply execute the script as follows inside the created virtual environment and provide the required arguments.

```
python ftp-size-checker.py --host [FTP hostname/IP address]
```

## Arguments

| Argument | Value | Default |
| ------ | ------ | ------ |
| --host | FTP hostname or IP address (required) | N/A |
| --username | FTP username (optional) | anonymous |
| --password | FTP password (optional) | N/A |
| --directory | FTP directory (optional) | "/" |
| --timeout | Max timeout for fetching the FTP directory list (optional) | 60 secs |

## Sample Output
```
(venv) [kenneth@linux ftp-size-checker]$ python ftp-size-checker.py --host ftp.ebi.ac.uk --directory /pub/databases/RNAcentral
[INFO] FTP Host: ftp.ebi.ac.uk
[INFO] FTP Username: anonymous
[INFO] FTP Directory: /pub/databases/RNAcentral
[INFO] FTP Timeout: 60 secs
[SUCCESS] Total File Size in Directory: 946.8 GB
(venv) [kenneth@linux ftp-size-checker]$
```
