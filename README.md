# identityhunt (identiyhunt.py or identityhunt.exe)
OSINT: track people down by username, email, ip, phone and website.

## installation:

pip install -r requirements_identity_hunt.txt

## directions:
insert emails, phone numbers, usernames into input.txt

-b, --blurb           write ossint blurb

-E, --emailmodules    email modules

-i, --ips             ip modules

-p, --phonestuff      phone modules

-s, --samples         sample modules

-t, --test            sample ip, users & emails

-U, --usersmodules    username modules

-W, --websites        websites modules

Usage:

default behavior, if you enter no options it just runs with -E -i -p -U -W selected
```
double click identityhunt.exe
or
python identityhunt.py (from command prompt) 
```
blurb
```
python identityhunt.py -b
```
help
```
identityhunt.exe -H
or
python identityhunt.py -H
```
emails
```
identityhunt.exe -E
or
python identityhunt.py -E
```
ip's only
```
identityhunt.exe -i
or
python identityhunt.py -i
```
print sample info for your input.txt (ex. kevinrose)
```
identityhunt.exe -s
or
python identityhunt.py -s
```
phone numbers only
```
identityhunt.exe -p
or
python identityhunt.py -p
```
users only
```
identityhunt.exe -U
or
python identityhunt.py -U
```
websites only
```
identityhunt.exe -W
or
python identityhunt.py -W
```
you can add mixed input types at once.
```
identityhunt.exe -E -i -p -U -W
or
python identityhunt.py -E -i -p -U -W
```


![sample output](Images/intel_sample.png)

