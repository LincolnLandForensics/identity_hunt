# identity_hunt (identiy_hunt.py or identity_hunt.exe)
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
double click identity_hunt.exe
or
python identity_hunt.py (from command prompt) 
```
help
```
identity_hunt.exe -H
or
python identity_hunt.py -H
```
emails
```
identity_hunt.exe -E
or
python identity_hunt.py -E
```
ip's only
```
identity_hunt.exe -i
or
python identity_hunt.py -i
```
print sample info for your input.txt (ex. kevinrose)
```
identity_hunt.exe -s
or
python identity_hunt.py -s
```
phone numbers only
```
identity_hunt.exe -p
or
python identity_hunt.py -p
```
users only
```
identity_hunt.exe -U
or
python identity_hunt.py -U
```
websites only
```
identity_hunt.exe -W
or
python identity_hunt.py -W
```
you can add mixed input types at once.
```
identity_hunt.exe -E -i -p -U -W
or
python identity_hunt.py -E -i -p -U -W
```


![sample output](Images/intel_sample.png)

