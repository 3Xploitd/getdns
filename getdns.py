#!/usr/bin/python
import dns.resolver
import sys
import re
import requests
import argparse
from pathlib import Path
from urllib.parse import urlparse

def dns_query(domain):

    if args.file or args.domain != None:
        if args.file:
            domain_list = open(domain,'r').readlines()
            for domain in domain_list:
                domain = domain.strip()
                if domain[0:4] == 'http':
                    domain = getbase_domain(domain)
                results = getdns(domain)


        else:
            domain = domain.strip()
            if domain[0:4] == 'http':
                domain = getbase_domain(domain)
            results = getdns(domain)

def getbase_domain(domain):
    domain = domain.strip()
    domain = urlparse(domain)[1]
    if domain.count('/') >= 1:
        domain = domain[0:(domain.find('/'))]
    if domain.count('.') >= 2:
        subdomain_number = domain.count('.')
        domain = domain.split('.')
        for number in range(0,subdomain_number-1):
            domain.remove(domain[0])
        domain = ".".join(domain)

    return domain

def getdns(domain):

    dns_records = {}
    record_types = ['a','aaaa','mx','soa','ptr','cname','ns','txt','srv','info','caa']
    for each in record_types:
        try:
            query = list(dns.resolver.resolve(domain,each))
            dns_records[each] = query

        except:
            continue


    print('The following DNS records were identified for domain, {}:\n'.format(domain))

    for each in dns_records.keys():

        if each.lower() == 'a':
            dns_data = re.findall(r'<.*?:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?>',str(dns_records.get(each)).replace('"',''))
        elif each.lower() == 'mx':
            dns_data = re.findall(r'<.*?:\s\d*?\s([\w\W]+?)\.*?>',str(dns_records.get(each)).replace('"',''))
        elif each.lower() == 'aaaa':
            dns_data = re.findall(r'<.*?:\s([\d\w:]{1,32})\.*?>',str(dns_records.get(each)).replace('"',''))

        else:
            dns_data = re.findall(r'<.*?:\s([\w\W]+?)\.*?>',str(dns_records.get(each)).replace('"',''))
        dns_data = ", ".join(dns_data)

        print(each.upper(),'--> ',dns_data)


def getsubdomains(domain):
    subdomains = requests.get('https://crt.sh/?Identity={}'.format(domain)).text
    subdomain_list = re.findall(r'[\w\-_\.\*]+?\.{}'.format(domain),subdomains)
    subdomains_final = set()
    for each in subdomain_list:
        if each.startswith('*') == True:
            each = each[2:]
        subdomains_final.add(each)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d','--domain',help='Domain Name to query',action='store')
    group.add_argument('-f','--file',help='File containing a list of domains to query',action='store')
    args = parser.parse_args()

    if args.file != None:
        domain = args.file
        if Path(domain).is_file() == False:
            print('Argument -f/--file used but value is not a file, please use "-d/--domain"')
            sys.exit()
    else:
        domain = args.domain
        if Path(domain).is_file() == True:
            print('Argument -d/--domain used but value is a file, please use "-f/--file"')
            sys.exit()

    dns_query(domain)

