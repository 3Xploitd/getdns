# getdns

A python-based tool which automates the process of obtaining the dns records for a domain.

## install

Install by cloning the repo:
`git clone https://github.com/3Xploitd/getdns.git`

Install dnspython dependency with: `pip install dnspython`

## Usage:

~~~python
usage: getdns.py [-h] (-d DOMAIN | -f FILE)

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Domain Name to query
  -f FILE, --file FILE  File containing a list of domains to query
~~~
