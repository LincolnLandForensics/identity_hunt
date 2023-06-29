#!/usr/bin/python
# coding: utf-8

# <<<<<<<<<<<<<<<<<<<<<<<<<<      Copyright        >>>>>>>>>>>>>>>>>>>>>>>>>>

# Copyright (C) 2023 LincolnLandForensics
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2, as published by the
# Free Software Foundation
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details (http://www.gnu.org/licenses/gpl.txt).

# <<<<<<<<<<<<<<<<<<<<<<<<<<      Imports        >>>>>>>>>>>>>>>>>>>>>>>>>>

try:
    from bs4 import BeautifulSoup
    import xlsxwriter
except:
    print('install missing modules:    pip install -r requirements_identity_hunt.txt')
    exit()

import os
import re
import sys
import json
import time
import random
import socket
import requests
import datetime
import argparse  # for menu system
from subprocess import call
from tkinter import * 
from tkinter import messagebox

# import phonenumbers
# from phonenumbers import geocoder, carrier


# <<<<<<<<<<<<<<<<<<<<<<<<<<      Pre-Sets       >>>>>>>>>>>>>>>>>>>>>>>>>>

author = 'LincolnLandForensics'
description = "OSINT: track people down by username, email, ip, phone and website"
tech = 'LincolnLandForensics'  # change this to your name if you are using Linux
version = '2.8.5'

# Regex section
regex_host = re.compile(r'\b((?:(?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+(?i)(?!exe|php|dll|doc' \
                        '|docx|txt|rtf|odt|xls|xlsx|ppt|pptx|bin|pcap|ioc|pdf|mdb|asp|html|xml|jpg|gif$|png' \
                        '|lnk|log|vbs|lco|bat|shell|quit|pdb|vbp|bdoda|bsspx|save|cpl|wav|tmp|close|ico|ini' \
                        '|sleep|run|dat$|scr|jar|jxr|apt|w32|css|js|xpi|class|apk|rar|zip|hlp|cpp|crl' \
                        '|cfg|cer|plg|lxdns|cgi|xn$)(?:xn--[a-zA-Z0-9]{2,22}|[a-zA-Z]{2,13}))(?:\s|$)')

regex_md5 = re.compile(r'^([a-fA-F\d]{32})$')  # regex_md5        [a-f0-9]{32}$/gm
regex_sha1 = re.compile(r'^([a-fA-F\d]{40})$')  # regex_sha1
regex_sha256 = re.compile(r'^([a-fA-F\d]{64})$')  # regex_sha256
regex_sha512 = re.compile(r'^([a-fA-F\d]{128})$')  # regex_sha512

regex_number = re.compile(r'^(^\d)$')  # regex_number    #Beta

regex_ipv4 = re.compile('(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}' +
                        '(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
regex_ipv6 = re.compile('(S*([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}S*|S*(' +
                        '[0-9a-fA-F]{1,4}:){1,7}:S*|S*([0-9a-fA-F]{1,4}:)' +
                        '{1,6}:[0-9a-fA-F]{1,4}S*|S*([0-9a-fA-F]{1,4}:)' +
                        '{1,5}(:[0-9a-fA-F]{1,4}){1,2}S*|S*([0-9a-fA-F]' +
                        '{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}S*|S*(' +
                        '[0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}S*' +
                        '|S*([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4})' +
                        '{1,5}S*|S*[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4})' +
                        '{1,6})S*|S*:((:[0-9a-fA-F]{1,4}){1,7}|:)S*|::(ffff' +
                        '(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}' +
                        '[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[' +
                        '0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[' +
                        '0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[' +
                        '0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')

regex_phone = re.compile('(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
regex_phone11 = re.compile(r'^1\d{10}$')
regex_phone2 = re.compile(r'(\d{3}) \W* (\d{3}) \W* (\d{4}) \W* (\d*)$')




# Color options
if sys.platform == 'win32' or sys.platform == 'win64':
    # if windows, don't use colors
    (r, o, y, g, b) = ('', '', '', '', '')
else:
    r = '\033[31m'  # red
    o = '\033[0m'  # off
    y = '\033[33m'  # yellow
    g = '\033[32m'  # green
    b = '\033[34m'  # blue

# Store bash color values
CRED = '\033[91m'  # red
CORNG = '\033[33m' # orange
CYEL = '\033[93m'  # yellow
CGRN = '\033[32m'  # green
CBHL = '\033[34m'  # blue
CVLT = '\033[35m'  # violet
CEND = '\033[0m'   # reset

print(CRED + '~~~red~~~ ' + CEND)

   
# <<<<<<<<<<<<<<<<<<<<<<<<<<      Menu           >>>>>>>>>>>>>>>>>>>>>>>>>>

def main():

    # check internet status
    status = internet()
    if status == False:
        noInternetMsg()
        print(CRED + '\nCONNECT TO THE INTERNET FIRST\n' + CEND)
        exit()
    else:
        print(CGRN + '\nINTERNET IS CONNECTED\n' + CEND)

    # global section
    global filename
    filename = 'input.txt'
    global Spreadsheet
    Spreadsheet = 'Intel_.xlsx'
    # global inputDetails
    # inputDetails = 'no'


    global row
    row = 1

    global emails
    global ips
    global phones
    global users
    global dnsdomains
    global websites
    
    emails = []
    ips = []
    phones = []
    users = []
    dnsdomains = []
    websites = [] 
    
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-I', '--input', help='', required=False)
    parser.add_argument('-O', '--output', help='', required=False)
    parser.add_argument('-E','--emailmodules', help='email modules', required=False, action='store_true')
    parser.add_argument('-H','--howto', help='email modules', required=False, action='store_true')
    parser.add_argument('-i','--ips', help='ip modules', required=False, action='store_true')
    parser.add_argument('-p','--phonestuff', help='phone modules', required=False, action='store_true')
    parser.add_argument('-s','--samples', help='print sample inputs', required=False, action='store_true')
    parser.add_argument('-t','--test', help='testing individual modules', required=False, action='store_true')
    parser.add_argument('-U','--usersmodules', help='username modules', required=False, action='store_true')
    parser.add_argument('-w','--websitetitle', help='websites titles', required=False, action='store_true')    

    parser.add_argument('-W','--websites', help='websites modules', required=False, action='store_true')    
    
    args = parser.parse_args()
    cls()
    print_logo()

    if args.samples:  
        samples()
        return 0
    if args.input:
        filename = args.input
    if args.output:
        Spreadsheet = args.output        

    create_ossint_xlsx()    # create the spreadsheet    
    master()   # re-print(original input list as 1-master and separate emails, ips, phones & users


    # Check if no arguments are entered
    if len(sys.argv) == 1:
        print('You didnt select any options so Ill run the major options')
        print('try -h for a listing of all menu options')
        args.emailmodules = True
        args.ips = True
        args.phonestuff = True
        args.usersmodules = True
        args.websites = True
    
    if args.howto:  # this section might be redundant
        parser.print_help()
        usage()
        return 0

    if args.emailmodules:  
        # BingEmail()    # alpha
        # emailrep() #alpha "too many requests"
        # facebookemail()    # todo  https://facebook.com/search/top/?q=kevinrose@gmail.com

        # flickremail()    # alpha  add scraper Invalid API Key
        ghunt()
        # GoogleScrapeEmail() # todo
        holehe_email()
        # lifestreamemail()# alpha
        # linkedinemail()    # alpha stopped working
        # myspaceemail()    # all false postives
        # naymzemail()    # beta
        # nikeplusemail()    # need login
        osintIndustries_email()
        # piplemail()# add info    (takes 90 seconds per email)
        # spokeo()    # needs work    (timeout error)
        # stumbluponemail()# alpha need login
        thatsthememail()    # https://thatsthem.com/email/smooth8101@yahoo.com
        twitteremail()    
        wordpresssearchemail()  # works
        # youtube_email()   # false positives
        # YelpEmail()# alpha
        
    if args.ips:  
        print("checking :", ips)
        # geoiptool() # works but need need to rate limit; expired certificate breaks this
        resolverRS()
        thatsthemip()
        whoisip()   
        whatismyip() # alpha
        
    # phone modules
    if args.phonestuff:
        thatsthemphone()
        # fouroneone()   # https://www.411.com/phone/1-417-967-2020
        # phonecarrier()  #beta
        reversephonecheck()
        spydialer()
        validnumber()    #beta
        whitepagesphone()
        whocalld()
        
    if args.test:  
        whocalld()

    if args.usersmodules:  
        about()
        bitbucket() # add fullname
        blogspot_users()
        disqus()    # test
        # ebay()  # all false positives due to captcha
        etsy()
        facebook()  # works
        flickr()   # add photo, note, name, info
        freelancer()
        friendfinder()
        foursquare()    # works
        garmin()
        gravatar()
        imageshack()    # works
        instagram()
        instructables() # works
        # keybase()   # pre-alpha
        # kickstarter() # access denied    
        kik()   
        # linkedin()  # needs auth
        # mapmytracks() # always 404
        massageanywhere()   # alpha
        # mastadon() # task    
        myshopify()
        myspace_users()
        paypal()  # needs work
        patreon()
        pinterest() # works
        poshmark()    
        public()    
        snapchat()    # must manually verify
        spotify()   # works
        # telegram() # task
        tiktok()
        tinder() # add dob, schools
        truthSocial() 
        #   # alpha https://www.tripadvisor.com/Profile/kevinrose
        # twitter()   # needs auth
        # venmo() # fails CloudFront
        wordpress() # works
        wordpressprofiles()  
        # yelp()   # random usernames         
        youtube()   # works
        familytree()
        sherlock()
        whatsmyname()

    if args.websitetitle:  
        titles()    # alpha
        
    if args.websites:  
        # Bing()# alpha
        redirect_detect()
        robtex()
        titles()    # alpha
        viewdnsdomain()
        whoiswebsite()    # works

    # set linux ownership    
    if sys.platform == 'win32' or sys.platform == 'win64':
        pass
    else:
        call(["chown %s.%s *.xlsx" % (tech.lower(), tech.lower())], shell=True)

    workbook.close()
    input(f"See '{Spreadsheet}' for output. Hit Enter to exit...")
   
    return 0
    
    # exit()  # this code is unreachable


# <<<<<<<<<<<<<<<<<<<<<<<<<<   Sub-Routines   >>>>>>>>>>>>>>>>>>>>>>>>>>

def cls():
    linux = 'clear'
    windows = 'cls'
    os.system([linux, windows][os.name == 'nt'])

def master():
    global row  # The magic to pass row globally
    style = workbook.add_format()
    color = 'white'

    if os.path.getsize(filename) == 0:
        input(f"'{filename}' is empty. fill it with username, email, ip, phone and websites.")
        sys.exit()
    elif os.path.isfile(filename):
        inputfile = open(filename)
    else:
        input(f"See '{filename}' does not exist. Hit Enter to exit...")
        sys.exit()
        
    for eachline in inputfile:
        
        (query, ranking, fullname, url, email , user) = ('', '', '', '', '', '')
        (phone, ip, entity, fulladdress, city, state) = ('', '', '', '', '', '')
        # (ipv6) = ('')
        (zip, country, note, aka, dob, gender) = ('', '', '', '', '', '')
        (info, misc, lastname, firstname, middlename, friend) = ('', '', '', '', '', '')
        (otherurls, otherphones, otheremails, case, sosfilenumber, president) = ('', '', '', '', '', '')
        (sosagent, managers, dnsdomain, dstip, srcip  ) = ('', '', '', '', '')
        (content, referer, osurl, titleurl, pagestatus) = ('', '', '', '', '')
        # (ips, emails, phones) = ('', '', '') # test
        
        (color) = 'white'
        style.set_bg_color('white')  # test

        eachline = eachline + "\t" * 40
        eachline = eachline.split('\t')  # splits by tabs

        query = (eachline[0].strip())
        ranking = (eachline[1].strip())
        if ranking == '':
            ranking = '1-master'
        fullname = (eachline[2].strip())
        url = (eachline[3].strip())
        email = (eachline[4].strip())
        user = (eachline[5].strip())
        phone = (eachline[6].strip())
        ip = (eachline[7].strip())
        entity = (eachline[8].strip())
        fulladdress = (eachline[9].strip())
        city = (eachline[10].strip())
        state = (eachline[11].strip())
        zip = (eachline[12].strip())
        country = (eachline[13].strip())
        note = (eachline[14].strip())
        aka = (eachline[15].strip())
        dob = (eachline[16].strip())
        gender = (eachline[17].strip())
        info = (eachline[18].strip())
        misc = (eachline[19].strip())
        lastname = (eachline[20].strip())
        firstname = (eachline[21].strip())
        middlename = (eachline[22].strip())
        friend = (eachline[23].strip())
        otherurls = (eachline[24].strip())
        otherphones = (eachline[25].strip())
        otheremails = (eachline[26].strip())
        case = (eachline[27].strip())
        sosfilenumber = (eachline[28].strip())
        president = (eachline[29].strip())
        sosagent = (eachline[30].strip())
        managers = (eachline[31].strip())
        dnsdomain = (eachline[32].strip())
        dstip = (eachline[33].strip())
        srcip = (eachline[34].strip())
        content = (eachline[35].strip())
        referer = (eachline[36].strip())
        osurl = (eachline[37].strip())
        titleurl = (eachline[38].strip())
        pagestatus = (eachline[39].strip())        

        # Regex data type
        if bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", query)):  # regex email    
            email = query
            user = email.split('@')[0]
            temp1 = [email]
            if query.lower() not in emails:            # don't add duplicates
                emails.append(email)
        elif re.search(regex_host, query):  # regex_host (Finds url and dnsdomain) # False positives for emails    # todo
            url = query
            if url.lower().startswith('http'):
                if url.lower() not in websites:            # don't add duplicates
                    websites.append(url)            
            else:
                logsource = 'IOC-dnsdomain'
                dnsdomain = query
            url = url.rstrip('/')
            if url.lower() not in websites:            # don't add duplicates
                websites.append(url)            
            dnsdomain = url.lower()
            dnsdomain = dnsdomain.replace("https://", "")
            dnsdomain = dnsdomain.replace("http://", "")
            dnsdomain = dnsdomain.split('/')[0]
            notes2 = dnsdomain.split('.')[-1]
            if dnsdomain.lower() not in dnsdomains:            # don't add duplicates
                dnsdomains.append(dnsdomain)
            
        elif re.search(regex_ipv4, query):  # regex_ipv4
            (ip) = (query)
            if query.lower() not in ips:            # don't add duplicates
                ips.append(ip)

        elif re.search(regex_ipv6, query):  # regex_ipv6
            (ip) = (query)
            if query.lower() not in ips:            # don't add duplicates
                ips.append(ip)

        elif re.search(regex_phone, query) or re.search(regex_phone11, query) or re.search(regex_phone2, query):  # regex_phone
            (phone) = (query)
            if query.lower() not in phones:            # don't add duplicates
                phones.append(phone)

            
        elif query.lower().startswith('http'):
            url = query
            if url.lower() not in websites:            # don't add duplicates
                websites.append(url)            
        elif query.strip() == '':
            print('blank input found')
        else:
            user = query
            if query.lower() not in users:            # don't add duplicates
                users.append(user)
            # (srcip, dstip) = (note, note)
            # logsource = 'IOC-IP'
        # elif re.search(regex_md5, note):  # regex_md5
            # logsource = 'IOC-Hash-Md5'
        # elif re.search(regex_sha256, note):  # regex_sha256
            # logsource = 'IOC-Hash-Sha256'
        # elif re.search(regex_sha1, note):  # regex_sha1
            # logsource = 'IOC-Hash-Sha1'
        # elif re.search(regex_sha512, note):  # regex_sha512
            # logsource = 'IOC-Hash-Sha512'

        # Read url,dnsdomain or dstip
        # if url != '':
            # (content, referer, osurl, titleurl, pagestatus) = request(url)
        # elif dnsdomain != '':
            # (content, referer, osurl, titleurl, pagestatus) = request(dnsdomain)
        # elif dstip != '':
            # (content, referer, osurl, titleurl, pagestatus) = request(dstip)
        # copy whole page
        # payload = content  # temp

        # color
        # if 'yahoo' in url:  
            # format_function(bg_color='orange')
        # elif 'google' in url:  #
            # format_function(bg_color='green')
        # elif 'Fail' in pagestatus:  #
            # format_function(bg_color='red')
        # else:
            # format_function(bg_color='white')

        # Write OSSINT excel
        write_ossint(query, ranking, fullname, url, email, user, phone, ip, entity, 
            fulladdress, city, state, zip, country, note, aka, dob, gender, info, 
            misc, lastname, firstname, middlename, friend, otherurls, otherphones, 
            otheremails, case, sosfilenumber, president, sosagent, managers, 
            dnsdomain, dstip, srcip, content, referer, osurl,
            titleurl, pagestatus)
    return users,ips,emails,phones


def about(): # testuser = kevinrose

    print('\n\t<<<<< Checking about.me against a list of users >>>>>')
    for user in users:    
        (fulladdress, city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '', '')
        (lastname, firstname) = ('', '')
        user = user.rstrip()
        url = ('https://about.me/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        for eachline in content.split("\n"):
            if " | about.me" in eachline:        
                fullname = eachline.strip().replace(" | about.me","") # .split("-")(0)

                if ' - ' in fullname:
                    fulladdress = fullname.split(' - ')[1]
                    fullname = fullname.split(' - ')[0]  
                    if ' ' in fullname:
                        fullname2 = fullname.split(' ')

                        firstname = fullname2[0]
                        lastname = fullname2[1]   
                    

        if '404' not in pagestatus:
            print(url, fullname) 
            write_ossint(user, '3 - about.me', fullname, url, '', user, '', '', '', fulladdress
                , city, '', '', country, '', '', '', '', '', '', lastname, firstname, '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', '', titleurl, pagestatus)        

def fastpeoplesearch():# testPhone= 385-347-1531
    print(y + '\n\t<<<<< Checking fastpeoplesearch against a list of ' + b + 'phone numbers' + y + ' >>>>>' + o)
    
    for phone in phones:
        (country, city, zip, case, note, content) = ('', '', '', '', '', '')
        (fullname, content, referer, osurl, titleurl, pagestatus)  = ('', '', '', '', '', 'research')
        phone = phone.replace('(','').replace(')','-').replace(' ','')
        # print('phone = >%s<' %(phone))     #temp   
        url = ('https://www.fastpeoplesearch.com/%s' %(phone))
        # (content, referer, osurl, titleurl, pagestatus) = request(url)    # protected by cloudflare

        for eachline in content.split("\n"):
            if "We could not find any results based on your search criteria" in eachline and case == '':
                print(r, "not found", o)  # temp
                url = ('')
            # elif "FastPeopleSearch for " in eachline:
                
                # fullname = eachline.split("FastPeopleSearch for ")[1]
                # print('fullname', fullname) # temp
                # note = eachline
        # pagestatus = ''        
                
        if url != '':
        # if ('%') not in url: 
            print(url) 
            write_ossint(phone, '9 - fastpeoplesearch', fullname, url, '', '', phone, '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', pagestatus)


def fouroneone():# testPhone= 385-347-1531
    print(y + '\n\t<<<<< Checking 411 against a list of ' + b + 'phone numbers' + y + ' >>>>>' + o)
    
    for phone in phones:
        (country, city, zip, case, note, content) = ('', '', '', '', '', '')
        (content, referer, osurl, titleurl, pagestatus)  = ('', '', '', '', '')
        phone = phone.replace('(','').replace(')','-').replace(' ','')
        # print('phone = >%s<' %(phone))     #temp   
        url = ('https://www.411.com/phone/%s' %(phone))
        # (content, referer, osurl, titleurl, pagestatus) = request(url)    # protected by cloudflare

        for eachline in content.split("\n"):
            if "No name associated with this number" in eachline and case == '':
                print("not found")  # temp
                url = ('')
            # elif "schema.org" in eachline:
                # print('oooh doggy') # temp
                # note = eachline
        pagestatus = ''        
                
        if url != '':
        # if ('%') not in url: 
            print(url) 
            write_ossint(phone, '9 - 411', '', url, '', '', phone, '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', referer, '', titleurl, pagestatus)


def blogspot_users(): # testuser = kevinrose
    print('\n\t<<<<< Checking blogspot against a list of users >>>>>')
    
    for user in users:
        url = f"https://{user}.blogspot.com"

        (content, referer, osurl, titleurl, pagestatus) = request_url(url)
        (fullname) = ('')

        if 'Success' in pagestatus:
            titleurl = titleurl_og(content)
            fullname = titleurl
            
            print(CGRN, url, CYEL, fullname, CBHL, pagestatus, CEND, titleurl)  # TEMP
            write_ossint(user, '4 - blogspot', fullname, url, '', user, '', '', '', ''
                , '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)


def bitbucket(): # testuser = kevinrose

    print('\n\t<<<<< Checking bitbucket against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        user = user.rstrip()
        url = ('https://bitbucket.org/%s/' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        
        # for eachline in content.split("\n"):
            # if "display_name" in eachline:
                # fullname = eachline
        
        if '404' not in pagestatus:
            # grab display_name = fullname
            print(url, titleurl) 
            write_ossint(user, '4 - bitbucket', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')   

                
def create_ossint_xlsx():
    global workbook
    workbook = xlsxwriter.Workbook(Spreadsheet)
    global sheet1
    sheet1 = workbook.add_worksheet('intel')
    headerformat = workbook.add_format({'bold': True, 'border': 1})
    sheet1.freeze_panes(1, 1)  # Freeze cells
    sheet1.set_selection('B2')

    # Excel column width
    sheet1.set_column(0, 0, 23) # query
    sheet1.set_column(1, 1, 14) # ranking
    sheet1.set_column(2, 2, 16) # fullname
    sheet1.set_column(3, 3, 25) # url
    sheet1.set_column(4, 4, 23) # email
    sheet1.set_column(5, 5, 14) # user
    sheet1.set_column(6, 6, 16) # phone
    sheet1.set_column(7, 7, 15) # ip
    sheet1.set_column(8, 8, 16) # entity
    sheet1.set_column(9, 9, 25) # fulladdress
    sheet1.set_column(10, 10, 15) # city
    sheet1.set_column(11, 11, 5) # state
    sheet1.set_column(12, 12, 7) # zip
    sheet1.set_column(13, 13, 8) # country
    sheet1.set_column(14, 14, 16) # note
    sheet1.set_column(15, 15, 15) # aka
    sheet1.set_column(16, 16, 12) # dob
    sheet1.set_column(17, 17, 7) # gender
    sheet1.set_column(18, 18, 15) # info
    sheet1.set_column(19, 19, 8) # misc
    sheet1.set_column(20, 20, 10) # lastname
    sheet1.set_column(21, 21, 10) # firstname
    sheet1.set_column(22, 22, 8) # middlename
    sheet1.set_column(23, 23, 17) # friend
    sheet1.set_column(24, 24, 15) # otherurls
    sheet1.set_column(25, 25, 15) # otherphones
    sheet1.set_column(26, 26, 15) # otheremails
    sheet1.set_column(27, 27, 12) # case
    sheet1.set_column(28, 28, 9) # sosfilenumber
    sheet1.set_column(29, 29, 12) # president
    sheet1.set_column(30, 30, 12) # sosagent
    sheet1.set_column(31, 31, 12) # managers
    sheet1.set_column(32, 32, 16) # dnsdomain
    sheet1.set_column(33, 33, 12) # dstip
    sheet1.set_column(34, 34, 12) # srcip
    sheet1.set_column(35, 35, 9) # content
    sheet1.set_column(36, 36, 9) # referer
    sheet1.set_column(37, 37, 6) # osurl
    sheet1.set_column(38, 38, 10) # titleurl
    sheet1.set_column(39, 39, 12) # pagestatus

    # Write column headers

    sheet1.write(0, 0, 'query', headerformat)
    sheet1.write(0, 1, 'ranking', headerformat)
    sheet1.write(0, 2, 'fullname', headerformat)
    sheet1.write(0, 3, 'url', headerformat)
    sheet1.write(0, 4, 'email', headerformat)
    sheet1.write(0, 5, 'user', headerformat)
    sheet1.write(0, 6, 'phone', headerformat)
    sheet1.write(0, 7, 'ip', headerformat)
    sheet1.write(0, 8, 'business/entity', headerformat)
    sheet1.write(0, 9, 'fulladdress', headerformat)
    sheet1.write(0, 10, 'city', headerformat)
    sheet1.write(0, 11, 'state', headerformat)
    sheet1.write(0, 12, 'zip', headerformat)
    sheet1.write(0, 13, 'country', headerformat)
    sheet1.write(0, 14, 'note', headerformat)
    sheet1.write(0, 15, 'aka', headerformat)
    sheet1.write(0, 16, 'dob', headerformat)
    sheet1.write(0, 17, 'gender', headerformat)
    sheet1.write(0, 18, 'info', headerformat)
    sheet1.write(0, 19, 'misc', headerformat)
    sheet1.write(0, 20, 'lastname', headerformat)
    sheet1.write(0, 21, 'firstname', headerformat)
    sheet1.write(0, 22, 'middlename', headerformat)
    sheet1.write(0, 23, 'friend', headerformat)
    sheet1.write(0, 24, 'otherurls', headerformat)
    sheet1.write(0, 25, 'otherphones', headerformat)
    sheet1.write(0, 26, 'otheremails', headerformat)
    sheet1.write(0, 27, 'case', headerformat)
    sheet1.write(0, 28, 'sosfilenumber', headerformat)
    sheet1.write(0, 29, 'president', headerformat)
    sheet1.write(0, 30, 'sosagent', headerformat)
    sheet1.write(0, 31, 'managers', headerformat)
    sheet1.write(0, 32, 'dnsdomain', headerformat)
    sheet1.write(0, 33, 'dstip', headerformat)
    sheet1.write(0, 34, 'srcip', headerformat)
    sheet1.write(0, 35, 'content', headerformat)
    sheet1.write(0, 36, 'referer', headerformat)
    sheet1.write(0, 37, 'osurl', headerformat)
    sheet1.write(0, 38, 'titleurl', headerformat)
    sheet1.write(0, 39, 'pagestatus', headerformat)

    # hidden columns
    sheet1.set_column(33, 33, None, None, {'hidden': 1}) # dstip
    sheet1.set_column(34, 34, None, None, {'hidden': 1}) # srcip


def disqus(): # testuser = kevinrose

    print('\n\t<<<<< Checking discus against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        user = user.rstrip()
        url = ('http://disqus.com/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        
        if '404' not in pagestatus:
            # fullname = titleurl
            print(url) 
            write_ossint(user, '5 - discus', '', url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', pagestatus)        


def ebay(): # testuser = kevinrose

    print('\n\t<<<<< Checking ebay against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus, note) = ('', '', '', '', '', '')
        user = user.rstrip()
        url = ('https://www.ebay.com/usr/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        
        for eachline in content.split("\n"):
            if 'been an eBay member since' in eachline:
                note = ('%s %s' %(eachline.strip(), note))
        
        if 'The User ID you entered was not found' not in content:
            fullname = titleurl
            print(url, titleurl) 
            write_ossint(user, '9 - ebay', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', '', pagestatus)        

def emailrep():# testEmail= smooth8101@yahoo.com   
    print(y + '\n\t<<<<< Checking emailrep against a list of ' + b + 'emails' + y + ' >>>>>' + o)
    
    for email in emails:
        (country, city, zip, case, note) = ('', '', '', '', '')
        
        url = ('https://emailrep.io/%s' %(email))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        note = content
        for eachline in content.split("\n"):
            if "domain_exists" in eachline and "true" in eachline:
                print("domain_exists")  # temp
            elif "exceeded daily limit" in eachline:
                note = "exceeded daily limit"
                print(note)
            else:
                url = ('')
        pagestatus = ''                
        if url != '':
        # if ('%') not in url: 
            print(url, email) 
            write_ossint(email, '9 - emamilrep', '', url, email, '', '', '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', referer, '', titleurl, pagestatus)

def etsy(): # testuser = kevinrose https://www.etsy.com/people/kevinrose

    print('\n\t<<<<< Checking etsy against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        user = user.rstrip()
        url = ('https://www.etsy.com/people/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        if '404' not in pagestatus:
            # grab display_name = fullname
            print(url, titleurl) 
            write_ossint(user, '4 - etsy', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)   

def facebook(): # testuser = kevinrose

    print('\n\t<<<<< Checking facebook against a list of users >>>>>')
    for user in users:    
        (Success,FullName,LastName,FirstName,ID,Gender) = ('','','','','','')
        (Photo,Country,Website,Email,Language,Username) = ('','','','','','')
        (city, country) = ('', '')
        (content, referer, osurl, titleurl, pagestatus) = ('','','','','')
        user = user.rstrip()
        url = ('http://facebook.com/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        # try:
            # (content, referer, osurl, titleurl, pagestatus) = request(url)
        # except:
            # pass

        if 'Success' in pagestatus and 'vi-vn.facebook.com' in content:
            fullname = titleurl
            print(url, fullname) 
            write_ossint(user, '3 - Facebook', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)

def familytree(): 

    print('\n\t<<<<< familytree entry >>>>>')
    url = ('https://www.familytreenow.com/search/')
    write_ossint('', '9 - manual', '', url, '', '', '', '', '', ''
                , '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')

def flickr(): # testuser = kevinrose

    print('\n\t<<<<< Checking flickr against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus, content) = ('', '', '', '', '', '')
        (note) = ('')
        user = user.rstrip()
        url = ('https://www.flickr.com/people/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)

        for eachline in content.split("  <"):
            if "og:title" in eachline:
                fullname = eachline.strip().split("\"")[1]

        if '404' not in pagestatus and 'ail' not in pagestatus:
            if fullname.lower() == user.lower():
                fullname = ''
        
            print(url, titleurl) 
            write_ossint(user, '4 - flickr', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', pagestatus)        

           
def format_function(bg_color='white'):
    global format
    format = workbook.add_format({
        'bg_color': bg_color
    })


def foursquare():    # testuser=    john
    print('\n\t<<<<< Checking instagram against a list of users >>>>>')
    for user in users:    
        url = ('https://foursquare.com/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = ('','','','','')
        (fullname, info, note) = ('', '', '')
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)

            content = content.strip()
            titleurl = titleurl.strip()
       
        except:
            pass

        if ' on Foursquare' in titleurl:
            fullname = titleurl.rstrip(' on Foursquare')
        
            write_ossint(user, '7 - foursquare.com', fullname, url, '', user, '', '', '', ''
                , '', '', '', '', note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)
            print(g + url + o)    
            
            
def freelancer(): # testuser = kevinrose

    print('\n\t<<<<< Checking freelancer against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        user = user.rstrip()
        url = ('https://www.freelancer.com/u/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        titleurl = titleurl.replace(' Profile | Freelancer','')
        if '404' not in pagestatus:
            # for eachline in content.split("\n"):
                # if "\<title\>" in eachline:
                    # fullname = eachline.split('<title>')[1]
                    # print('hello world')
            
            if ' ' in titleurl:
                fullname = titleurl
            
            if fullname.lower() == user.lower():
                fullname = ''
            
            
            print(url, fullname) 
            write_ossint(user, '5 - freelancer', fullname, url, '', user, '', '', '', ''
                , '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        

def friendfinder():    # testuser=  kevinrose
    print('\n\t<<<<< Checking friendfinder against a list of users >>>>>')
    for user in users:    
        url = ('https://www.friendfinder-x.com/profile/%s' %(user))

        (content, referer, osurl, titleurl, pagestatus) = ('','','','','')
        (fullname, info, note) = ('', '', '')
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
      
        except:
            pass

        if 'Register to Find' not in titleurl:
            write_ossint(user, '7 - friendfinder.com', fullname, url, '', user, '', '', '', ''
                , '', '', '', '', note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)
            print(g + url + o)    

def garmin(): # testuser = kevinrose

    print('\n\t<<<<< Checking garmin against a list of users >>>>>')
    for user in users:    
        (Success, fullname, lastname, firstname, case, gender) = ('','','','','','')
        (photo, country, website, email, language, username) = ('','','','','','')
        (city) = ('')
        user = user.rstrip()

        url = ('https://connect.garmin.com/modern/profile/%s' %(user))

        (content, referer, osurl, titleurl, pagestatus) = request(url)
        
        # try:
            # (content, referer, osurl, titleurl, pagestatus) = request(url)
        # except:
            # pass
        # if 1==1:
        # print(content)
        # if user in content:
        if 'twitter:card' not in content:
        
            fullname = titleurl
            fullname = fullname.split(" (")[0]
            print(url, fullname) 
            write_ossint(user, '9 - garmin', '', url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', pagestatus)

 
def geoiptool():    # testuser= 77.15.67.232
    print('\n\t<<<<< Checking geodatatool.com against a list of IPs >>>>>')
    for ip in ips:
        (country, city, state, zip) = ('', '', '', '')
     
        # url = ('http://geoiptool.com/en/?IP=%s' %(ip))
        url = ('https://www.geodatatool.com/en/?IP=%s' %(ip))

        # (content, referer, osurl, titleurl, pagestatus) = request(url)    # certificate errors
        (content, referer, osurl, titleurl, pagestatus) = request_url(url)  # ignore certificates
        print(type(content))    # temp
        content2 = content.strip().split("\n")
        
        # for eachline in content:        
        for eachline in content2:
        
        # for eachline in content.split("\n"):
            print("Eachline = %s" %(eachline)) # temp

            if "Country: " in eachline:
                country = eachline.strip().split(": ")[1]
                country = country.split("<")[0]
            elif "City: " in eachline:
                city = eachline.strip().split(": ")[1]
                city = city.split("<")[0]            
            elif "Region: " in eachline:
                state = eachline.strip().split(": ")[1]
                state = state.split("<")[0]            
            elif "Postal Code: " in eachline:
                zip = eachline.strip().split(": ")[1]
                zip = zip.split("<")[0] 
        print(y + ip, country, city, state, zip +o)
        time.sleep(7) #will sleep for 30 seconds
        write_ossint(ip, '6 - geodatatool', '', url, '', '', '', ip, '', ''
        , city, state, zip, country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', pagestatus)

def ghunt():# testEmail= kevinrose@gmail.com   
    for email in emails:
        (note, url) = ('', '')
        note = ('cd C:\Forensics\scripts\python\git-repo\GHunt && ghunt email %s' %(email)) 
        if email.endswith('gmail.com'):
            ranking = ('8 - ghunt')
        else:
            ranking = ('9 - ghunt')  
        write_ossint(email, ranking, '', url, email, '', '', '', '', ''
        , '', '', '', '', note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'research')


def gravatar(): # testuser = kevinrose      http://en.gravatar.com/profiles/kevinrose.json

    print('\n\t<<<<< Checking gravatar against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        (info, lastname, firstname, note, otherurls) = ('', '','', '', '')
        user = user.rstrip()
        url = ('http://en.gravatar.com/profiles/%s.json' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        
        if 'ail' not in pagestatus:
            parsed_data = json.loads(content)

            info = parsed_data['entry'][0]['photos'][0]['value']


            if 'familyName' in content:
                firstname = parsed_data['entry'][0]['name']['givenName']
                lastname = parsed_data['entry'][0]['name']['familyName']
                fullname = parsed_data['entry'][0]['name']['formatted']
            if 'aboutMe' in content:
                note = parsed_data['entry'][0]['aboutMe']
                note = note.replace('&amp', '&')
                
            if 'urls\":[{\"value' in content and 'aboutMe' in content:

                # Extract the urls list from the JSON object
                urls = parsed_data['entry'][0]['urls']

                for url in urls:
                    otherurls = ('%s %s' %(url['value'], otherurls))

            url = ('http://en.gravatar.com/%s' %(user))
            print(url, fullname) 
            
            if fullname != '' or otherurls != '' or note != '': 
            
                write_ossint(user, '3 - gravatar', fullname, url, '', user, '', '', '', ''
                    , city, '', '', country, note, '', '', '', info, '', lastname, firstname, '', '', otherurls, '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        
            else:
                write_ossint(user, '7 - gravatar', fullname, url, '', user, '', '', '', ''
                    , city, '', '', country, note, '', '', '', info, '', lastname, firstname, '', '', otherurls, '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        


def holehe_email():# testEmail= kevinrose@gmail.com
    print(y + '\n\t<<<<< Checking holehe against a list of ' + b + 'emails' + y + ' >>>>>' + o)
    
    for email in emails:
        (country, city, zip, case) = ('', '', '', '')
        
        url = ('cd C:\Forensics\scripts\python\git-repo\holehe && holehe -NP --no-color --no-clear --only-used %s' %(email))
        write_ossint(email, '9 - manual', '', url, email, '', '', '', '', ''
            , '', '', '', '', 'https://github.com/megadose/holehe', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'research')

def imageshack(): # testuser = ToddGilbert

    print('\n\t<<<<< Checking imageshack against a list of users >>>>>')
    for user in users:    
        # (Success,FullName,LastName,FirstName,ID,Gender) = ('','','','','','')
        # (Photo,Country,Website,Email,Language,Username) = ('','','','','','')
        (city, country, fullname) = ('', '', '')
        user = user.rstrip()
        url = ('https://imageshack.com/user/%s' %(user))

        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except:
            pass

        if 's Images' in titleurl:
            # fullname = titleurl
            print(url) 
            write_ossint(user, '4 - imageshack', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', pagestatus)        

def instagram():    # testuser=    kevinrose     # add info
    print('\n\t<<<<< Checking instagram against a list of users >>>>>')
    for user in users:    
        url = ('https://instagram.com/%s/' %(user))
        (content, referer, osurl, titleurl, pagestatus) = ('','','','','')
        (fullname, info, note) = ('', '', '')
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
            
            
            
            content = content.strip()
            titleurl = titleurl.strip()
            for eachline in content.split("\n"):
                if "@context" in eachline:
                    content = eachline.strip()
                elif 'og:title' in eachline and 'content=\"' in eachline:
                    fullname = eachline.split('\"')[1].split(' (')[0]
                elif 'ProfilePage\",\"description' in eachline:
                    info = eachline
                    # Load the JSON data
                    data = json.loads(eachline)

                    # Extract the description value and print it
                    note = data['description']
       
        except:
            pass
            
        # time.sleep(1) # will sleep for 1 seconds
        if 'alternate' in content:
            
        
            write_ossint(user, '3 - instagram.com', fullname, url, '', user, '', '', '', ''
                , '', '', '', '', note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)
            print(g + url + o)    

 
def instagramtwo(): #alpha
    # from lib.colors import red,white,green,reset
    self = 'kevinrose'

    response = self.session.get(self.url)
    if response.status_code != 200:
        exit(f"[-] instagram: user not found{reset}")
    response = response.json()
    user = response['graphql']['user']
           
    data = {'Profile photo': user['profile_pic_url_hd'],
                 'Username': user['username'],
                 'User ID': user['id'],
                 'External URL': user['external_url'],
                 'Bio': user['biography'],
                 'Followers': user['edge_followed_by']['count'],
                 'Following': user['edge_follow']['count'],
                 'Pronouns': user['pronouns'],
                 'Images': user['edge_owner_to_timeline_media']['count'],
                 'Videos': user['edge_felix_video_timeline']['count'],
                 'Reels': user['highlight_reel_count'],
                 'Is private?': user['is_private'],
                 'Is verified?': user['is_verified'],
                 'Is business account?': user['is_business_account'],
                 'Is professional account?': user['is_professional_account'],
                 'Is recently joined?': user['is_joined_recently'],
                 'Business category': user['business_category_name'],
                 'Category': user['category_enum'],
                 'Has guides?': user['has_guides']
    }
    print
    
    print(f"\n{user['full_name']} | Instagram{reset}")
    for key, value in data.items():
       print(f"├─ {key}: {value}")


def instructables(): # testuser = kevinrose

    print('\n\t<<<<< Checking instructables against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        user = user.rstrip()
        url = ('https://www.instructables.com/member/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        if '404' not in pagestatus:
            fullname = titleurl
            print(url, titleurl) 
            write_ossint(user, '7 - instructables', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        

def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False
 
            
def ip_address(dnsdomain):
    (ip) = ('')
    """
    Ping the URL and return the IP address
    """
    try:
        ip = socket.gethostbyname(dnsdomain)
    except socket.gaierror:
        ip = ''
    return ip

        
def noInternetMsg():
    '''
    prints a pop-up that says "Connect to the Internet first"
    '''
    window = Tk()
    window.geometry("1x1")
      
    w = Label(window, text ='Translate-Inator', font = "100") 
    w.pack()
    messagebox.showwarning("Warning", "Connect to the Internet first") 

def keybase():    # testuser=    kevin
    print('\n\t<<<<< Checking keybase.io against a list of users >>>>>')
    for user in users:    
        url = ('https://keybase.io/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = ('','','','','')
        (fullname, info, note) = ('', '', '')
        (content, referer, osurl, titleurl, pagestatus) = request(url)

        try:
            # (content, referer, osurl, titleurl, pagestatus) = request(url)
            
            
            
            content = content.strip()
            titleurl = titleurl.strip()
            for eachline in content.split("\n"):
                if "@context" in eachline:
                    content = eachline.strip()
                elif 'og:title' in eachline and 'content=\"' in eachline:
                    fullname = eachline.split('\"')[1].split(' (')[0]
                elif 'ProfilePage\",\"description' in eachline:
                    info = eachline
                    # Load the JSON data
                    data = json.loads(eachline)

                    # Extract the description value and print it
                    note = data['description']
       
        except:
            pass
            
        # time.sleep(1) # will sleep for 1 seconds
        # if 'what you are looking for...it does not exist' not in content:
        # if 'Your conversation will be end-to-end encrypted' in content:
        if 'following' in content:
        
        
      
        
        # if 1==1:    
        
            write_ossint(user, '3 - keybase.com', fullname, url, '', user, '', '', '', ''
                , '', '', '', '', note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)
            print(g + url + o)    

def kickstarter(): # testuser = kevinrose
    print('\n\t<<<<< Checking kickstarter against a list of users >>>>>')
    for user in users:    
        (fullname, titleurl, pagestatus, content) = ('', '', '', '')
        (note, firstname, lastname, photo, misc, lastseen) = ('', '', '', '', '', '')

        user = user.rstrip()
        url = ('https://www.kickstarter.com/profile/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        # for eachline in content.split(","):
            # if "firstName" in eachline:
                # firstname = eachline.strip().split(":")[1]
                # firstname = firstname.strip('\"')
            # elif "lastName" in eachline:
                # lastname = eachline.strip().split(":")[1]
                # lastname = lastname.strip('\"')
            # elif "displayPicLastModified" in eachline:
                # note = eachline.strip().split(":")[1]
            # elif "displayPic\"" in eachline:
                # photo = eachline.strip().split(":\"")[1].replace("\\","")
            # fullname = ('%s %s' %(firstname,lastname))
        if '404' not in pagestatus:
            print("%s = %s" %(url, fullname)) # temp
            write_ossint(user, '9 - kickstarter', fullname, url, '', user, '', '', '', ''
                , '', '', '', '', note, '', '', '', '', misc, lastname, firstname, '', '', '', '', '', '', '', '', '', '', '', content, '', '', '', '', titleurl, pagestatus)        

    
def kik(): # testuser = kevinrose
    print('\n\t<<<<< Checking kik against a list of users >>>>>')
    for user in users:    
        (fullname, titleurl, pagestatus, content) = ('', '', '', '')
        (note, firstname, lastname, photo, misc, lastseen) = ('', '', '', '', '', '')
        (otherurl) = ('')
        user = user.rstrip()
        url = ('https://ws2.kik.com/user/%s' %(user))
        
        otherurl = ('http://kik.me/%s' %(user))
               
        
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        for eachline in content.split(","):
            if "firstName" in eachline:
                firstname = eachline.strip().split(":")[1]
                firstname = firstname.strip('\"')
            elif "lastName" in eachline:
                lastname = eachline.strip().split(":")[1]
                lastname = lastname.strip('\"')
            elif "displayPicLastModified" in eachline:
                note = eachline.strip().split(":")[1]
                # note = int(note)
                # from datetime import datetime
                # dt_object = datetime.fromtimestamp(lastseen)
                # note = ('last seen %s' %(dt_object))
                # print("dt_object =", dt_object)
                # print("type(dt_object) =", type(dt_object))                
                
            elif "displayPic\"" in eachline:
                photo = eachline.strip().split(":\"")[1].split("\"")[0].replace("\\","")
                
            fullname = ('%s %s' %(firstname,lastname))
            fullname = fullname.replace("\"}","")
        if '404' not in pagestatus:
            print("%s = %s" %(url, fullname)) # temp
            write_ossint(user, '4 - kik', fullname, otherurl, '', user, '', '', '', ''
                , '', '', '', '', photo, '', '', '', '', misc, lastname, firstname, '', '', url, '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        


def linkedin():    # testuser=    kevinrose     # grab info
    print('\n\t<<<<< Checking linkedin against a list of users >>>>>')
    for user in users:    
        (email, fullname, lastname,lastname,firstname) = ('', '', '', '', '')
        (content, referer, osurl, titleurl, pagestatus) = ('', '', '', '', '')
        
        otherurl = ('http://linkedin.com/in/%s' %(user))
        url = ('https://linkedin.com/search/results/all/?keywords=%s' %(user))
        

        
        (city, fullname, lastname, country) = ('', '','','')
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except:pass
        # if 1==1:
        if " LinkedIn" in titleurl:
            titleUrl = titleurl.replace("  | LinkedIn","")
            if titleurl.lower() != user.lower():
                fullname = titleurl
            
            if ' ' in fullname:
                fullname2 = fullname.split(" ")

                firstname = fullname2[0]
                lastname = fullname2[1]

            write_ossint(user, '9 - linkedin.com', '', url, '', '', '', '', email, ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', otherurl, '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)
            print(g , url, '\t', y , fullname ,  o)

def mapmytracks(): # testuser = kevinrose

    print('\n\t<<<<< Checking mapmytracks against a list of users >>>>>')
    for user in users:    
        (Success, fullname, lastname, firstname, case, gender) = ('','','','','','')
        (photo, country, website, email, language, username) = ('','','','','','')
        (city) = ('')
        user = user.rstrip()

        url = ('https://www.mapmytracks.com/%s' %(user))

        (content, referer, osurl, titleurl, pagestatus) = request(url)
        
        # try:
            # (content, referer, osurl, titleurl, pagestatus) = request(url)
        # except:
            # pass
        # if 1==1:
        # print(content)
        # if user in content:
        if 'nothing to see here' not in content:   # fixme
        
            fullname = titleurl
            fullname = fullname.split(" (")[0]
            print(url, fullname) 
            write_ossint(user, '9 - mapmytracks', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', titleurl, pagestatus)

def massageanywhere():    # testuser=   Misty0427
    print('\n\t<<<<< Checking massageanywhere against a list of users >>>>>')
    for user in users:    
        url = ('https://www.massageanywhere.com/profile/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = ('','','','','')
        (fullname, info, note, firstname, fulladdress) = ('', '', '', '', '')
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
       
        except:
            pass

        if 'Profile for' in titleurl:
            if 'MassageAnywhere.com Profile for ' in titleurl:  
                titleurl = titleurl.replace('MassageAnywhere.com Profile for ','')
                if ' of ' in titleurl:
                    # titleurl = titleurl.split(' of ')
                    fullname = titleurl.split(' of ')[0]
                    fulladdress = titleurl.split(' of ')[1]
                    
            write_ossint(user, '7 - massageanywhere.com', fullname, url, '', user, '', '', '', fulladdress
                , '', '', '', '', note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)
            print(g + url + o)    

def mastadon(): # testuser = kevinrose

    print('\n\t<<<<< Checking mastadon against a list of users >>>>>')
    for user in users:    
        (Success, fullname, lastname, firstname, case, gender) = ('','','','','','')
        (photo, country, website, email, language, username) = ('','','','','','')
        (city, note, info, email, content, pagestatus) = ('', '', '', '', '', '')
        (lastname, firstname, data) = ('', '', '')
        
        user = user.rstrip()
        url = ('https://mastodon.social/@%s' %(user))
        note = ('https://mastodon.social/api/v2/search?q=%s' %(user))

        (content, referer, osurl, titleurl, pagestatus) = request(url)

        for eachline in content.split("\n"):
            if "og:title" in eachline:
                fullname = eachline.strip().split("\"")[1].split(' (')[0]

        if 'accounts\":[{' in content:        
            data = json.loads(content)              # Convert JSON data to Python dictionary
            fullname = data["accounts"][0]["display_name"]
            info = data['accounts'][0]['avatar']
        
        if " " in fullname:
            firstname = fullname.split(" ")[0]
            lastname = fullname.split(" ")[1]
            print(data)
        if "uccess" in pagestatus and 'This resource could not be found' not in content:
            print(url, fullname) 
            write_ossint(user, '3 - mastadon', fullname, url, email, user, '', '', '', ''
               , city, '', '', country, note, '', '', '', info, '', lastname, firstname, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)

def myshopify():    # testuser=    rothys
    print('\n\t<<<<< Checking myshopify against a list of users >>>>>')
    for user in users:    
        url = ('https://%s.myshopify.com/' %(user))
        (content, referer, osurl, titleurl, pagestatus) = ('','','','','')
        (fullname, info, note, otherurls) = ('', '', '', '')
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
            content = content.strip()
            titleurl = titleurl.strip()
            for eachline in content.split("\n"):
                if "@context" in eachline:
                    content = eachline.strip()
                elif 'og:title' in eachline and 'content=\"' in eachline:
                    info = eachline.split('\"')[1].split(' (')[0]
                elif 'ProfilePage\",\"description' in eachline:
                    info = eachline
                    # # Load the JSON data
                    data = json.loads(eachline)

                    # # Extract the description value and print it
                    note = data['description']

        except:
            pass
            
        time.sleep(1) # will sleep for 1 seconds
        if 'Success' in pagestatus:

            response = requests.get(url)

            if response.history:
                otherurls = response.url
                note = ('redirects to %s' %(otherurls))

            write_ossint(user, '5 - myshopify.com', '', url, '', user, '', '', '', ''
                , '', '', '', '', note, '', '', '', info, '', '', '', '', '', otherurls, '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)
            print(g + url , "     " , y + note + o)    

def myspace_users():
    print('\n\t<<<<< Checking myspace against a list of users >>>>>')
    
    for user in users:
        url = f"https://myspace.com/{user}"

        (content, referer, osurl, titleurl, pagestatus) = request_url(url)
        (fullname) = ('')

        if 'Success' in pagestatus and ('Your search did not return any results') not in content:
            fullname = titleurl

            print(CGRN, url, CYEL, fullname, CEND, pagestatus)  # TEMP
            write_ossint(user, '4 - myspace', fullname, url, '', user, '', '', '', ''
                , '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)

         
def myspaceemail():# testEmail= kandyem@yahoo.com   267619602
    print(y + '\n\t<<<<< Checking myspace against a list of ' + b + 'emails' + y + ' >>>>>' + o)
    
    for email in emails:
        (fullname, country, city, zip, case) = ('', '', '', '', '')
        (content, referer, osurl, titleurl, pagestatus) = ('', '', '', '', '')
        url = ('http://www.myspace.com/search/people?q=%s&ac=t' %(email))
        # (content, referer, osurl, titleurl, pagestatus) = request(url)
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except:
            pass        

        for eachline in content.split("\n"):
            if 'Your search did not return any results' in eachline:
                print('hello world')
            
            if "data-id" in eachline and case == '':
                case = eachline.strip().split(" data-id=")[1]
                case = case.replace("\"", "").split(" ")[0]
                url = ('https://myspace.com/%s' %(case))
            elif "og:title" in eachline:
                fullname = eachline.strip().split("\"")[1].replace('Search Myspace','')
                print(fullname) # temp

        if ('%') not in url and ('Your search did not return any results') not in content: 
            print(url, email) 
            write_ossint(email, '9 - myspace.com', fullname, url, email, '', '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'test', '', '', content, '', '', pagestatus)

def osintIndustries_email():

    print('\n\t<<<<< osint.Industries entry >>>>>')
    url = ('https://osint.industries/email#')
    write_ossint('', '9 - manual', '', url, '', '', '', '', '', ''
                , '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')
    
    
def patreon(): # testuser = kevinrose

    print('\n\t<<<<< Checking patreon against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        (note) = ('')
        user = user.rstrip()
        url = ('https://www.patreon.com/%s/creators' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        if '404' not in pagestatus:
            titleurl = titleurl.replace(' Patreon','')
            if ' | ' in titleurl:   
                fullname = titleurl.split(' | ')[0]
                if user == fullname:
                    fullname = ''
                note = titleurl.split(' | ')[1]
            print(url, titleurl) 
            write_ossint(user, '5 - patreon', fullname, url, '', user, '', '', '', ''
                , '', '', '', '', note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        


def paypal(): # testuser = kevinrose

    print('\n\t<<<<< Checking paypal against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        (fulladdress, lastname, firstname) = ('', '', '')
        
        user = user.rstrip()
        url = ('https://www.paypal.com/paypalme/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        (note) = ('')
        if '404' not in pagestatus:
            for eachline in content.split("\n"):
                if eachline == "": pass                                             # skip blank lines
                else:
                    # define the regular expression pattern
                    pattern = r'{"userInfo":{(.*?)}}'

                    # match the pattern to the input string
                    match = re.search(pattern, content)

                    # extract the data variable from the match object
                    if match:
                        # data = match
                        data = match.group(1)
                        # print(data) # temp
                        note = data
                        
                        # fulladdress = data["userInfo"]["displayAddress"]    # TypeError: string indices must be integers
                        # fullname = data["userInfo"]["displayName"]   
                        # lastname = data["userInfo"]["familyName"]   
                        # firstname = data["userInfo"]["givenName"]                           
                        
        
        if ':' in note:
            fullname = titleurl
            print(url, titleurl) 
            write_ossint(user, '9 - paypal', fullname, url, '', user, '', '', '', fulladdress
                , city, '', '', country, note, '', '', '', '', '', lastname, firstname, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        


def phonecarrier():# testuser=    210-316-9435 +919876543210  #beta
    print('\n\t<<<<< Checking for phone carrier >>>>>')
    for phone in phones:    
        (country, city, zip) = ('', '', '')
        (Country, Region) = ('', '')
        # Parsing String to Phone number
        phoneNumber = phonenumbers.parse(phone)
        # phone = phoneNumber  
        # Getting carrier of a phone number
        Carrier = carrier.name_for_number(phoneNumber, 'en')
        
        # Getting region information
        Region = geocoder.description_for_number(phoneNumber, 'en')
        country = Region  
        # Printing the carrier and region of a phone number
        print(Carrier)
        print(Region)
        if phoneNumber != '':
        # if len(phone) > 2:
            # print('hello world' , len(phoneNumber) ) # temp
            write_ossint(phoneNumber, Carrier, '', '', '', '', phoneNumber, '', '', ''
                , city, '', '', Region, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')


def pinterest():    # testuser=    kevinrose     # add city
    print('\n\t<<<<< Checking pinterest against a list of users >>>>>')
    for user in users:    
        (country, email, fullname,lastname,firstname) = ('', '', '','','')
        (success, note, photo, website, city, otherurls) = ('','','','','', '')
        (content, referer, osurl, titleurl, pagestatus) = ('', '', '','','')
        url = ('https://www.pinterest.com/%s/' %(user))
        otherurls = ('https://pinterest.com/search/users/?q=%s' %(user))

        
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
           
            fullname = titleurl
            fullname = fullname.split(' (')[0]

            if ' ' in FullName:
                fullname2 = fullname.split(" ")
                firstName = fullname2[0]
                lastName = fullname2[1]
            # success = 1    
        except:
            pass

        if 'Success' in pagestatus:
            for eachline in content.split("\n"):
                if eachline == "": pass                                             # skip blank lines
                else:
                    if 'pinterestapp:about' in eachline and 'rebuildStoreOnClient' not in eachline:
                        eachline = eachline.split('\"')
                        note = eachline[1]

                    # elif "title\>" in eachline and "\(" in eachline:
                        # fullname = eachline # temp
                        # print("blah" , fullname) # temp
            if note != '':
                write_ossint(user, '4 - pinterest', fullname, url, '', user, '', '', email, ''
                    , city, '', '', country, note, '', '', '', '', '', lastname, firstname, '', '', otherurls, '', '', '', '', '', '', '', '', '', '', '', '', '', '', pagestatus)            
                print(g + url + y + '\t', fullname , note, o)
                
                
def plaxoemail():    # testEmail= craig@craigslist.org#
    print(y + '\n\t<<<<< Checking plaxo against a list of ' + b + 'emails' + y + ' >>>>>' + o)
    for email in emails:
        url = ('http://www.plaxo.com/signup?t=ajax&avail=true&email=%s' %(email))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        if ('Claimed') in content: 
        # if ('Claimed') in str(response): 
            write_ossint(email, '7 - plaxo.com (email exists)', '', url, '', '', '', '', email, ''
                , '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')

            print(g + Email + '\t' + Url + o)
        # else:
            # print(r + Email + '\t' + Url + o)
            
def print_logo():
    clear = "\x1b[0m"
    colors = [36, 32, 34, 35, 31, 37]

    x = """
 ___    _            _   _ _         _   _             _   
|_ _|__| | ___ _ __ | |_(_) |_ _   _| | | |_   _ _ __ | |_ 
 | |/ _` |/ _ \ '_ \| __| | __| | | | |_| | | | | '_ \| __|
 | | (_| |  __/ | | | |_| | |_| |_| |  _  | |_| | | | | |_ 
|___\__,_|\___|_| |_|\__|_|\__|\__, |_| |_|\__,_|_| |_|\__|
                               |___/                       

  """
    for N, line in enumerate(x.split("\n")):
        sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
        time.sleep(0.05)

def public():    # testuser=    kevinrose
    print('\n\t<<<<< Checking public against a list of users >>>>>')
    for user in users:    
        (country, email, fullname,lastname,firstname) = ('', '', '','','')
        (success, note, photo, website, city, otherurls) = ('','','','','', '')
        (content) = ('')
        url = ('https://public.com/@%s' %(user))
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)


            # success = 1    
        except:
            pass

        if 'Success' in pagestatus:
            for eachline in content.split("\n"):
                if eachline == "": pass                                             # skip blank lines
                elif "og:title" in eachline:
                    fullname = eachline.strip().split("\"")[1]
                    fullname = fullname.split(" (")[0]
                    if ' ' in fullname:

                        fullname2 = fullname.split(" ")
                        firstname = fullname2[0]
                        lastname = fullname2[1]
              
            if note != 'true':
                write_ossint(user, '4 - public', fullname, url, '', user, '', '', email, ''
                    , city, '', '', country, note, '', '', '', '', '', lastname, firstname, '', '', otherurls, '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, '')            
                print(g + url + y + '\t', fullname , note, o)
 
def poshmark():    # testuser=    kevinrose
    print('\n\t<<<<< Checking poshmark against a list of users >>>>>')
    for user in users:    
        (country, email, fullname,lastname,firstname) = ('', '', '','','')
        (success, note, photo, website, city, otherurls) = ('','','','','', '')
        (content) = ('')
        url = ('https://poshmark.com/closet/%s' %(user))
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)


            # success = 1    
        except:
            pass

        if 'Success' in pagestatus:
            for eachline in content.split("\n"):
                if eachline == "": pass                                             # skip blank lines
                elif "og:title" in eachline:
                    fullname = eachline.strip().split("\"")[1].replace('\'s Closet', '')
                    firstname = fullname

            if note != 'true':
                write_ossint(user, '7 - poshmark', fullname, url, '', user, '', '', email, ''
                    , city, '', '', country, note, '', '', '', '', '', lastname, firstname, '', '', otherurls, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')            
                print(g + url + y + '\t', fullname , note, o)
                
def read_url():
    global row  # The magic to pass row globally
    style = workbook.add_format()
    color = 'white'

    inputfile = open(filename)
    # Create dnsdomain
    for eachline in inputfile:
        
        
        (query, ranking, fullname, url, email , user) = ('', '', '', '', '', '')
        (phone, ip, entity, fulladdress, city, state) = ('', '', '', '', '', '')
        (zip, country, note, aka, dob, gender) = ('', '', '', '', '', '')
        (info, misc, lastname, firstname, middlename, friend) = ('', '', '', '', '', '')
        (otherurls, otherphones, otheremails, case, sosfilenumber, president) = ('', '', '', '', '', '')
        (sosagent, managers, dnsdomain, dstip, srcip  ) = ('', '', '', '', '')
        (content, referer, osurl, titleurl, pagestatus) = ('', '', '', '', '')
        
        (color) = 'white'
        style.set_bg_color('white')  # test

        eachline = eachline + "," * 72
        eachline = eachline.split(',')  # splits by comas
        note = (eachline[0].strip())

        # Regex data type
        if bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", note)):  # regex email    
            logsource = 'IOC-Email'

        elif re.search(regex_host, note):  # regex_host (Finds url and dnsdomain) # False positives for emails    # todo
            url = note
            if url.lower().startswith('http'):
                logsource = 'IOC-url'
            else:
                logsource = 'IOC-dnsdomain'
            url = url.rstrip('/')
            dnsdomain = url.lower()
            dnsdomain = dnsdomain.replace("https://", "")
            dnsdomain = dnsdomain.replace("http://", "")
            dnsdomain = dnsdomain.split('/')[0]
            notes2 = dnsdomain.split('.')[-1]

        elif re.search(regex_ipv4, note):  # regex_ipv4
            (srcip, dstip) = (note, note)
            logsource = 'IOC-IP'
        elif re.search(regex_md5, note):  # regex_md5
            logsource = 'IOC-Hash-Md5'
        elif re.search(regex_sha256, note):  # regex_sha256
            logsource = 'IOC-Hash-Sha256'
        elif re.search(regex_sha1, note):  # regex_sha1
            logsource = 'IOC-Hash-Sha1'
        elif re.search(regex_sha512, note):  # regex_sha512
            logsource = 'IOC-Hash-Sha512'

        # Read url,dnsdomain or dstip
        if url != '':
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        elif dnsdomain != '':
            (content, referer, osurl, titleurl, pagestatus) = request(dnsdomain)
        elif dstip != '':
            (content, referer, osurl, titleurl, pagestatus) = request(dstip)
        # copy whole page

        # color
        # if 'Fail' in pagestatus:  #
            # format_function(bg_color='red')
        # elif 'yahoo' in url:  
            # format_function(bg_color='orange')
        # elif 'google' in url:  #
            # format_function(bg_color='green')
            
            
        else:
            format_function(bg_color='white')

        # Write OSSINT excel
        write_ossint(query, ranking, fullname, url, email , user, phone, ip, entity, 
            fulladdress, city, state, zip, country, note, aka, dob, gender, info, 
            misc, lastname, firstname, middlename, friend, otherurls, otherphones, 
            otheremails, case, sosfilenumber, president, sosagent, managers, 
            dnsdomain, dstip, srcip, content, referer, osurl,
            titleurl, pagestatus)

        print('%s%s    %s%s    %s    %s%s    %s' % (b, note, g, osurl, r, titleurl, o, pagestatus))


def redirect_detect():
    print(y, '\n\t<<<<< website redirect detector >>>>>'    , o)    

    for website in websites:    
        (final_url, dnsdomain, referer, osurl, titleurl, pagestatus) = ('', '', '', '', '', '')
        url = website
        url = url.replace("http://", "https://")
        if "http" not in url.lower():
            url = ('https://%s' %(url))
            
        referer = url.lower().strip()
        try:
            response = requests.get(url)

            final_url = response.url

            # print(url, " redirects to ", final_url)        

        except TypeError as error:
            # print(error)
            pass
        
        dnsdomain = url.lower()
        dnsdomain = dnsdomain.replace("https://", "")
        dnsdomain = dnsdomain.replace("http://", "")
        dnsdomain = dnsdomain.split('/')[0]

        ip = ip_address(dnsdomain)
        
        if dnsdomain not in final_url:
            print(url, " redirects to ", final_url)    
            write_ossint(url, '7 - redirect ', '', final_url, '', '', '', ip, '', ''
                , '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', dnsdomain, '', '', '', referer, osurl, titleurl, pagestatus)


def request(url):
    (content, referer, osurl, titleurl, pagestatus) = ('','','','','')
    (string) = ('')
    fake_referer = 'https://www.google.com/'
    headers = {'Referer': fake_referer}
    url = url.replace("http://", "https://")     # test
    # if "http" not in url.lower():
        # url = ('https://%s' %(url))
            
    # if url.lower().startswith('http'):
        # page = requests.get(url)
        
        
    # else:
        # page  = requests.get("http://" +url)

    page  = requests.get(url, headers=headers)
    pagestatus  = page.status_code
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.prettify()
    try:
        osurl = page.headers['Server']
    except:pass
    
    try:
        titleurl = soup.title.string
    except:pass
    
    # try:    
        # page  = requests.get(url, headers=headers)
        # pagestatus  = page.status_code
        # soup = BeautifulSoup(page.content, 'html.parser')
        # content = soup.prettify()
        # osurl = page.headers['Server']
        # titleurl = soup.title.string
    # except:
        # pass
    
#pagestatus
    
    if str(pagestatus).startswith('2') :    
        pagestatus = ('Success - %s' %(pagestatus))
    elif str(pagestatus).startswith('3') :    
        pagestatus = ('Redirect - %s' %(pagestatus))
    elif str(pagestatus).startswith('4') :    
        pagestatus = ('Fail - %s' %(pagestatus))
    elif str(pagestatus).startswith('5') :    
        pagestatus = ('Fail - %s' %(pagestatus))
    elif str(pagestatus).startswith('1') :    
        pagestatus = ('Info - %s' %(pagestatus))
    try:
        pagestatus = pagestatus.strip()
    except Exception as e:
        print(f"Error striping pagestatus: {str(e)}")
# titleurl

    try:
        title_tag = content.find('title')
        if title_tag is not None:
            title = title_tag.text.strip()
            # The full name is often included in parentheses after the username
            # Example: "Tom Anderson (myspacetom)"
            # We'll split the title at the first occurrence of '(' to extract the full name
            parts = title.split(' (', 1)
            if len(parts) > 1:
                titleurl = parts[0]
    except Exception as e:
        # print(f"Error parsing title: {str(e)}")
        pass

    if titleurl !="":
        try:
            meta_tags = content.find_all('meta')
            for tag in meta_tags:
                # print('tag = %s' %(tag))    
                if tag.get('property') == 'og:title':
                    titleurl = tag.get('content')
                    titleurl =  title.split(' (')[0]
        except Exception as e:
            # print(f"Error parsing metadata: {str(e)}")
            # print('this is an error')
            pass

    try:
        titleurl = str(titleurl)    #test
        titleurl = (titleurl.encode('utf8'))    # 'ascii' codec can't decode byte
        titleurl = (titleurl.decode('utf8'))    # get rid of bytes b''
    except TypeError as error:
        print(error)
        titleurl = ''


    titleurl = titleurl.strip()
    content = content.strip()
    
    return (content, referer, osurl, titleurl, pagestatus)    

def request_url(url):
    
    fake_referer = 'https://www.google.com/'
    headers = {'Referer': fake_referer}

    
    (content, referer, osurl, titleurl, pagestatus)= ('blank', '', '', '', '')
    (response) = ('')
    
    if url.lower().startswith('http'):
        blah = ''
    else:
        url = ("https://" +url)

    try:
        response = requests.get(url, verify=False, headers=headers)        
        response.raise_for_status()
        pagestatus  = response.status_code
        content = response.content.decode()
        content = BeautifulSoup(content, 'html.parser')
        


    except requests.exceptions.RequestException as e:
        # print(f"Could not fetch URL {url}: {str(e)}")
        # raise requests.exceptions.RequestException(str(e))
        (pagestatus) = ('Fail')

# osurl
    try:
        osurl = response.headers['Server']
    except:
    # except KeyError:
        pass

# titleurl
    try:
        titleurl = titleurl_get(content)
        # titleurl = titleurl_og(content)
    except KeyError:
        titleurl = ''


#pagestatus
    
    if str(pagestatus).startswith('2') :    
        pagestatus = ('Success - %s' %(pagestatus))
    elif str(pagestatus).startswith('3') :    
        pagestatus = ('Redirect - %s' %(pagestatus))
    elif str(pagestatus).startswith('4') :    
        pagestatus = ('Fail - %s' %(pagestatus))
    elif str(pagestatus).startswith('5') :    
        pagestatus = ('Fail - %s' %(pagestatus))
    elif str(pagestatus).startswith('1') :    
        pagestatus = ('Info - %s' %(pagestatus))

    pagestatus = pagestatus.strip()    

    return (content, referer, osurl, titleurl, pagestatus)

def resolverRS():# testIP= 77.15.67.232
    print(y + '\n\t<<<<< Checking resolverRS against a list of ' + b + 'ip' + y + ' >>>>>' + o)
    
    for ip in ips:
        (country, city, zip, case, note, state) = ('', '', '', '', '', '')
        (misc, info) = ('', '')
        
        url = ('https://resolve.rs/ip/geolocation.html?ip=%s' %(ip))
        (content, referer, osurl, titleurl, pagestatus) = request(url)

        for eachline in content.split("\n"):
            if "403 ERROR" in eachline:
                pagestatus = '403 Error'
                content = ''
            # elif "Found 0 results for your query" in eachline:
                # print("not found")  # temp
                # url = ('')
            # elif "td id=\"maxmind" in eachline :   # and zip != ''
                # note = eachline
                # print(note) # temp


            elif "\"code\": \"" in eachline :   # and zip != ''
                zip = eachline.split("\"")[3]
            elif "\"en\": \"" in eachline :   # city
                print('')
                if city == '':
                    city = eachline.split("\"")[3]
                elif misc == '' and city != '': # continent
                    misc = eachline.split("\"")[3]

                elif misc != '' and country == '' and city != '': # country
                    country = eachline.split("\"")[3]
                elif info == '' and misc != '' and country != '' and city != '':    # registered country
                    info = eachline.split("\"")[3]
                elif state == '' and info != '' and misc != '' and country != '' and city != '':    # state
                    state = eachline.split("\"")[3]
            elif "COMCAST" in eachline :   # isp  >ASN</a>
                note = 'COMCAST'
                # print(note) # temp


        # pagestatus = ''                
        if url != '':
            print(url, ip) 
            write_ossint(ip, '6 - resolve.rs', '', url, '', '', '', ip, '', ''
                , city, state, zip, country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', referer, '', titleurl, pagestatus)

def reversephonecheck():# testPhone= 708-372-8101
    print(y + '\n\t<<<<< Checking reversephonecheck against a list of ' + b + 'phone numbers' + y + ' >>>>>' + o)
    for phone in phones:
        (query) = (phone)
        (fulladdress, country, city, zip, case, note) = ('', '', '', '', '', '')
        (content, referer, osurl, titleurl, pagestatus)  = ('', '', '', '', '')
        (areacode, prefix, line, count, match, match2) = ('', '', '', 1, '', '')
        phone = phone.replace('(','').replace(')','-').replace(' ','')
        print(phone)
        if phone.startswith('1-'):
            phone =phone.replace('1-','')
        elif phone.startswith('1'):
            phone =phone.lstrip('1')

        if len(phone) != 10:
            return "Invalid phone number"
        elif '-' not in phone:
            phone = (phone[:3] + "-" + phone[3:6] + "-" + phone[6:])
            
        (line2) = ('')
        # print('phone = >%s<' %(phone))     #temp   
        if "-" in phone:
            phone2 = phone.split("-")
            areacode = phone2[0]
            prefix = phone2[1]
            try:
                line = phone2[2]
                line2 = line
                line = line[:2]
                
            except:
                pass
        url = ('https://www.reversephonecheck.com/1-%s/%s/%s/#%s' %(areacode, prefix, line, phone.replace('-', ''))) 

        (content, referer, osurl, titleurl, pagestatus) = request(url) 
        match = ("%s - %s" %(prefix, line2))
        # match2 = match.replace(' - ','')
        # match2 = ('%s%s' %(areacode, match2))
        
        # print('match2 = ', match2)  # temp
        # print('match = %s' %(match))    # temp
        for eachline in content.split("\n"):
            if match in eachline:

                pagestatus = 'research'
                # print('eachline = %s' %(eachline))
                count += 1
            # if match2 in eachline and 'ownersAddresses' in eachline:
                # note = ('%s %s' %(note, eachline))
                # print(note) # temp
                # fulladdress = eachline.split('owner:i,address:[\"')[0]   # ownersAddresses
                # fulladdress = eachline.split('ownersAddresses')[1]   # ownersAddresses

        if pagestatus == 'research' and count == 2:
            print(url) 
            write_ossint(query, '3 - reversephonecheck', '', url, '', '', phone, '', '', fulladdress
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', pagestatus)
        else:
            write_ossint(query, '9 - reversephonecheck', '', url, '', '', phone, '', '', fulladdress
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', pagestatus)
        

def robtex():
    print(y, '\n\t<<<<< robtex dns lookup >>>>>'    , o)    

    for website in websites:    
        print(website)
        (final_url, dnsdomain, referer, osurl, titleurl, pagestatus) = ('', '', '', '', '', '')
        (otherurl, ip) = ('', '')
        url = website
        url = url.replace("http://", "https://")
        if "http" not in url.lower():
            url = ('https://%s' %(url))
        
        dnsdomain = url.lower()
        dnsdomain = dnsdomain.replace("https://", "")
        dnsdomain = dnsdomain.replace("http://", "")
        dnsdomain = dnsdomain.split('/')[0]

        ip = ip_address(dnsdomain)

        otherurl = url  

        url = ('https://www.robtex.com/dns-lookup/%s#quick' %(dnsdomain))
        
        if 1==1:
        # if dnsdomain not in final_url:

            write_ossint(url, '9 - robtexDNS-lookup ', '', url, '', '', '', ip, '', ''
                , '', '', '', '', '', '', '', '', '', '', '', '', '', '', otherurl, '', '', '', '', '', '', '', dnsdomain, '', '', '', '', '', '', '')
   

def samples():
    print('''    
Alain_THIERRY
anh_usa
frizz925
gurkha_love
Hmei7
itdoesnthavetohappen
JLight29
kevinrose
kevinwagner
kobegal
luckyjames844
maverick3819
merz356
MR-JEFF
N3tAtt4ck3r
Pattycakes98
ryanlwatkins
thekevinrose
williger
zazenergy
nullcrew
realDonaldTrump
Their1sn0freakingwaythisisreal12JT4321
        
77.15.67.232
92.20.236.78
255.255.255.255

annemconnor@yahoo.com
kandyem@yahoo.com
kevinrose@gmail.com
craig@craigslist.org
ceo@zappos.com
lnd_whitaker@yahoo.com
gsmstocks@gmail.com
lydianorman1@hotmail.com
soniraj388@gmail.com
tanderson09@gmail.com
tin_max87@yahoo.com
Their1sn0freakingwaythisisreal12344321@fakedomain.com

385-347-1531
999-999-9999
'''
)    

def sherlock():    # testuser=    kevinrose
    print('\n\t<<<<< Manually check sherlock against a list of users >>>>>')
    for user in users:    
        note = ('cd C:\Forensics\scripts\python\git-repo\sherlock && python sherlock %s' %(user)) 

        if 1==1:

            write_ossint(user, '8 - manual', '', '', '', user, '', '', '', ''
                , '', '', '', '', note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'research')


def snapchat(): # testuser = kevinrose

    print('\n\t<<<<< Checking snapchat against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus, content) = ('', '', '', '', 'research', '')
        user = user.rstrip()
        url = ('https://www.snapchat.com/add/%s?' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)

        for eachline in content.split("\n"):

            if "og:title" in eachline:
                fullname = eachline.strip().split("\"")[1].replace(' on Snapchat','')


        if 'name=\"description' in content:
            write_ossint(user, '6 - snapchat', fullname, url, '', user, '', '', '', ''
            , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', pagestatus)        
            print(url)        

        # elif 'name=\"description' in content and 'Please provide your Snapchat username if you have one' in content:
            # write_ossint(user, '8 - snapchat', fullname, url, '', user, '', '', '', ''
            # , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', titleurl, pagestatus)        
            # print(url)        



def spotify(): # testuser = kevinrose

    print('\n\t<<<<< Checking spotify against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        user = user.rstrip()
        url = ('https://open.spotify.com/user/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        if '404' not in pagestatus:
            fullname = titleurl
            print(url, titleurl) 
            write_ossint(user, '6 - spotify', '', url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', pagestatus)        

def spydialer():# testPhone= 708-372-8101
    print('\n\t<<<<< Checking spydialer against a list of users >>>>>')

    for phone in phones:
        (country, city, zip, case, note) = ('', '', '', '', '')
        (content, referer, osurl, titleurl, pagestatus)  = ('', '', '', '', '')
        phone = phone.replace('(','').replace(')','').replace(' ','')
        # print('phone = >%s<' %(phone))     #temp   
        url = ('https://www.spydialer.com')

        pagestatus = 'research'        
        write_ossint(phone, '3 - spydialer', '', url, '', '', phone, '', '', ''
                , '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', pagestatus)

def thatsthememail():# testEmail= smooth8101@yahoo.com   
    print(y + '\n\t<<<<< Checking thatsthem against a list of ' + b + 'emails' + y + ' >>>>>' + o)
    
    for email in emails:
        (country, city, zip, case, note) = ('', '', '', '', '')
        
        url = ('https://thatsthem.com/email/%s' %(email))
        (content, referer, osurl, titleurl, pagestatus) = request(url)

        for eachline in content.split("\n"):
            if "Found 0 results for your query" in eachline and case == '':
                print("not found")  # temp
                url = ('')
            # elif "schema.org" in eachline:
                # print('oooh doggy') # temp
                # note = eachline
                
        pagestatus = ''                
        if url != '':
        # if ('%') not in url: 
            print(url, email) 
            write_ossint(email, '9 - thatsthem', '', url, email, '', '', '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', referer, '', titleurl, pagestatus)

def thatsthemip():# testIP= 8.8.8.8
    print(y + '\n\t<<<<< Checking thatsthem against a list of ' + b + 'ip' + y + ' >>>>>' + o)
    
    for ip in ips:
        (country, city, zip, case, note, state) = ('', '', '', '', '', '')
        
        url = ('https://thatsthem.com/ip/%s' %(ip))
        (content, referer, osurl, titleurl, pagestatus) = request(url)

        for eachline in content.split("\n"):
            if "located in " in eachline:
                state = eachline
                note = eachline

            elif "403 ERROR" in eachline:
                pagestatus = '403 Error'
                content = ''
            elif "Found 0 results for your query" in eachline:
                print("not found")  # temp
                url = ('')
        # pagestatus = ''                
        if url != '':
            print(url, ip) 
            write_ossint(ip, '6 - thatsthem', '', url, '', '', '', ip, '', ''
                , city, state, '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, referer, '', titleurl, pagestatus)


def thatsthemphone():# testPhone= 708-372-8101  
    print(y + '\n\t<<<<< Checking thatsthem against a list of ' + b + 'phone numbers' + y + ' >>>>>' + o)
    
    for phone in phones:
        (country, city, zip, case, note) = ('', '', '', '', '')
        phone = phone.replace('(','').replace(')','-')
   
        url = ('https://thatsthem.com/phone/%s' %(phone))    # https://thatsthem.com/reverse-phone-lookup
        (content, referer, osurl, titleurl, pagestatus) = request(url)

        if "Found 0 results for your query" in content or "The request could not be satisfied" in content:
            url = ('')

        for eachline in content.split("\n"):
            if "Found 0 results for your query" in eachline and case == '':
                print("not found")  # temp
                url = ('')
            # elif "schema.org" in eachline:
                # print('oooh doggy') # temp
                # note = eachline
        pagestatus = ''        
                
        if url != '':
        # if ('%') not in url: 
            print(url, phone) 
            write_ossint(phone, '6 - thatsthem', '', url, '', '', phone, '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', pagestatus)

def telegram(): # testuser = kevinrose

    print('\n\t<<<<< Checking telegram against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus, content) = ('', '', '', '', 'research', '')
        user = user.rstrip()
        url = ('https://t.me/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        for eachline in content.split("\n"):
            if "og:title" in eachline:
                fullname = eachline.strip().split("\"")[1]

        if 'Telegram' not in fullname:
            print(url, titleurl) 
            write_ossint(user, '7 - telegram', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', titleurl, pagestatus)        


def tiktok(): # testuser = kevinrose

    print('\n\t<<<<< Checking tiktok against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus, content) = ('', '', '', '', 'research', '')
        user = user.rstrip()
        url = ('https://tiktok.com/@%s?' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)

        if 'uccess' in pagestatus:
            fullname = titleurl
            fullname = fullname.split(' (')[0]
            if fullname == user:
                fullname = ''
            print(url, fullname) 
            write_ossint(user, '4 - tiktok', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        

def tinder():    # testuser=    john
    print('\n\t<<<<< Checking tinder against a list of users >>>>>')
    for user in users:    
        url = ('https://tinder.com/@%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = ('','','','','')
        (fullname, dob, info, misc, note) = ('', '', '', '', '')
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
            
            
            
            content = content.strip()
            titleurl = titleurl.strip()
            for eachline in content.split("\n"):
                if "@context" in eachline:
                    content = eachline.strip()
                elif 'og:title' in eachline and 'content=\"' in eachline:
                    fullname = eachline.split('\"')[1].split(' (')[0]
                elif 'schools\"' in eachline:
                # elif 'schools\":\[{\"name' in eachline:
                    data = json.loads(eachline)
                    note = data["schools"][0]["name"]
                    # Extract the description value and print it
                    # note = data['description']
                    misc = eachline
                    
                    dob= data["webProfile"]["user"]["birth_date"]
        except:
            pass
            
        # time.sleep(1) # will sleep for 1 seconds
        if 'alternate' in content:
            
        
            write_ossint(user, '7 - tinder.com', fullname, url, '', user, '', '', '', ''
                , '', '', '', '', note, '', '', '', '', '', '', '', '', '', '', '', '', '', dob, '', info, misc, '', '', '', '', '', '', titleurl, pagestatus)
            print(g + url + o)    



def titles():    # testsite= google.com
    from subprocess import call, Popen, PIPE
    print(y, '\n\t<<<<< Titles grab against a list of Website\'s >>>>>'    , o)    

    for website in websites:    
        (content, referer, osurl, titleurl, pagestatus) = ('', '', '', '', '')
        (ip, note) = ('', '')
        
        url = website

        fake_referer = 'https://www.google.com/'
        headers = {'Referer': fake_referer}
        url = url.replace("http://", "https://")     # test
        if "http" not in url.lower():
            url = ('https://%s' %(url))

        url = url.replace("https://", "http://")

        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except TypeError as error:
            print(error)


        # try:    
            # page  = requests.get(url, headers=headers)
            # pagestatus  = page.status_code
            # soup = BeautifulSoup(page.content, 'html.parser')
            # content = soup.prettify()
            # osurl = page.headers['Server']
            # titleurl = soup.title.string
        # except:
            # pass
        
        # dnsdomain
        dnsdomain = url.lower()
        dnsdomain = dnsdomain.replace("https://", "")
        dnsdomain = dnsdomain.replace("http://", "")
        dnsdomain = dnsdomain.split('/')[0]
        
        # ip
        ip = ip_address(dnsdomain)
        
        print(y, website , pagestatus,  g, titleurl, o)
        write_ossint(url, '7 - website ', '', url, '', '', '', ip, '', ''
            , '', '', '', '', note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', dnsdomain, '', '', '', referer, osurl, titleurl, pagestatus)


def titleurl_get(content):

    titleurl = ''
    try:
        # soup = BeautifulSoup(html, 'html.parser')
        title_tag = content.find('title')
        if title_tag is not None:
            title = title_tag.text.strip()
            # The full name is often included in parentheses after the username
            # Example: "Tom Anderson (myspacetom)"
            # We'll split the title at the first occurrence of '(' to extract the full name
            parts = title.split(' (', 1)
            if len(parts) > 1:
                titleurl = parts[0]
    except Exception as e:
        # print(f"Error parsing title: {str(e)}")
        pass
    # print('titleurl = %s' %(titleurl)) # temp

    return titleurl

def titleurl_og(content):
    (titleurl) = ('')

    try:
        meta_tags = content.find_all('meta')
        for tag in meta_tags:
            # print('tag = %s' %(tag))    
            if tag.get('property') == 'og:title':
                titleurl = tag.get('content')
                titleurl =  title.split(' (')[0]
    except Exception as e:
        # print(f"Error parsing metadata: {str(e)}")
        # print('this is an error')
        pass
    return titleurl


def truthSocial(): # testuser = realdonaldtrump https://truthsocial.com/@realDonaldTrump

    print('\n\t<<<<< Checking truthsocial.com against a list of users >>>>>')
    print('\n\tThis one one takes a while')
    for user in users:    
        (city, country, note, fullname, titleurl, pagestatus) = ('', '', '', '', '', '')
        (info, ranking) = ('', '9 - truthsocial.com')
        user = user.rstrip()
        url = ('https://truthsocial.com/@%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        # print('trying %s' %(url))   # temp
        pagestatus = ''
        time.sleep(3) #will sleep for 3 seconds
        for eachline in content.split("  <"):
            if 'This resource could not be found' in eachline:
                pagestatus = '404'
            elif "og:title" in eachline:
                titleurl = eachline.strip().split("\"")[1]
                fullname = titleurl.split(" (")[0]
                pagestatus = '200'
                ranking = '9 - truthsocial.com'
                if titleurl == 'Truth Social':
                    pagestatus = '404'
                else:
                    pagestatus = '200'
                    ranking = '3 - truthsocial.com'
                # print(fullname) # temp
            elif "og:description" in eachline:
                note = eachline.strip().split("\"")[1]

        if '@' in titleurl: 
            print(url, fullname) 
            write_ossint(user, ranking, fullname, url, '', user, '', '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)  

        
def twitter():    # testuser=    kevinrose     # add info
    print('\n\t<<<<< Checking twitter against a list of users >>>>>')
    for user in users:    
        (fullname,lastname,firstname, email, city, country) = ('','','', '', '', '')
        url = ('https://twitter.com/%s' %(user))
        
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        # print(titleurl, url, pagestatus)  # temp
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
            # print(titleurl)  # temp
            titleurl = titleurl.replace(") on Twitter","")
            titleurl = titleurl.lower().replace(User.lower(),"")
            titleurl = titleurl.replace(" (","")
            fullname = titleurl
            fullname = fullname.replace(" account suspended","")
            fullname = fullname.replace("twitter /","")
            titleurl = titleurl.lower().replace(fullname.lower(),"")

            write_ossint(user, '5 - twitter.com', fullname, url, email, user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)
            print(g , url, '\t', y , fullname , '\t', titleurl , o)
        except:
            write_ossint(user, '9 - twitter.com', fullname, url, email, user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', titleurl, pagestatus)
            pass
            
def twitteremail(): # test Email=     craig@craigslist.org 
    print(y + '\n\t<<<<< Checking twitter against a list of emails >>>>>' + o)
    # {"valid":false,"msg":"Email has already been taken. An email can only be used on one Twitter account at a time.","color":"red","taken":true,"blank":false}
    for email in emails:
        url = ('https://twitter.com/users/email_available?email=%s' %(email))
        (country, city, zip) = ('', '', '')        
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)    # access denied cloudflare
        except socket.error as ex:
            print(ex)        
        if 'Email has already been taken' in content:
            write_ossint(email, '5 - twitter.com', '', url, email, '', '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', '', '')
            print(g + email + o)

def validnumber():# testPhone= 7083703020
    print(y + '\n\t<<<<< Checking validnumber against a list of ' + b + 'phone numbers' + y + ' >>>>>' + o)
    # https://validnumber.com/phone-number/3124377966/
    for phone in phones:
        (country, city, state, zip, case, note) = ('', '', '', '', '', '')
        (content, referer, osurl, titleurl, pagestatus)  = ('', '', '', '', '')
        (query) = (phone)
        phone = phone.replace('(','').replace(')','').replace(' ','')
        if phone.startswith('1-'):
            phone =phone.replace('1-','')
        elif phone.startswith('1'):
            phone =phone.lstrip('1')
        
        
        # print('phone = >%s<' %(phone))     #temp   
        url = ('https://validnumber.com/phone-number/%s/' %(phone.replace("-", "")))
        
        (content, referer, osurl, titleurl, pagestatus) = request(url)    # protected by cloudflare
        pagestatus = ''
        for eachline in content.split("\n"):
            if "No name associated with this number" in eachline and case == '':
                print("not found")  # temp
                url = ('')
            elif "Find out who owns" in eachline:
                if 'This device is registered in ' in eachline:
                    note = eachline.split('\"')[1]
                    note = note.split('Free owner details for')[0]
                    city = eachline.split("This device is registered in ")[1].split("Free owner details")[0]
                    
                    state = city.split(',')[1]
                    city = city.split(',')[0]

            # descpattern = r'<meta name="description" content="(.+?)">'
            # match = re.search(descpattern, eachline)
            # if match:
                # note = match.group(1)
                # print(match.group(1))
          
          
        if city != '':        
                print(url) 
                write_ossint(query, '5 - validnumber', '', url, '', '', phone, '', '', ''
                    , city, state, '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', referer, '', titleurl, '')


def venmo(): # testuser = kevinrose

    print('\n\t<<<<< Checking venmo against a list of users >>>>>')
    for user in users:    
        (Success, fullname, lastname, firstname, case, gender) = ('','','','','','')
        (photo, country, website, email, language, username) = ('','','','','','')
        (city, content) = ('', '')
        (content, referer, osurl, titleurl, pagestatus) = ('','','','','')
        user = user.rstrip()
        url = ('https://account.venmo.com/u/%s' %(user))

        (content, referer, osurl, titleurl, pagestatus) = request(url)
        
        # try:
            # (content, referer, osurl, titleurl, pagestatus) = request(url)
        # except:
            # pass
        # if 1==1:    
        if 'Sign in to pay this person' in content:
        # if 'the page you requested does not exist' not in content:
            print('bobs your uncle')    # temp
            fullname = titleurl
            fullname = fullname.split(" (")[0]
            print(url, fullname) 
            write_ossint(user, '3 - venmo', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)

        elif 'the page you requested does not exist' not in content:
            write_ossint(user, '9 - venmo', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', titleurl, pagestatus)


def viewdnsdomain():
    print(y, '\n\t<<<<< viewdns lookup >>>>>'    , o)    

    for website in websites:    
        print(website)
        (final_url, dnsdomain, referer, osurl, titleurl, pagestatus) = ('', '', '', '', '', '')
        (content, referer, osurl, titleurl, pagestatus) = ('', '', '', '', '')
        (otherurl, ip) = ('', '')
        url = website
        url = url.replace("http://", "https://")
        if "http" not in url.lower():
            url = ('https://%s' %(url))
        
        dnsdomain = url.lower()
        dnsdomain = dnsdomain.replace("https://", "")
        dnsdomain = dnsdomain.replace("http://", "")
        dnsdomain = dnsdomain.split('/')[0]

        ip = ip_address(dnsdomain)

        otherurl = url  

        url = ('https://viewdns.info/whois/?domain=%s' %(dnsdomain))
        # (content, referer, osurl, titleurl, pagestatus) = request(url)
        # time.sleep(10) #will sleep for 10 seconds
        if 1==1:
        # if dnsdomain not in final_url:

            write_ossint(url, '9 - viewdns ', '', url, '', '', '', ip, '', ''
                , '', '', '', '', '', '', '', '', '', '', '', '', '', '', otherurl, '', '', '', '', '', '', '', dnsdomain, '', '', '', content, '', titleurl, pagestatus)
   


def whatismyip():    # testuser= 77.15.67.232  
    print('\n\t<<<<< Checking whatismyipaddress.com against a list of IPs >>>>>')
    for ip in ips:
        (country, city, state, zip, pagestatus, title) = ('', '', '', '', '', '')
        url = ('https://whatismyipaddress.com/ip/%s' %(ip))
        
        # (content, referer, osurl, titleurl, pagestatus) = request(url)
        (content, titleurl) = ('', '')

        # for content in content.split("meta property"):
            # print('hello world') # temp
            # print(content)  # temp
            # if "og:description" in content:
                # print(content) # temp
                # info = content.strip().split("\"")[1]
                # print(info) # temp
            # elif "og:title" in content:
                # titleurl = content.strip().split("\"")[1]
                # print(titleurl) # temp

        # time.sleep(7) #will sleep for 30 seconds
        write_ossint(ip, '9 - whatismyipaddress', '', url, '', '', '', ip, '', ''
        , city, state, zip, country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, titleurl, pagestatus)

def whatsmyname():    # testuser=    kevinrose
    print('\n\t<<<<< Checking whatsmyname against a list of users >>>>>')
    for user in users:    
        url = ('https://whatsmyname.app/')
        
        note = ('cd C:\Forensics\scripts\python\git-repo\WhatsMyName && python web_accounts_list_checker.py -u %s -of C:\Forensics\scripts\python\output_%s.txt' %(user, user)) 
            
        # time.sleep(1) # will sleep for 1 seconds
        if 1==1:

            write_ossint(user, '9 - manual', '', url, '', user, '', '', '', ''
                , '', '', '', '', note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'research')


def whitepagesphone():# testuser=    210-316-9435
    print('\n\t<<<<< Checking whitepages against a list of users >>>>>')
    for phone in phones:    
        (country, city, zip) = ('', '', '')
        (titleurl) = ('')
        # url = ('http://www.whitepages.com/search/ReversePhone?full_phone=%s' %(phone))
        url = ('https://www.whitepages.com/phone/1-%s' %(phone))

        # (content, referer, osurl, titleurl, pagestatus) = request(url)    # access denied cloudflare

        write_ossint(phone, '9 - whitepages', '', url, '', '', phone, '', '', ''
            , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, '')
    
def whocalld():# testPhone= 708-372-8101 DROP THE LEADING 1
    print(y + '\n\t<<<<< Checking whocalld against a list of ' + b + 'phone numbers' + y + ' >>>>>' + o)
    # https://whocalld.com/+17083728101
    for phone in phones:
        (country, city, state, zip, case, note) = ('', '', '', '', '', '')
        (fullname, content, referer, osurl, titleurl, pagestatus)  = ('', '', '', '', '', '')
        phone = phone.replace('(','').replace(')','').replace(' ','')
        
        if phone.startswith('1'):
            phone = phone.replace('1','')
        
        # print('phone = >%s<' %(phone))     #temp   
        url = ('https://whocalld.com/+1%s' %(phone.replace("-", "")))
        
        (content, referer, osurl, titleurl, pagestatus) = request(url)    # protected by cloudflare

        for eachline in content.split("\n"):
            if "Not found" in eachline and case == '':
                # print("%s Not found" %(phone))  # temp
                url = ('')
            elif "This seems to be" in eachline:
                if ' in ' in eachline:
                    note = eachline.replace(". </p>",'').replace("<p>",'').strip().replace("This",phone)
                    city = eachline.split(" in ")[1].replace(". </p>",'').replace("<p>",'').strip()
                    if ", " in city:
                        state = city.split(", ")[1].replace(".",'')
                        city = city.split(", ")[0]
                    note = ("According to %s %s" %(url, note))
            elif "The name of this caller seemed to be " in eachline:
                note = eachline
                fullname = eachline.replace("The name of this caller seemed to be ",'').split(",")[0].strip()
                if ' in ' in eachline:
                    note = eachline.replace(". </p>",'').replace("<p>",'').strip().replace("This",phone)
                    city = eachline.split(" in ")[2].replace(". </p>",'').replace("<p>",'').strip()
                    if ", " in city:
                        state = city.split(", ")[1].replace(".",'')
                        city = city.split(", ")[0]



         
        pagestatus = ''        
                
        if url != '':
            print(url, fullname) 
            write_ossint(phone, '4 - whocalld', fullname, url, '', '', phone, '', '', ''
                , city, state, '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', referer, '', titleurl, pagestatus)

def whoisip():    # testuser=    77.15.67.232   only gets 403 Forbidden
    from subprocess import call, Popen, PIPE
    print('\n\t<<<<< Checking whois against a list of IP\'s >>>>>')

    for ip in ips:    
        (city, business, country, zip, state) = ('', '', '', '', '')
        (content, titleurl, pagestatus) = ('', '', '')
        (email, phone, fullname, entity, fulladdress) = ('', '', '', '', '') 
        url = ('https://www.ip-adress.com/whois/%s' %(ip))
        if sys.platform == 'win32' or sys.platform == 'win64':    
            (content, referer, osurl, titleurl, pagestatus) = request(url)
            if '403 Forbidden' in content:
                pagestatus = '403 Forbidden'
                content = ''
            for eachline in content.split("\n"):
                
                if "www.ip-adress.com/legal-notice" in eachline:
                    for eachline in content.split("<tr><th>"):
                        if "Country<td>" in eachline:
                            country = eachline.strip().split("Country<td>")[1]
                        elif "City<td>" in eachline:
                            city = eachline.strip().split("City<td>")[1]
                        elif "ISP</abbr><td>" in eachline:
                            business = eachline.strip().split("ISP</abbr><td>")[1]
                        elif "Postal Code<td>" in eachline:
                            zip = eachline.strip().split("Postal Code<td>")[1]
                        elif "State<td>" in eachline:
                            state = eachline.strip().split("State<td>")[1]
               
                elif "<tr><th>Country</th><td>" in eachline:
                    country = eachline.strip().split("<tr><th>Country</th><td>")[1]
                    country = country.split("<")[0]
                elif "City: " in eachline:
                    city = eachline.strip().split("<tr><th>City</th><td>")[1]
                    city = city.split("<")[0]            
                elif "<tr><th>Postal Code</th><td>" in eachline:
                    zip = eachline.strip().split("<tr><th>Postal Code</th><td>")[1]
                    zip = zip.split("<")[0] 
            time.sleep(3) #will sleep for 30 seconds
            if "Fail" in pagestatus:
                pagestatus = 'fail'
        else:
            WhoisArgs = ('whois %s' %(ip))
            response= Popen(WhoisArgs, shell=True, stdout=PIPE)
            for line in response.stdout:
                line = line.decode("utf-8")
                if ':' in line and "# " not in line and len(line) > 2:
                    line = line.strip()
                    content = ('%s\n%s' %(content, line))
                if email == '':
                    if line.startswith('RAbuseEmail:'):
                        try:
                            email = (line.split(': ')[1].lstrip())
                        except:pass    
                    elif line.lower().startswith('abuse-mailbox:'):email = (line.split(': ')[1].lstrip())
                    elif line.lower().startswith('orgabuseemail:'):email = (line.split(': ')[1].lstrip())
                    elif line.lower().startswith('Orgtechemail:'):email = (line.split(': ')[1].lstrip())
                
                if phone == '':
                    if line.lower().startswith('rabusephone:'):phone = (line.split(': ')[1].lstrip())
                    elif line.lower().startswith('orgabusephone:'):phone = (line.split(': ')[1].lstrip())
                    elif line.lower().startswith('phone:'):phone = (line.split(': ')[1].lstrip())
                    phone = phone.replace("+", "")
                if line.lower().startswith('rtechname:'):fullname = (line.split(': ')[1].lstrip())
                elif line.lower().startswith('person:'):fullname = (line.split(': ')[1].lstrip())                
                
                if line.lower().startswith('country:'):country = (line.split(': ')[1].lstrip())
                if line.lower().startswith('city:'):city = (line.split(': ')[1].lstrip())
                if line.lower().startswith('address:'):fulladdress = ('%s %s' %(fulladdress, line.split(': ')[1].lstrip()))
                if line.lower().startswith('stateprov:'):state = (line.split(': ')[1].lstrip())
                if line.lower().startswith('postalcode:'):zip = (line.split(': ')[1].lstrip())
                if line.lower().startswith('orgname:'):entity = (line.split(': ')[1].lstrip())
                elif line.lower().startswith('org-name:'):entity = (line.split(': ')[1].lstrip())
        
        print(y + ip, country, city, zip +o)
        write_ossint(ip, '9 - whois', fullname, url, email, '', phone, ip, entity, fulladdress
            , city, state, zip, country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', titleurl, pagestatus)


def whoiswebsite():    # testsite= google.com
    from subprocess import call, Popen, PIPE
    print(y, '\n\t<<<<< Checking whois against a list of Website\'s >>>>>'    , o)    

    for dnsdomain in dnsdomains:    
        # query = website
        # website = website.replace('http://','')
        # website = website.replace('https://','')
        # website = website.replace('www.','')
        
        url = ('https://www.ip-adress.com/website/%s' %(dnsdomain))
        url2 = ('https://whois.domaintools.com/%s' %(dnsdomain.replace('www.','')))
        (email,phone,fullname,country,city,state) = ('','','','','','')
        (city, country, zip, state, ip) = ('', '', '', '', '')
        (content, titleurl, pagestatus) = ('', '', '')
        (email, phone, fullname, entity, fulladdress) = ('', '', '', '', '') 

        if sys.platform == 'win32' or sys.platform == 'win64':    
            print('skipping whois query from windows')  # temp
            write_ossint(dnsdomain, '7 - whois', fullname, url, email, '', phone, ip, entity, fulladdress
                , city, state, zip, country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', dnsdomain, '', '', content, '', '', titleurl, pagestatus)

            write_ossint(dnsdomain, '9 - whois.domaintools.com', fullname, url2, '', '', '', '', '', ''
                , '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', dnsdomain, '', '', '', '', '', '', '')


        elif dnsdomain.endswith('.com') or dnsdomain.endswith('.edu') or dnsdomain.endswith('.net'):
            WhoisArgs = ('whois %s' %(dnsdomain))
            response= Popen(WhoisArgs, shell=True, stdout=PIPE)
            for line in response.stdout:
                line = line.decode("utf-8")
                if ':' in line and "# " not in line and len(line) > 2:
                    line = line.strip()
                    content = ('%s\n%s' %(content, line))
                if email == '':
                    if line.startswith('RAbuseEmail:'):
                        try:
                            email = (line.split(': ')[1].lstrip())
                        except:pass    
                    elif line.lower().startswith('abuse-mailbox:'):email = (line.split(': ')[1].lstrip())
                    elif line.lower().startswith('orgabuseemail:'):email = (line.split(': ')[1].lstrip())
                    elif line.lower().startswith('Orgtechemail:'):email = (line.split(': ')[1].lstrip())
                
                if phone == '':
                    if line.lower().startswith('rabusephone:'):phone = (line.split(': ')[1].lstrip())
                    elif line.lower().startswith('orgabusephone:'):phone = (line.split(': ')[1].lstrip())
                    elif line.lower().startswith('phone:'):phone = (line.split(': ')[1].lstrip())
                    phone = phone.replace("+", "")
                if line.lower().startswith('rtechname:'):fullname = (line.split(': ')[1].lstrip())
                elif line.lower().startswith('person:'):fullname = (line.split(': ')[1].lstrip())                
                
                if line.lower().startswith('country:'):country = (line.split(': ')[1].lstrip())
                if line.lower().startswith('city:'):city = (line.split(': ')[1].lstrip())
                if line.lower().startswith('address:'):fulladdress = ('%s %s' %(fulladdress, line.split(': ')[1].lstrip()))
                if line.lower().startswith('stateprov:'):state = (line.split(': ')[1].lstrip())
                if line.lower().startswith('postalcode:'):zip = (line.split(': ')[1].lstrip())
                if line.lower().startswith('orgname:'):entity = (line.split(': ')[1].lstrip())
                elif line.lower().startswith('org-name:'):entity = (line.split(': ')[1].lstrip())
                
            print(y, ("whois "+dnsdomain) ,g, email, ' ', phone  , o)
            write_ossint(dnsdomain, '7 - whois', fullname, url, email, '', phone, ip, entity, fulladdress
                , city, state, zip, country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', dnsdomain, '', '', content, '', '', titleurl, pagestatus)
        else:
            print(r, dnsdomain, " not an edu net or edu site?", o)
            write_ossint(dnsdomain, '7 - whois', fullname, url, email, '', phone, ip, entity, fulladdress
                , city, state, zip, country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', dnsdomain, '', '', content, '', '', titleurl, pagestatus)
        time.sleep(7)

def wordpress(): # testuser = kevinrose

    print('\n\t<<<<< Checking wordpress against a list of users >>>>>')
    for user in users:    
        (Success, fullname, lastname, firstname, case, gender) = ('','','','','','')
        (photo, country, website, email, language, username) = ('','','','','','')
        (city, note) = ('', '')
        user = user.rstrip()
        url = ('https://wordpress.org/support/users/%s/' %(user))
        note = ('https://%s.wordspress.com' %(user))        
        
        
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except socket.error as ex:
            print(ex)
        # except:
            # pass
        if 'That page can' not in content:
        # if 'Do you want to register' not in content:
            fullname = titleurl
            fullname = fullname.split(" (")[0]
            print(url, fullname) 
            write_ossint(user, '4 - wordpress', '', url, '', user, '', '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', pagestatus)

def wordpressprofiles(): # testuser = kevinrose

    print('\n\t<<<<< Checking wordpress profiles against a list of users >>>>>')
    for user in users:    
        (Success, fullname, lastname, firstname, case, gender) = ('','','','','','')
        (photo, country, website, email, language, username) = ('','','','','','')
        (city) = ('')
        user = user.rstrip()
        url = ('https://profiles.wordpress.org/%s/' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except:
            pass
        if '404' not in pagestatus:
            fullname = titleurl
            fullname = fullname.split(" (")[0]
            if fullname.lower() in titleurl.lower():
                (fullname, titleurl) = ('', '')
            
            print(url, fullname) 
            write_ossint(user, '5 - wordpress', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)

                
def wordpresssearchemail():    # testuser=    kevinrose@gmail.com 
    print('\n\t<<<<< Checking wordpressemail against a list of users >>>>>')
    for email in emails:
        
        url = ('http://en.search.wordpress.com/?q=\"%s\"' %(email))
        
        
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except:
            pass

        if 'Your search did not match any blog posts' not in content:

            content = content.split('\n') 
            for eachline in content:

                if eachline == "": pass                                             # skip blank lines
                else:
                    if 'post-title' in eachline:
                        # print(eachline) # temp
                        eachline = eachline.split('\"')
                        url = eachline[3]
                        write_ossint(email, '9 - wordpress', '', url, email, '', '', '', '', ''
                            , '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'research')
                        print(g + url , b, '\t', email, o)    

                        
def write_ossint(query, ranking, fullname, url, email , user, phone, ip, entity, 
    fulladdress, city, state, zip, country, note, aka, dob, gender, info, 
    misc, lastname, firstname, middlename, friend, otherurls, otherphones, 
    otheremails, case, sosfilenumber, president, sosagent, managers, 
    dnsdomain, dstip, srcip, content, referer, osurl,
    titleurl, pagestatus):

    # color
    try:
        if 'Fail' in pagestatus:  #
            format_function(bg_color='red')
        elif 'fail' in pagestatus or 'research' in pagestatus:  
            # format_function(bg_color='orange')
            format_function(bg_color='#FFc000')         # orange  
    except:pass        
        
        
    # elif 'google' in url:  #
        # format_function(bg_color='#92D050')  # green
    else:
        format_function(bg_color='white')
    
    global row

    sheet1.write_string(row, 0, query, format)
    sheet1.write_string(row, 1, ranking, format)
    sheet1.write_string(row, 2, fullname, format)
    sheet1.write_string(row, 3, url, format)
    sheet1.write_string(row, 4, email, format)
    sheet1.write_string(row, 5, user, format)
    sheet1.write_string(row, 6, phone, format)
    sheet1.write_string(row, 7, ip, format)
    sheet1.write_string(row, 8, entity, format)
    sheet1.write_string(row, 9, fulladdress, format)
    sheet1.write_string(row, 10, city, format)
    sheet1.write_string(row, 11, state, format)
    sheet1.write_string(row, 12, zip, format)
    sheet1.write_string(row, 13, country, format)
    sheet1.write_string(row, 14, note, format)
    sheet1.write_string(row, 15, aka, format)
    sheet1.write_string(row, 16, dob, format)
    sheet1.write_string(row, 17, gender, format)
    sheet1.write_string(row, 18, info, format)
    sheet1.write_string(row, 19, misc, format)
    sheet1.write_string(row, 20, lastname, format)
    sheet1.write_string(row, 21, firstname, format)
    sheet1.write_string(row, 22, middlename, format)
    sheet1.write_string(row, 23, friend, format)
    sheet1.write_string(row, 24, otherurls, format)
    sheet1.write_string(row, 25, otherphones, format)
    sheet1.write_string(row, 26, otheremails, format)
    sheet1.write_string(row, 27, case, format)
    sheet1.write_string(row, 28, sosfilenumber, format)
    sheet1.write_string(row, 29, president, format)
    sheet1.write_string(row, 30, sosagent, format)
    sheet1.write_string(row, 31, managers, format)
    sheet1.write_string(row, 32, dnsdomain, format)
    sheet1.write_string(row, 33, dstip, format)
    sheet1.write_string(row, 34, srcip, format)
    sheet1.write_string(row, 35, content, format)
    sheet1.write_string(row, 36, referer, format)
    sheet1.write_string(row, 37, osurl, format)
    sheet1.write_string(row, 38, titleurl, format)
    try:
        sheet1.write_string(row, 39, pagestatus, format)
    except:
        pass
    row += 1


def yelp():    # testuser=    GHoG4X4FY8D8L563zzPX5w
    print('\n\t<<<<< Checking yelp against a list of users >>>>>')
    for user in users:    
        url = ('http://www.yelp.com/user_details?userid=%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = ('','','','','')
        (fullname, info, note) = ('', '', '')
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)

            content = content.strip()
            titleurl = titleurl.strip()
       
        except:
            pass
        if 'uccess' in pagestatus:
            if '\'' in titleurl:
                fullname = titleurl.split('\'')[0]
            
            write_ossint(user, '7 - yelp.com', fullname, url, '', user, '', '', '', ''
                , '', '', '', '', note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)
            print(g + url + o)    


def youtube(): # testuser = kevinrose

    print('\n\t<<<<< Checking youtube against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        user = user.rstrip()
        url = ('https://www.youtube.com/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        titleurl = titleurl.replace(' - YouTube','')
        if '404' not in pagestatus:
            # for eachline in content.split("\n"):
                # if "\<title\>" in eachline:
                    # fullname = eachline.split('<title>')[1]
                    # print('hello world')

            fullname = titleurl
            
            if fullname.lower() == user.lower():
                fullname = ''
            
            
            print(url, fullname) 
            write_ossint(user, '4 - youtube', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        

def youtube_email():# testEmail= kevinrose@gmail.com  
    print(y + '\n\t<<<<< Checking youtube against a list of ' + b + 'emails' + y + ' >>>>>' + o)
    
    for email in emails:
        (country, city, zip, case, note) = ('', '', '', '', '')
        (content, referer, osurl, titleurl, pagestatus) = ('', '', '', '', '')
        url = ('https://youtube.com/results?search_query=%s' %(email))
        url = url.replace('@','%40')
        
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        # note = content
        for eachline in content.split("\n"):
            if "domain_exists" in eachline and "true" in eachline:
                print(" ")  # temp
            elif "exceeded daily limit" in eachline:
                note = "exceeded daily limit"
            else:
                # url = ('')
                print('')
        # pagestatus = ''  
        if 1==1:
        # if url != '':
        # if ('%') not in url: 
            print(url, email) 
            write_ossint(email, '9 - youtube', '', url, email, '', '', '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', referer, '', titleurl, pagestatus)



def usage():
    file = sys.argv[0].split('\\')[-1]
    print("\nDescription: " + description)
    print(file + " Version: %s by %s" % (version, author))
    print("\nExample:")
    # print("\t" + file + " -u -I input.txt -O out_urls.xlsx\t\t")
    # print("\t" + sys.argv[0] +" -C -I input.txt -O out_ossint.xlsx")

    print("\t" + sys.argv[0] +" -E")
    print("\t" + sys.argv[0] +" -i")
    print("\t" + sys.argv[0] +" -t")
    print("\t" + sys.argv[0] +" -s ")
    print("\t" + sys.argv[0] +" -p")
    print("\t" + sys.argv[0] +" -U")
    print("\t" + sys.argv[0] +" -W")
    print("\t" + sys.argv[0] +" -E -i -p -U -W")


if __name__ == '__main__':
    main()

# <<<<<<<<<<<<<<<<<<<<<<<<<< Revision History >>>>>>>>>>>>>>>>>>>>>>>>>>

"""
2.8.6 - made the .py and .exe version dummy proof. Just double click and it runs
2.7.6 - internet checker, removed -I and -O requirement
2.8.0 - kik
"""

# <<<<<<<<<<<<<<<<<<<<<<<<<< Future Wishlist  >>>>>>>>>>>>>>>>>>>>>>>>>>

"""
fix dnsdomains if it ends with / , take it off
tkinter purely gui interface

fix telegram with bad input
instagramtwo()
create a new identity_hunt with xlsx and requests instead of urllib2

https://vimeo.com/john

https://www.fiverr.com/samanvay 

https://hubpages.com/@kevinrose


"""

# <<<<<<<<<<<<<<<<<<<<<<<<<<      notes            >>>>>>>>>>>>>>>>>>>>>>>>>>

"""

ThereIsN0WayTh1sISaRealUser12345131234 gets detected as a phone number

"""

# <<<<<<<<<<<<<<<<<<<<<<<<<<      The End        >>>>>>>>>>>>>>>>>>>>>>>>>>