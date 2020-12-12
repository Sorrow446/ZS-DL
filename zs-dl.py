#!/usr/bin/env python3

import os
import re
import sys
import json
import time
import argparse
import traceback
try:
	from urllib.parse import unquote
except ImportError:
	from urllib import unquote

import requests
from tqdm import tqdm



def read_txt(abs):
	with open(abs) as f:
		return [u.strip() for u in f.readlines()]

def decrypt_dlc(abs):
	# Thank you, dcrypt owner(s).
	url = "http://dcrypt.it/decrypt/paste"
	r = s.post(url, data={
			'content': open(abs)
		}
	)
	r.raise_for_status()
	j = json.loads(r.text)
	if not j.get('success'):
		raise Exception(j)
	return j['success']['links']

def parse_prefs():
	out_path = os.path.join(os.getcwd(), 'ZS-DL downloads')
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-u', '--urls', 
		nargs='+', required=True,
		help='URLs separated by a space or an abs path to a txt file.'
	)
	parser.add_argument(
		'-o', '--output-path',
		default=out_path,
		help='Abs output directory.'
	)
	parser.add_argument(
		'-ov', '--overwrite',
		action='store_true',
		help='Overwrite file if already exists.'
	)
	parser.add_argument(
		'-p', '--proxy',
		help='HTTPS only. <IP>:<port>.'
	)
	args = parser.parse_args()
	if args.urls[0].endswith('.txt'):
		args.urls = read_txt(args.urls[0])
	for url in args.urls:
		if url.endswith('.dlc'):
			print("Processing DLC container: " + url)
			try:
				args.urls = args.urls + decrypt_dlc(url)
			except Exception as e:
				err("Failed to decrypt DLC container: " + url)
			args.urls.remove(url)
			time.sleep(1)
	return args

def dir_setup():
	if not os.path.isdir(cfg.output_path):
		os.makedirs(cfg.output_path)

def err(txt):
	print(txt)
	traceback.print_exc()
	
def set_proxy():
	s.proxies.update({'https': 'https://' + cfg.proxy})
	
def check_url(url):
	regex = r'https://www(\d{1,3}).zippyshare.com/v/([a-zA-Z\d]{8})/file.html'
	match = re.match(regex, url)
	if match:
		return match.group(1), match.group(2)
	raise ValueError("Invalid URL: " + str(url))

def extract(url, server, _id):
	regex = (
		r'document.getElementById\(\'dlbutton\'\).href = "/d/[a-zA-Z\d]{8}/" '
		r'\+ \((\d+) % (\d+) \+ (\d+) % (\d+)\) \+ "\/(.+)";'
	)
	for _ in range(3):
		r = s.get(url)
		if r.status_code != 500:
			break
		time.sleep(1)
	r.raise_for_status()
	meta = re.search(regex, r.text)
	if not meta:
		raise Exception('Failed to get file URL. File down or pattern changed.')
	num_1 = int(meta.group(1))
	num_2 = int(meta.group(2))
	num_3 = int(meta.group(3))
	num_4 = int(meta.group(4))
	final_num = num_1 % num_2 + num_3 % num_4
	enc_fname = meta.group(5)
	file_url = "https://www{}.zippyshare.com/d/{}/{}/{}".format(server, _id, final_num, enc_fname)
	return file_url, unquote(enc_fname)

def get_file(ref, url):
	s.headers.update({
		'Range': "bytes=0-",
		'Referer': ref
	})
	r = s.get(url, stream=True)
	del s.headers['Range']
	del s.headers['Referer']
	r.raise_for_status()
	length = int(r.headers['Content-Length'])
	return r, length
	
def download(ref, url, fname):
	print(fname)
	abs = os.path.join(cfg.output_path, fname)
	if os.path.isfile(abs):
		if cfg.overwrite:
			print("File already exists locally. Will overwrite.")
		else:
			print("File already exists locally.")
			return
	r, size = get_file(ref, url)
	with open(abs, 'wb') as f:
		with tqdm(total=size, unit='B',
			unit_scale=True, unit_divisor=1024,
			initial=0, miniters=1) as bar:
				for chunk in r.iter_content(32*1024):
					if chunk:
						f.write(chunk)
						bar.update(len(chunk))

def main(url):
	server, _id = check_url(url)
	file_url, fname = extract(url, server, _id)
	download(url, file_url, fname)

if __name__ == '__main__':
	try:
		if hasattr(sys, 'frozen'):
			os.chdir(os.path.dirname(sys.executable))
		else:
			os.chdir(os.path.dirname(__file__))
	except OSError:
		pass

	s = requests.Session()
	s.headers.update({
		'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
					  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
					  "/75.0.3770.100 Safari/537.36"
	})

	print("""
	 _____ _____     ____  __
	|__   |   __|___|    \|  |
	|   __|__   |___|  |  |  |__
	|_____|_____|   |____/|_____|		 
	""")
	cfg = parse_prefs()
	dir_setup()
	if cfg.proxy:
		set_proxy()
	total = len(cfg.urls)
	for num, url in enumerate(cfg.urls, 1):
		print("\nURL {} of {}:".format(num, total))
		try:
			main(url)
		except Exception as e:
			err('URL failed.')
