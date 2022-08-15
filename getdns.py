#!/usr/bin/python
import dns.resolver
import sys
import re

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

getdns(sys.argv[1])
sys.exit()
