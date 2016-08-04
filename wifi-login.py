#!/usr/bin/env python

from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from configparser import ConfigParser
from os.path import expanduser
from os.path import join as pathjoin

# Never check any hostnames

class HostNameIgnoringAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       assert_hostname=False)

if __name__ == '__main__':
	postdata = {
		'password':      'accesscode',
		'buttonClicked': '4',
		'redirect_url':  '',
		'err_flag':      '0',
		'info_flag':     '0',
		'info_msg':      '0',
		'terms':         'checkbox' }

	config = ConfigParser()
	home = expanduser("~")
	config_file = pathjoin(home, '.config', 'login-stockholm.ini')		
	try:
		config.read(config_file)
		postdata['username'] = config['global']['login']
		host = config['global']['host']
	except IOError:
		pass

	s = Session()
	s.mount(host, HostNameIgnoringAdapter())
	r = s.post(host, data = postdata)

	if 'Login Successful' in r.content.decode('utf-8'):
		print('Logged in to wi-fi')
	else:
		print('Already logged in/login failed')

