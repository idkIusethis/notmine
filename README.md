# Python Strawpoll.me Voting Bot

A Python strawpoll.me voting bot allowing multiple voting while bypassing IP duplication checks by using proxies.

# Terms: #
Poll ID: This is the uninque ID of the poll, for example given the url of a poll
https://www.strawpoll.me/16791383/
The Poll id here is "16791383"
-----
Option Index: option index is the index of the options avalable, like 1, 2, 3, 4
so for example:
we have a poll: "What do you mean ?" with options
"YES" 
"NO"

In this case the option "YES" corresponds to index 1 and "NO" corresponds to index 2

# The proxies file: #
The proxy file is named "proxies.txt" if the file doesn't exist an error message is shown like this:
'[x] Proxy file does not exists."
press 'Enter' key to exit.

In this file is where the programs read in proxies to be used. and is in the below format:
IP:PORT
like for example:

1.20.102.177:48283#TH
95.47.116.133:31808#CZ
213.6.31.186:36127#PS
41.160.245.149:50182#ZA
177.10.197.197:35171#BR
207.154.200.199:3128#DE
220.132.35.14:44556#TW


# A sample RUN #
Usage:

C:\dvn-anakin> python strawpoll.py

Enter Poll ID: <poll id goes here. e.g 16791383>
Loading Options ... Done.

Enter Option Index between 1 - 2
Enter Option index: <option index goes here, we are using yes so "1" is chosen.>

Option ID: 137358100
Loaded 7844 proxies.
------------------------------
Starting up ...
------------------------------
[*] Using Proxy 194.146.230.9:41258
[*] Using Proxy 91.203.27.139:41533
[*] Using Proxy 101.51.141.106:60623
[*] Using Proxy 27.96.84.17:32135
<snipped ...>
