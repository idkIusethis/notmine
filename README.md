# Python Strawpoll.me Voting Bot

A Python strawpoll.me voting bot allowing multiple voting while bypassing IP duplication checks by using proxies.

# Terms: #
**1. Poll ID** <br />
Each poll has unique ID which can be found within its URL address <br />
*Example:* <br />
*Given the URL of a poll https://www.strawpoll.me/16791383/, poll's ID is 16791383*

**2. Option index** <br />
Option index is the index of the options avalable for that poll

*Example:* <br />
*Given the poll "Are You the noobmaster?" with options (possible answers):* <br />
*a) Yes* <br />
*b) No*, <br />
*The first answer 'Yes' has option index 1, the second has option index 2* 

# The proxies file: #
The proxy file is named **proxies.txt** and it contains proxies in this format: *IP:PORT* <br />
*Example:* <br />
*1.20.102.177:48283 <br />
95.47.116.133:31808 <br />
213.6.31.186:36127 <br />
41.160.245.149:50182 <br />
177.10.197.197:35171*

If **proxies.txt** doesn't exist, an error message is shown like this:
```
[x] Proxy file does not exists.
press 'Enter' key to exit.
```


# Running the program #
*Example:* <br />
*Having a poll with the following URL address https://www.strawpoll.me/16791383, this is how You would run the script* <br />

Run the script from command line:
```
C:\dvn-anakin> python strawpoll.py
```

Follow the instructions
```
Enter Poll ID: 16791383
Loading Options ... Done.

Enter Option Index between 1 - 2
Enter Option index: 2

Option ID: 137358100
Loaded 7844 proxies.
------------------------------
Starting up ...
------------------------------
[*] Using Proxy 194.146.230.9:41258
[*] Using Proxy 91.203.27.139:41533
[*] Using Proxy 101.51.141.106:60623
[*] Using Proxy 27.96.84.17:32135

...
```