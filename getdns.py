#!/usr/bin/python
import dns.resolver
import sys
import re
import requests

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


def getsuddomains(domain):
    subdomains = requests.get('https://crt.sh/?Identity={}'.format(domain)).text
    subdomain_list = re.findall(r'[\w\-_\.\*]+?\.{}'.format(domain),subdomains)
    subdomains_final = set()
    for each in subdomain_list:
        if each.startswith('*') == True:
            each = each[2:]
        subdomains_final.add(each)
   # loop = True
   # results=0
   # while loop:
   #     try:
   #         google_search = requests.get('https://google.com/?q=site:'+domain+'&start='+str(results)).text
   #         results+=10
   #         subdomain_list = re.findall(r'[\w\-_\.\*]+?\.{}'.format(domain),google_search)
   #         for each in subdomain_list:

   #             subdomains_final.add(each)
   #         print(len(subdomains_finals))
   #         for each in subdomains_final:
   #             print(each)
   #     except:
   #         loop = False
   #         break

    for each in sorted(subdomains_final):
        print(each)

    print("\n","{} unique subdomains were discovered for {}".format(len(subdomains_final),domain))
if sys.argv[1] == '-d':
    getdns(sys.argv[2])
elif sys.argv[1] == '-s':
    getsuddomains(sys.argv[2])

else:
    print("SyntaxError: Must specifiy which tool to use (ex. python3 getdns.py -d DOMAIN or python3 getdns.py -s DOMAIN)")
sys.exit()
