# identity_hunt
Query web to track people down by username, email, ip, websites and phone.

# installation:

pip install -r requirements.txt

# directions:
insert emails, phone numbers, usernames into input.txt

-E, --emailmodules    email modules

-i, --ips             ip modules

-p, --phonestuff      phone modules

-s, --samples         sample modules

-t, --test            sample ip, users & emails

-U, --usersmodules    username modules

-W, --websites        websites modules

Example:
identity_hunt.py -E -I input.txt -O Intel_.xlsx           # emails

identity_hunt.py -i -I input.txt -O Intel_.xlsx           # ip's only

identity_hunt.py -s                                         # prints sample info for your input.txt (ex. evinrose)

identity_hunt.py -p -I input.txt -O Intel_.xlsx             # phone numbers only

identity_hunt.py -U -I input.txt -O Intel_.xlsx             # if you are just doing usernames

identity_hunt.py -W -I input.txt -O Intel_.xlsx             # websites only

identity_hunt.py -i -p -U -W -I input.txt -O Intel_.xlsx    # this is the full command if you have mixed inputs.


