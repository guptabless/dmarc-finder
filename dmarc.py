import requests
from bs4 import BeautifulSoup
import bcolors
import argparse
import sys
import os

def banner():
    print("""

            ██████╗░███╗░░░███╗░█████╗░██████╗░░█████╗░░░░░░░███████╗██╗███╗░░██╗██████╗░███████╗██████╗░
            ██╔══██╗████╗░████║██╔══██╗██╔══██╗██╔══██╗░░░░░░██╔════╝██║████╗░██║██╔══██╗██╔════╝██╔══██╗
            ██║░░██║██╔████╔██║███████║██████╔╝██║░░╚═╝█████╗█████╗░░██║██╔██╗██║██║░░██║█████╗░░██████╔╝
            ██║░░██║██║╚██╔╝██║██╔══██║██╔══██╗██║░░██╗╚════╝██╔══╝░░██║██║╚████║██║░░██║██╔══╝░░██╔══██╗
            ██████╔╝██║░╚═╝░██║██║░░██║██║░░██║╚█████╔╝░░░░░░██║░░░░░██║██║░╚███║██████╔╝███████╗██║░░██║
            ╚═════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░░░░░░░╚═╝░░░░░╚═╝╚═╝░░╚══╝╚═════╝░╚══════╝╚═╝░░╚═╝
                                                                                               code by NG        
    """)

if len(sys.argv) > 1:
    banner()
    if (sys.argv[1] == '-d'):
        try:
            input_site = sys.argv[2]
            parser = argparse.ArgumentParser()
            parser.add_argument("-d", required=True)
            args = parser.parse_args()
            if (os.path.exists(input_site) == True):
                file = open(input_site, "r")
                lines = file.readlines()
                for web_url in lines:
                    strip_web_url = web_url.strip()
                    print("**************************************************************************" + '\n')
                    print('URL' , strip_web_url)
                    full_input_site = 'https://' + strip_web_url
                    print('Web site Full URL', full_input_site)
                    status_input = requests.get(full_input_site).status_code
                    if (status_input == 200):
                        url = 'https://stopemailfraud.proofpoint.com/dmarc/?lookup=' + strip_web_url
                        print('Full url', url)
                        input_text = requests.get(url)
                        b_text = BeautifulSoup(input_text.text, 'html.parser')
                        for div in b_text.find_all('div', {"id": "dmarc-record-raw"}):
                         if div != None:
                            print(bcolors.OKMSG + div.text)
                            p_value = (div.text)[12]
                            if (p_value == 'r'):
                                print(bcolors.ERRMSG + 'Dmarc records are properly set')
                            elif (p_value == 'q'):
                                print(bcolors.OKMSG + 'Dmarc record set to quartine')
                            elif (p_value == 'n'):
                                print(bcolors.ERRMSG + 'Dmarc record set are not set properly ')
                         else:
                             print("Not reacheabl domain")
            elif (os.path.exists(input_site) == False):
             full_input_site = 'https://' + input_site
             print('Web site Full URL', full_input_site)
             status_input = requests.get(full_input_site).status_code
            if(status_input ==200):
                url =  'https://stopemailfraud.proofpoint.com/dmarc/?lookup=' + input_site
                print('Full url',url)
                input_text = requests.get(url)
                b_text = BeautifulSoup(input_text.text,'html.parser')
                for div in b_text.find_all('div', {"id": "dmarc-record-raw"}):
                    if  div != None:
                     print(bcolors.OKMSG + div.text)
                     p_value = (div.text)[12]
                     if(p_value == 'r'):
                         print('Dmarc records are properly set')
                     elif(p_value == 'q'):
                         print('Dmarc record set to quartine')
                     elif(p_value == 'n'):
                         print('Dmarc record set are not set properly ')

        except:
            print(bcolors.ERR + 'This domain is not reachable')

    elif (sys.argv[1] == '-h'):
        print(bcolors.BOLD + 'usage: damrc.py [-h] -d Domain' '\n' 'OPTIONS:' '\n' '-h,--help    '
                             'show this help message and exit' '\n''-d Domain,   --domain DOMAIN for which you want to search damrc record')
    elif (sys.argv[1] != '-d'):
        print(bcolors.OKMSG + 'Please enter -d < valid domain without http:// or https:// >')
else:
    banner()
    print(bcolors.ERR + 'Please select at-least 1 option from -d or -h, with a valid domain')
