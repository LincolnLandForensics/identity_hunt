#!/usr/bin/python
# coding: utf-8

# <<<<<<<<<<<<<<<<<<<<<<<<<<      Copyright        >>>>>>>>>>>>>>>>>>>>>>>>>>

# Copyright (C) 2022 LincolnLandForensics
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

import os
import re
import sys
import time
import random
import requests
import datetime
import argparse  # for menu system
import xlsxwriter
from subprocess import call
from bs4 import BeautifulSoup

# import phonenumbers
# from phonenumbers import geocoder, carrier


# <<<<<<<<<<<<<<<<<<<<<<<<<<      Pre-Sets       >>>>>>>>>>>>>>>>>>>>>>>>>>

author = 'LincolnLandForensics'
description = "Query web to track people down by username,email,ip..."
tech = 'LincolnLandForensics'  # change this to your name if you are using Linux
version = '2.7.0'

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


# <<<<<<<<<<<<<<<<<<<<<<<<<<      Menu           >>>>>>>>>>>>>>>>>>>>>>>>>>

def main():
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
    parser.add_argument('-i','--ips', help='ip modules', required=False, action='store_true')
    parser.add_argument('-p','--phonestuff', help='phone modules', required=False, action='store_true')
    parser.add_argument('-s','--samples', help='sample modules', required=False, action='store_true')
    parser.add_argument('-t','--test', help='sample ip, users & emails', required=False, action='store_true')
    parser.add_argument('-U','--usersmodules', help='username modules', required=False, action='store_true')
    parser.add_argument('-W','--websites', help='websites modules', required=False, action='store_true')    
    
    args = parser.parse_args()
    cls()
    print_logo()

    if args.samples:  
        samples()
        return 0
        
    elif not args.input:  # this section might be redundant
        parser.print_help()
        usage()
        return 0

    if args.input and args.output:
        global filename
        filename = args.input
        global Spreadsheet
        Spreadsheet = args.output
        create_ossint_xlsx()
        master()   # re-print(original input list as 1-master and separate emails, ips, phones & users
        # print(emails) # temp

        if args.emailmodules:  
            # BingEmail()    # alpha
            emailrep() #alpha
            # facebookemail()    # alpha
            # flickremail()    # alpha  add scraper Invalid API Key
            # GoogleScrapeEmail() # todo
            # lifestreamemail()# alpha
            # linkedinemail()    # alpha stopped working
            myspaceemail()    # add info, scrape url
            # naymzemail()    # beta
            # nikeplusemail()    # need login
            # piplemail()        # add info    (takes 90 seconds per email)
            # spokeo()            # needs work    (timeout error)
            # stumbluponemail()# alpha need login
            thatsthememail()    # https://thatsthem.com/email/smooth8101@yahoo.com
            twitteremail()    
            wordpresssearchemail()  # works
            # YelpEmail()        # alpha
            
        if args.ips:  
            print("checking :", ips)
            geoiptool() # works but need need to rate limit
            thatsthemip()
            whoisip()   # beta
            
        # phone modules
        if args.phonestuff:
            thatsthemphone()
            fouroneone()   # https://www.411.com/phone/1-417-967-2020
            # phonecarrier()  #beta
            validnumber()    #beta
            whitepagesphone()

        if args.test:  
            instagramtwo()    # beta
            
        if args.usersmodules:  
            # About()        # alpha
            # badoo()    # beta add info
            # bebo()              # down for upgrade
            # bitbucket()        # add photo, note, name, info
            # blackplanet()                    
            # blogspot()  # works
            # dailymotion()                               
            # delicious()        # beta
            # deviantart()                    
            # digg()        # beta
            disqus()                        
            ebay()  # works
            # etsy()    
            facebook()  # works
            # ffffound()        # beta add inf
            flickr()   # add photo, note, name, info
            # formspring()    # beta add title & info
            # github()            
            # GoogleScrape()    # beta
            gravatar()  # works
            # HackerRank()        # add inf
            # hackthissite()        # add inf
            # hi5()        # add inf (stopped working)
            # hi52()        # beta add inf
            # hulu()        # beta add inf # may need new profile url
            imageshack()    # works
            # imgur()                                      
            instagram()   # always fails
            instructables() # works
            # justintv()        # add info
            # kickstarter()        # add info                    
            kik()   # alpha
            # kongregate()        # add info
            # lastfm()            # add info
            # lifestream()        # add info
            # leakedin()        # beta
            # linkedin()        # needs auth
            # LiveJournal()        # add info    
            # mapmywalk()        # add info
            # mobypicture()    # add info
            # MyLife()            # add info
            myspace()        # add info
            # netlog()
            # okcupid()        # add info
            # pastebin()        # add info
            # pandora()                 # add info
            # peepmail()        # alpha
            # photobucket()    
            pinterest() # works
            # pipl()            # alpha
            # pwned()                            
            # rankmyhack()    # website offline
            # reddit()                                                                  
            # scribd()            
            # slideshare()        # add info
            # softpedia()        
            spotify()   # works
            # stumblupon()        
            # squidoo()                                                                                  
            # tagged()        # add info
            # technorati()        # add info
            # telegram()    # alpha
            tiktok()    # todo
            # thingiverse()        # add info    
            # topsy()        # alpha add info
            # tumblr()                        
            # twitter()   # fails
            # twitterfriends()    # alpha add info
            # typepad()        # add info (verify)
            # ustream()        # add info 
            venmo() # alpha
            # Vimeo()            
            # webshots()        # now requires auth
            # wifeswap()        # beta
            # wordpress() # works test
            wordpressprofiles()    
            # xanga()            # beta    add info
            # Xing()            
            # yahooprofile()    # alpha    add info
            # Yfrog()            # add info
            youtube()   # works


        if args.websites:  
            # Bing()        # alpha
            titles()    # alph
            whoiswebsite()    # works
            
        # if args.websites:
             # row = read_url(row)
            # row = read_url()

    # set linux ownership    
    if sys.platform == 'win32' or sys.platform == 'win64':
        pass
    else:
        call(["chown %s.%s *.xlsx" % (tech.lower(), tech.lower())], shell=True)

    workbook.close()
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

    inputfile = open(filename)
    for eachline in inputfile:
        
        (query, ranking, fullname, url, email , user) = ('', '', '', '', '', '')
        (phone, ip, entity, fulladdress, city, state) = ('', '', '', '', '', '')
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
        elif re.search(regex_phone, query):  # regex_phone
            (phone) = (query)
            if query.lower() not in phones:            # don't add duplicates
                phones.append(phone)

            
        elif query.lower().startswith('http'):
            url = query
            if url.lower() not in websites:            # don't add duplicates
                websites.append(url)            
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
    # return USERS,IPS,EMAILS        

def fouroneone():# testPhone= 708-372-8101  view-source:https://www.411.com/phone/1-417-967-2020
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


def blogspot(): # testuser = kevinrose

    print('\n\t<<<<< Checking blogspot against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        user = user.rstrip()
        url = ('https://%s.blogspot.com' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        if '404' not in pagestatus:
            fullname = titleurl
            print(url, titleurl) 
            write_ossint(user, '4 - blogspot', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        


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

def disqus(): # testuser = kevinrose

    print('\n\t<<<<< Checking discus against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        user = user.rstrip()
        url = ('http://disqus.com/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        
        if '404' not in pagestatus:
            fullname = titleurl
            print(url, titleurl) 
            write_ossint(user, '5 - discus', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        


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
            write_ossint(user, '5 - ebay', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        

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



def facebook(): # testuser = kevinrose

    print('\n\t<<<<< Checking facebook against a list of users >>>>>')
    for user in users:    
        (Success,FullName,LastName,FirstName,ID,Gender) = ('','','','','','')
        (Photo,Country,Website,Email,Language,Username) = ('','','','','','')
        (city, country) = ('', '')
        user = user.rstrip()
        url = ('http://facebook.com/%s' %(user))

        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except:
            pass

        if 'Success' in pagestatus:
            fullname = titleurl
            print(url, fullname) 
            write_ossint(user, '4 - Facebook', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)

def flickr(): # testuser = kevinrose

    print('\n\t<<<<< Checking flickr against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus, content) = ('', '', '', '', '', '')
        (note) = ('')
        user = user.rstrip()
        url = ('http://www.flickr.com/people/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        # content = content.replace('\n',' ') # beta
        # for eachline in content.split("\n"):
        for eachline in content.split("  <"):
            if "og:title" in eachline:
                fullname = eachline.strip().split("\"")[1]
                print(fullname) # temp
            # elif "My sites:" in eachline:
                # eachline = eachline.replace('\n',' ')
                # note = eachline.strip()
                # note = eachline.strip().split(": ")[1]
                # city = city.split("<")[0]            
            # elif "Postal Code: " in eachline:
                # zip = eachline.strip().split(": ")[1]
                # zip = zip.split("<")[0] 

        if '404' not in pagestatus:
            print(url, titleurl) 
            write_ossint(user, '4 - flickr - add info', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        

           
def format_function(bg_color='white'):
    global format
    format = workbook.add_format({
        'bg_color': bg_color
    })
    
def geoiptool():    # testuser= 77.15.67.232
    # print('\n\t<<<<< Checking geoiptool against a list of IPs >>>>>')
    print('\n\t<<<<< Checking geodatatool.com against a list of IPs >>>>>')
    for ip in ips:
        (country, city, state, zip) = ('', '', '', '')
     
        # url = ('http://geoiptool.com/en/?IP=%s' %(ip))
        url = ('https://www.geodatatool.com/en/?IP=%s' %(ip))
        
        
        (content, referer, osurl, titleurl, pagestatus) = request(url)

        for eachline in content.split("\n"):
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

def gravatar(): # testuser = kevinrose

    print('\n\t<<<<< Checking gravatar against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        user = user.rstrip()
        url = ('http://en.gravatar.com/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        if '404' not in pagestatus:
            fullname = titleurl
            print(url, titleurl) 
            write_ossint(user, '4 - gravatar', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        


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
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        

def instagram():    # testuser=    kevinrose     # add info
    print('\n\t<<<<< Checking instagram against a list of users >>>>>')
    for user in users:    
        url = ('https://instagram.com/%s/' %(user))
        (content, referer, osurl, titleurl, pagestatus) = ('','','','','fail')
        # try:
            # (content, referer, osurl, titleurl, pagestatus) = request(url)
            # content = content.strip()
            # titleurl = titleurl.strip()
            # for eachline in content.split("\n"):
                # if "@context" in eachline:
                    # content = eachline.strip()
            # if "Fail" in pagestatus:
                # pagestatus = 'fail'
        # except:
            # pass
        # time.sleep(3) # will sleep for 3 seconds
        write_ossint(user, '67 - instagram.com friends: grab info', '', url, '', user, '', '', '', ''
            , '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', titleurl, pagestatus)
        print(g + url + content + o)    

 
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

    print('\n\t<<<<< Checking instructablest against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        user = user.rstrip()
        url = ('http://www.instructables.com/member/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        if '404' not in pagestatus:
            fullname = titleurl
            print(url, titleurl) 
            write_ossint(user, '4 - instructables', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        

def kik(): # testuser = kevinrose
    print('\n\t<<<<< Checking kik against a list of users >>>>>')
    for user in users:    
        (fullname, titleurl, pagestatus, content) = ('', '', '', '')
        (note, firstname, lastname, photo, misc, lastseen) = ('', '', '', '', '', '')

        user = user.rstrip()
        url = ('https://ws2.kik.com/user/%s' %(user))
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
                photo = eachline.strip().split(":\"")[1].replace("\\","")
            fullname = ('%s %s' %(firstname,lastname))
        if '404' not in pagestatus:
            print("%s = %s" %(url, fullname)) # temp
            write_ossint(user, '4 - kik', fullname, url, '', user, '', '', '', ''
                , '', '', '', '', note, '', '', '', '', misc, lastname, firstname, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')        


def linkedin():    # testuser=    kevinrose     # grab info
    print('\n\t<<<<< Checking linkedin against a list of users >>>>>')
    for user in users:    
        (email, fullname, lastname,lastname,firstname) = ('', '', '', '', '')

        url = ('http://linkedin.com/in/%s' %(user))
        (city, fullname, lastname, country) = ('', '','','')
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except:pass
        if 1==1:
        # if " LinkedIn" in titleurl:
            titleUrl = titleurl.replace("  | LinkedIn","")
            if titleurl.lower() != user.lower():
                fullname = titleurl
            
            if ' ' in fullname:
                fullname2 = fullname.split(" ")

                firstname = fullname2[0]
                lastname = fullname2[1]

            write_ossint(user, '5 - linkedin.com', '', url, '', '', '', '', email, ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', titleurl, pagestatus)
            print(g , url, '\t', y , fullname ,  o)

def myspace(): # testuser = kevinrose

    print('\n\t<<<<< Checking myspace against a list of users >>>>>')
    for user in users:    
        (Success, fullname, lastname, firstname, case, gender) = ('','','','','','')
        (photo, country, website, email, language, username) = ('','','','','','')
        (city) = ('')
        user = user.rstrip()
        url = ('https://myspace.com/%s' %(user))

        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except:
            pass

        if 'Success' in pagestatus:
            fullname = titleurl
            fullname = fullname.split(" (")[0]
            print(url, fullname) 
            write_ossint(user, '4 - myspace', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)
         
def myspaceemail():# testEmail= kandyem@yahoo.com   267619602
    print(y + '\n\t<<<<< Checking myspace against a list of ' + b + 'emails' + y + ' >>>>>' + o)
    
    for email in emails:
        (country, city, zip, case) = ('', '', '', '')
        
        url = ('http://www.myspace.com/search/people?q=%s&ac=t' %(email))
        (content, referer, osurl, titleurl, pagestatus) = request(url)

        for eachline in content.split("\n"):
            if "data-id" in eachline and case == '':
                case = eachline.strip().split(" data-id=")[1]
                case = case.replace("\"", "").split(" ")[0]
                url = ('https://myspace.com/%s' %(case))

        if ('%') not in url: 
            print(url, email) 
            write_ossint(email, '5 - myspace.com', '', url, email, '', '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', referer, '', titleurl, pagestatus)

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
        
        url = ('http://www.pinterest.com/%s/' %(user))
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

            write_ossint(user, '5 - pinterest', fullname, url, '', user, '', '', email, ''
                , city, '', '', country, note, '', '', '', '', '', lastname, firstname, '', '', otherurls, '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, '')            
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

def request(url):
    (content,referer,osurl,titleurl,pagestatus) = ('','','','','')
    if url.lower().startswith('http'):
        page = requests.get(url)
    else:
        page  = requests.get("http://" +url)
    pagestatus  = page.status_code
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.prettify()

#Clean up titleurl
    try:
        titleurl = str(titleurl)    #test
        titleurl = (titleurl.encode('utf8'))    # 'ascii' codec can't decode byte
        titleurl = (titleurl.decode('utf8'))    # get rid of bytes b''
    except TypeError as error:
        print(error)
        # except:
        # titleurl = ''
        
    # print('type(titleurl) = %s' %(type(titleurl)))      # temp
    # if type(titleurl) == None:
        # print('ehlloe') # temp
    # try:
        # titleurl = str(soup.title.string)    # todo
    # except TypeError as error:
        # print(error)
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

    pagestatus = pagestatus.strip()

# Clean up titleurl
    try:
        titleurl = str(titleurl)    #test
        titleurl = (titleurl.encode('utf8'))    # 'ascii' codec can't decode byte
        titleurl = (titleurl.decode('utf8'))    # get rid of bytes b''
    except TypeError as error:
        print(error)
        titleurl = ''

    titleurl = titleurl.strip()
    content = content.strip()
    
    return (content,referer,osurl,titleurl,pagestatus)    


def samples():
    print('''        Sample users are:
    
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

        Sample Emails are:

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

        Sample IP's are:
        
77.15.67.232
92.20.236.78

    Sample phone
708-372-8101
'''
)    


def spotify(): # testuser = kevinrose

    print('\n\t<<<<< Checking spotify against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        user = user.rstrip()
        url = ('http://open.spotify.com/user/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        if '404' not in pagestatus:
            fullname = titleurl
            print(url, titleurl) 
            write_ossint(user, '4 - spotify', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        

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
            write_ossint(email, '6 - thatsthem', '', url, email, '', '', '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', referer, '', titleurl, pagestatus)

def thatsthemip():# testIP= 8.8.8.8
    print(y + '\n\t<<<<< Checking thatsthem against a list of ' + b + 'ip' + y + ' >>>>>' + o)
    
    for ip in ips:
        (country, city, zip, case, note, state) = ('', '', '', '', '', '')
        
        url = ('https://thatsthem.com/ip/%s' %(ip))
        (content, referer, osurl, titleurl, pagestatus) = request(url)

        for eachline in content.split("\n"):
            if "403 ERROR" in eachline:
                pagestatus = '403 Error'
                content = ''
            elif "Found 0 results for your query" in eachline:
                print("not found")  # temp
                url = ('')
            elif "located in " in eachline:
                state = eachline
                note = eachline
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
        print('phone = >%s<' %(phone))        
        url = ('https://thatsthem.com/phone/%s' %(phone))
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
            print(url, phone) 
            write_ossint(phone, '6 - thatsthem', '', url, '', '', phone, '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', referer, '', titleurl, pagestatus)

def telegram(): # testuser = kevinrose

    print('\n\t<<<<< Checking telegram against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus, content) = ('', '', '', '', 'research', '')
        user = user.rstrip()
        url = ('https://t.me/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        for eachline in content.split("\n"):
            print(eachline) # temp

            if "og:title" in eachline:
                fullname = eachline.strip().split("\"")[1]
                print(fullname) # temp
        # if 'no subscribers' in content:
            # print('no subscribers') # temp
        # else:
            # print('subscribers') # temp   
            # pagestatus = '404 fail'
        # fullname = titleurl
        print(url, titleurl) 
        write_ossint(user, '70 - telegram', fullname, url, '', user, '', '', '', ''
            , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', titleurl, pagestatus)        


def tiktok(): # testuser = kevinrose

    print('\n\t<<<<< Checking tiktok against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus, content) = ('', '', '', '', 'research', '')
        user = user.rstrip()
        url = ('http://tiktok.com/@%s?' %(user))
        # (content, referer, osurl, titleurl, pagestatus) = request(url)
        # titleurl = titleurl.replace(' - YouTube','')
        if 't find this account' in content:
            pagestatus = '404 fail'
        fullname = titleurl
        print(url, titleurl) 
        write_ossint(user, '70 - tiktok', fullname, url, '', user, '', '', '', ''
            , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', titleurl, pagestatus)        

        # if '404' not in titleurl:
            # fullname = titleurl
            # print(url, titleurl) 
            # write_ossint(user, '4 - tiktok', fullname, url, '', user, '', '', '', ''
                # , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        


def titles():    # testsite= google.com
    from subprocess import call, Popen, PIPE
    print(y, '\n\t<<<<< Titles grab against a list of Website\'s >>>>>'    , o)    

    for website in websites:    
        url = website
        url = url.replace("https://", "http://")
        
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except TypeError as error:
            print(error)
        
        dnsdomain = url.lower()
        dnsdomain = dnsdomain.replace("https://", "")
        dnsdomain = dnsdomain.replace("http://", "")
        dnsdomain = dnsdomain.split('/')[0]

        print(y, website , pagestatus,  o)
        write_ossint(url, '7 ', '', url, '', '', '', '', '', ''
            , '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', dnsdomain, '', '', content, referer, osurl, titleurl, pagestatus)
        
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
            write_ossint(user, '15 - twitter.com', fullname, url, email, user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)
            pass
            
def twitteremail(): # test Email=     craig@craigslist.org 
    print(y + '\n\t<<<<< Checking twitter against a list of emails >>>>>' + o)
    # {"valid":false,"msg":"Email has already been taken. An email can only be used on one Twitter account at a time.","color":"red","taken":true,"blank":false}
    for email in emails:
        url = ('https://twitter.com/users/email_available?email=%s' %(email))
        (country, city, zip) = ('', '', '')        
        (content, referer, osurl, titleurl, pagestatus) = request(url)    # access denied cloudflare

        if 'Email has already been taken' in content:
            write_ossint(email, '5 - twitter.com', '', url, email, '', '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', '', '')
            print(g + email + o)

def validnumber():# testPhone= 708-372-8101
    print(y + '\n\t<<<<< Checking validnumber against a list of ' + b + 'phone numbers' + y + ' >>>>>' + o)
    # https://validnumber.com/phone-number/3124377966/
    for phone in phones:
        (country, city, zip, case, note) = ('', '', '', '', '')
        (content, referer, osurl, titleurl, pagestatus)  = ('', '', '', '', '')
        phone = phone.replace('(','').replace(')','').replace(' ','')
        # print('phone = >%s<' %(phone))     #temp   
        url = ('https://validnumber.com/phone-number/%s/' %(phone))
        (content, referer, osurl, titleurl, pagestatus) = request(url)    # protected by cloudflare

        for eachline in content.split("\n"):
            if "No name associated with this number" in eachline and case == '':
                print("not found")  # temp
                url = ('')
            elif "Find out who owns" in eachline:
                if 'This device is registered in ' in eachline:
                    city = eachline.split("This device is registered in ")[1].split("Free owner details")[0]
            # elif "schema.org" in eachline:
                # print('oooh doggy') # temp
                # note = eachline
        pagestatus = ''        
                
        if url != '':
        # if ('%') not in url: 
            print(url) 
            write_ossint(phone, '3 - validnumber', '', url, '', '', phone, '', '', ''
                , city, '', '', country, note, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', referer, '', titleurl, pagestatus)



def venmo(): # testuser = kevinrose

    print('\n\t<<<<< Checking venmo against a list of users >>>>>')
    for user in users:    
        (Success, fullname, lastname, firstname, case, gender) = ('','','','','','')
        (photo, country, website, email, language, username) = ('','','','','','')
        (city) = ('')
        user = user.rstrip()
        # url = ('http://venmo.com/%s' %(user))
        url = ('https://venmo.com/u/%s' %(user))

        (content, referer, osurl, titleurl, pagestatus) = request(url)
        
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except:
            pass
        if 'Do you want to register' not in content:
            fullname = titleurl
            fullname = fullname.split(" (")[0]
            print(url, fullname) 
            write_ossint(user, '9 - venmo', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)


def whitepagesphone():# testuser=    210-316-9435
    print('\n\t<<<<< Checking whitepages against a list of users >>>>>')
    for phone in phones:    
        (country, city, zip) = ('', '', '')
        (titleurl) = ('')
        url = ('http://www.whitepages.com/search/ReversePhone?full_phone=%s' %(phone))
        # (content, referer, osurl, titleurl, pagestatus) = request(url)    # access denied cloudflare

        write_ossint(phone, '7 - whitepages', '', url, '', '', phone, '', '', ''
            , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, '')
    

def whoisip():    # testuser=    77.15.67.232
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
        write_ossint(ip, '7 - whois', fullname, url, email, '', phone, ip, entity, fulladdress
            , city, state, zip, country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', content, '', '', titleurl, pagestatus)

def whoiswebsite():    # testsite= google.com
    from subprocess import call, Popen, PIPE
    print(y, '\n\t<<<<< Checking whois against a list of Website\'s >>>>>'    , o)    

    for dnsdomain in dnsdomains:    
        # query = website
        # website = website.replace('http://','')
        # website = website.replace('https://','')
        # website = website.replace('www.','')
        
        url = (' https://www.ip-adress.com/website/%s' %(dnsdomain))
        (email,phone,fullname,country,city,state) = ('','','','','','')
        (city, country, zip, state, ip) = ('', '', '', '', '')
        (content, titleurl, pagestatus) = ('', '', '')
        (email, phone, fullname, entity, fulladdress) = ('', '', '', '', '') 

        if sys.platform == 'win32' or sys.platform == 'win64':    
            write_ossint(dnsdomain, '7 - whois', fullname, url, email, '', phone, ip, entity, fulladdress
                , city, state, zip, country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', dnsdomain, '', '', content, '', '', titleurl, pagestatus)
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
        (city) = ('')
        user = user.rstrip()
        url = ('http://%s.wordspress.com' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except:
            pass
        if 'Do you want to register' not in content:
            fullname = titleurl
            fullname = fullname.split(" (")[0]
            print(url, fullname) 
            write_ossint(user, '4 - wordpress', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)

def wordpressprofiles(): # testuser = kevinrose

    print('\n\t<<<<< Checking wordpress profiles against a list of users >>>>>')
    for user in users:    
        (Success, fullname, lastname, firstname, case, gender) = ('','','','','','')
        (photo, country, website, email, language, username) = ('','','','','','')
        (city) = ('')
        user = user.rstrip()
        url = ('http://profiles.wordpress.org/%s/' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        
        try:
            (content, referer, osurl, titleurl, pagestatus) = request(url)
        except:
            pass
        if '404' not in pagestatus:
            fullname = titleurl
            fullname = fullname.split(" (")[0]
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
                        write_ossint(email, '2 - wordpress.com (email exists)', '', url, email, '', '', '', '', ''
                            , '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')
                        print(g + url , b, '\t', email, o)    

                        
def write_ossint(query, ranking, fullname, url, email , user, phone, ip, entity, 
    fulladdress, city, state, zip, country, note, aka, dob, gender, info, 
    misc, lastname, firstname, middlename, friend, otherurls, otherphones, 
    otheremails, case, sosfilenumber, president, sosagent, managers, 
    dnsdomain, dstip, srcip, content, referer, osurl,
    titleurl, pagestatus):

    # color
    if 'Fail' in pagestatus:  #
        format_function(bg_color='red')
    elif 'fail' in pagestatus or 'research' in pagestatus:  
        format_function(bg_color='orange')
    # elif 'google' in url:  #
        # format_function(bg_color='green')
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
    sheet1.write_string(row, 39, pagestatus, format)

    row += 1

def youtube(): # testuser = kevinrose

    print('\n\t<<<<< Checking youtube against a list of users >>>>>')
    for user in users:    
        (city, country, fullname, titleurl, pagestatus) = ('', '', '', '', '')
        user = user.rstrip()
        url = ('http://www.youtube.com/%s' %(user))
        (content, referer, osurl, titleurl, pagestatus) = request(url)
        titleurl = titleurl.replace(' - YouTube','')
        if '404' not in pagestatus:
            fullname = titleurl
            print(url, titleurl) 
            write_ossint(user, '4 - youtube', fullname, url, '', user, '', '', '', ''
                , city, '', '', country, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', titleurl, pagestatus)        


def usage():
    file = sys.argv[0].split('\\')[-1]
    print("\nDescription: " + description)
    print(file + " Version: %s by %s" % (version, author))
    print("\nExample:")
    # print("\t" + file + " -u -I input.txt -O out_urls.xlsx\t\t")
    # print("\t" + sys.argv[0] +" -C -I input.txt -O out_ossint.xlsx")
    print("\t" + sys.argv[0] +" -E -I input.txt -O Intel_.xlsx")
    print("\t" + sys.argv[0] +" -i -I input.txt -O Intel_.xlsx")
    print("\t" + sys.argv[0] +" -t -I input.txt -O Intel_.xlsx")
    print("\t" + sys.argv[0] +" -s ")
    print("\t" + sys.argv[0] +" -p -I input.txt -O Intel_.xlsx")
    print("\t" + sys.argv[0] +" -U -I input.txt -O Intel_.xlsx")
    print("\t" + sys.argv[0] +" -W -I input.txt -O Intel_.xlsx")
    print("\t" + sys.argv[0] +" -i -p -U -W -I input.txt -O Intel_.xlsx")
    
    # print("\t" + sys.argv[0] +" -E -i -U -I input.txt -O output.csv")    
 

#  print("\t" + file +" -s -I nodes.txt -O out_second.xls")


if __name__ == '__main__':
    main()

# <<<<<<<<<<<<<<<<<<<<<<<<<< Revision History >>>>>>>>>>>>>>>>>>>>>>>>>>

"""
1.0.0 - kik
0.0.2 - python2to3 conversion
0.0.1 - based on Password_recheckinator.py
"""

# <<<<<<<<<<<<<<<<<<<<<<<<<< Future Wishlist  >>>>>>>>>>>>>>>>>>>>>>>>>>

"""
instagramtwo()
create a new identity_hunt with xlsx and requests instead of urllib2
python sherlock kevinrose # mirror sherlock

https://validnumber.com/phone-number/3124377966/
https://ttlc.intuit.com/community/user/viewprofilepage/user-id/_95

"""

# <<<<<<<<<<<<<<<<<<<<<<<<<<      notes            >>>>>>>>>>>>>>>>>>>>>>>>>>

"""


"""

# <<<<<<<<<<<<<<<<<<<<<<<<<<      The End        >>>>>>>>>>>>>>>>>>>>>>>>>>