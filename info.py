'''
Display ID3 tags

Usage:
python3 process.py [directory]

'''
import os, sys
from os import listdir
from os.path import isfile, join
import subprocess

import mutagen.id3
from mutagen.mp3 import MP3

if len(sys.argv) == 1:
	print("Usage info.py [directory_name]")
	sys.exit()

mypath = sys.argv[1]

if not os.path.isdir(mypath):
	print("directory " + mypath + " not found")
	sys.exit()

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for f in onlyfiles:
	filename, file_extension = os.path.splitext(mypath + "/" + f)
	if file_extension == ".mp3":
		print (f)
		audio = mutagen.File(mypath + "/" + f)

		info = {
			"author": "unknown",
			"title": "unknown",
			"label": "unknown",
			"year": "unknown",
			"bpm": 0,
			"key": "unknown",
			"url": "unknown",
			"album_url": "unknown",
			"code": "unknown",
		}
		if "TPE1" in audio:
			info['author'] = audio['TPE1'].text[0]
		if "TIT2" in audio:
			info['title'] = audio['TIT2'].text[0]
		if "TPUB" in audio:
			info['label'] = audio['TPUB'].text[0]
		if "TDRC" in audio:
			info['year'] = audio['TDRC'].text[0]
		if "TBPM" in audio:
			info['bpm'] = audio['TBPM'].text[0]
		if "TKEY" in audio:
			info['key'] = audio['TKEY'].text[0]
		if "WOAF" in audio:
			info['url'] = audio['WOAF'].url
		if "WPUB" in audio:
			info['album_url'] = audio['WPUB'].url
		if "TSRC" in audio:
			info['code'] = audio['TSRC'].text[0]

		print(info)