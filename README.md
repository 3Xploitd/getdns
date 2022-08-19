# getdns

A python-based tool which automates the process of obtaining the dns records for a domain.

# getsubs

Another python-based tool integrated with getdns to obtain subdomains for a particular domain.

## Usage:
getdns has two arguments, one specifying the tool to use with either `-d` for getdns, or `-s` for `getsubs` and the other is the domain to query. For example:
`./getdns.py -d example.com` or `./getdns.py -s example.com`
