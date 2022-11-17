# identity_hunt
OSINT: track people down by username, email, ip, phone and website.

## installation:

pip install -r requirements.txt

## directions:
insert emails, phone numbers, usernames into input.txt

-E, --emailmodules    email modules

-i, --ips             ip modules

-p, --phonestuff      phone modules

-s, --samples         sample modules

-t, --test            sample ip, users & emails

-U, --usersmodules    username modules

-W, --websites        websites modules

Usage:

help
'''
identity_hunt.py -H
'''
emails
'''
identity_hunt.py -E
'''
ip's only
'''
identity_hunt.py -i
'''
print sample info for your input.txt (ex. kevinrose)
'''
identity_hunt.py -s
'''
phone numbers only
'''
identity_hunt.py -p
'''
users only
'''
identity_hunt.py -U
'''
websites only
'''
identity_hunt.py -W
'''
you can add mixed input types at once.
'''
identity_hunt.py -E -i -p -U
'''


![sample output](Images/intel_sample.png)

