#!python3
import bs4
import requests
import threading
import queue
import os
import time

class StrawPoll(threading.Thread):
	PROXY_FILE = 'proxies.txt'

	def __init__(self, poll_id):
		threading.Thread.__init__(self)
		self.poll_id = poll_id
		self.timeout = 30
		self.url = 'https://www.strawpoll.me/{}'.format(self.poll_id)
		self.option_id = ''
		self.payload = ''
		self.headers = self.loadHeaders()
		self.cookies = None
		self.proxy =  self.selectProxy()
		if self.proxy is None:
			self.status = False
		else:
			self.status = True


	def run(self):
		if not self.getCookieSoup():
			#print('Could not acquire cookie and soup.')
			return
		time.sleep(1)
		self.vote(OPTION_ID)

	def loadHeaders(self):
		# load headers
		header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
			'Accept': '*/*',
			'Accept-Language': 'de,en-US;q=0.7,en; q=0.3',
			'X-Requested-With': 'XMLHttpRequest'}

	def getCookieSoup(self):
		#print('Acquiring tokens and cookies ...')

		try:
			req1 = requests.get(self.url, timeout=self.timeout, proxies=self.proxy)
		except requests.exceptions.ConnectionError as ex:
			print('[x] Could not make requests, Bad proxy .. Skipping.')
			#print('[x] Reason: {}'.format(ex))
			return False

		except requests.exceptions.ProxyError as ex:
			print('[x] Cannot connect to proxy')
			return False
			
		except requests.exceptions.Timeout as ex:
			print('[x] Time Out error ... Trying again !')
			return False

		if req1.status_code == requests.codes.ok:
			soup = bs4.BeautifulSoup(req1.text, 'html.parser')
			self.soup = soup
			self.cookies = req1.cookies
		else:
			print('[x] Request not successfull. Status Code: {}'.format(req1.status_code))
			return False

		#print(' Done.')
		return True

	def vote(self, option_id):
		
		self.option_id = option_id
		# construct our payload
		self.constructPayload()


		# make the requests
		try:
			req2 = requests.post(self.url, data=self.payload, 
				headers=self.headers, cookies=self.cookies, 
				timeout=self.timeout, proxies=self.proxy)

		except requests.exceptions.ConnectionError as ex:
			print('[x] Could not make requests, Bad proxy .. Skipping.')
			#print('[x] Reason: {}'.format(ex))
			return False

		except requests.exceptions.Timeout as ex:
			print('[x] Time Out error ... Trying again !')
			return False

		except requests.exceptions.ProxyError as ex:
			print('[x] Cannot connect to proxy')
			return False

		if 'success' in req2.text:
			json = req2.json()
			if json['success'] == 'success':
				print('[+] Successfully Voted')
				return True
			else:
				print('[-] Vote not successfull')
				#print(json)
				#threading.lock()
				#VOTE_COUNT += 1
				#threading.unlock()
				return False
		else:
			print('[!] Inspect this.')
			print(req2.text)

	
	def selectProxy(self):
		# select a proxy from the list of proxy.
		try:
			proxy = queue_var.get(False)
		except queue.Empty:
			return None

		print('[*] Using Proxy {}'.format(proxy))

		return {'https': 'http://{}'.format(proxy)}

	def constructPayload(self):
		self.payload = {'security-token': self.loadSecToken(),
			self.loadAuthToken(): '', 
			'options': self.option_id}

	def loadAuthToken(self):
		auth_token = self.soup.find('input', {'id': 'field-authenticity-token'}).get('name')
		if auth_token is not None:
			return auth_token

	def loadSecToken(self):
		sec_token = self.soup.find('input', {'name': 'security-token'}).get('value')
		if sec_token is not None:
			return sec_token

	def loadOptionID(self):
		all_options = []
		options = self.soup.find_all('input', {'name': 'options'})
		for option in options:
			oid = option.get('value')
			if oid is not None:
				all_options.append(oid)
		return all_options

# ####
def loadProxy():
	# check if the file exists
	if not os.path.exists(StrawPoll.PROXY_FILE):
		print('[x] Proxy file does not exists.')
		exit_()

	proxies = []
	with open(StrawPoll.PROXY_FILE) as handle:
		for line in handle:
			proxy = line.strip().split('#')[0]
			proxies.append(proxy)
	print('Loaded {} proxies.'.format(len(proxies)))
	return proxies

def loadOptions(poll_id):
	# the options id also known as oid is fetched here.
	print('Loading Options ...', end='')

	url = 'https://www.strawpoll.me/{}'.format(poll_id)
	req = requests.get(url, timeout=20)
	if req.status_code == requests.codes.ok:
		soup = bs4.BeautifulSoup(req.text, 'html.parser')
		
	else:
		print('[!] Could not load options')
		print('[x] Request not successfull. Status Code: {}'.format(req.status_code))
		return

	print('Done.')

	# extract the oid's here ..
	all_options = []
	options = soup.find_all('input', {'name': 'options'})

	for option in options:
		oid = option.get('value')
		if oid is not None:
			all_options.append(oid)
	return all_options

def exit_():
	print()
	input('Press <enter> to exit')
	exit()

if __name__ == '__main__': 
	# get the poll id from the user
	while  True:
	
		try:
			poll_id = str(input('Enter Poll ID: '))
		except ValueError:
			print('Invalid Poll ID entered!, Try Again!')
			continue
		else:
			break


	POLL_ID = poll_id

	# counter for number of vote found, default 0
	VOTE_COUNT = 0

	# load the options available
	OPTIONS = loadOptions(POLL_ID)

	# get the option index
	print('\nEnter Option Index between 1 - {}'.format(len(OPTIONS)))
	while True:
		try:
			option_index = int(input('Enter Option index: '))
		except ValueError:
			print('\nInvalid Index Option entered!, Try Again!')
			continue
		else:
			if option_index > len(OPTIONS):
				print('\n[x] Index Entered is greater than available number of index')
				print('Try Again!\n')
				continue
			elif option_index <= 0:
				print('\n[x] Can\'t use an index less than or equal 0')
				print('Try Again!\n')
				continue
			break

	# select the optino to use .
	OPTION_ID = OPTIONS[option_index-1]
	print('Option ID: {}'.format(OPTION_ID))
	all_straw = []

	# use a queue ..
	queue_var = queue.Queue()

	# load the proxy from file
	PROXIES = loadProxy()

	# load the proxy into the queue
	for proxy in PROXIES:
		queue_var.put(proxy)

	print('-'*30)
	print('Starting up ...')
	print('-'*30)
	time.sleep(5)
	# get into a forverver loop
	while True:
		# initiate an instance
		straw = StrawPoll(POLL_ID)
		# we aren't able to use the proxy
		if not straw.status:
			break
		# launch the vote
		straw.start()
		all_straw.append(straw)

	# wait for every other thread to finish
	for straw in all_straw:
		straw.join()

	# clean up
	print('Vote Count: {}'.format(VOTE_COUNT))
	exit_()