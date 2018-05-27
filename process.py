'''
Usage:
python3 process.py [directory]

Notes:
https://superuser.com/questions/519649/tool-to-bulk-speed-up-convert-an-audio-file

Bpm tools:
http://manpages.ubuntu.com/manpages/trusty/man1/bpm.1.html

Sox documentation:
http://sox.sourceforge.net/sox.html

Detect BPM:
sox 01.mp3 -t raw -r 44100 -e float -c 1 - | bpm

Change tempo:
sox 01.mp3 -C 320 02.mp3 tempo 1.1

'''
import os, sys
from os import listdir
from os.path import isfile, join
import subprocess

import mutagen.id3
from mutagen.mp3 import MP3

from shutil import copyfile


if len(sys.argv) == 1:
	print("Usage info.py [directory_name]")
	sys.exit()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

mypath = sys.argv[1]

runUpdateTempo = True

if not os.path.isdir(mypath):
	print("directory " + mypath + " not found")
	sys.exit()

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for f in onlyfiles:
	filename, file_extension = os.path.splitext(mypath + "/" + f)
	if file_extension == ".mp3":
		print (bcolors.HEADER + f + bcolors.ENDC)
		ff = mypath + f;
		ffc = filename + "_174" + file_extension;

		audio = mutagen.File(ff)

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
			info['year'] = str(audio['TDRC'].text[0])
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


		print ("\t" + info["author"] + " - " + info["title"] + " (" + info["label"] + ", " + info["year"] + ")")		
		print ("\t" + info["url"] + ", " +info["album_url"] + ", " +info["code"])
		print ("\tkey:" + info["key"])

		originalBpm = float(info["bpm"]);
		bpm = 0;
		cmd = subprocess.Popen('sox -V1 '+ ff +' -t raw -r 44100 -e float -c 1 - | bpm', shell=True, stdout=subprocess.PIPE)
		for i, line in enumerate(cmd.stdout):
			if i == 0:
				bpm = float(line.decode("utf-8"))
		

		if originalBpm < 90:
			originalBpm *= 2;
		if bpm < 90:
			bpm *= 2;

		match = originalBpm / bpm * 100;

		print("\torignalBpm: " + str(originalBpm) + ", detected bpm: " + str(bpm) + ", match: " + str(match) + "%")

		usableBpm = 0
		if originalBpm > 160:
			usableBpm = originalBpm
		elif bpm > 160:
			usableBpm = bpm

		if usableBpm > 0:
			tempoUpdate = float("{0:.12f}".format(174 / usableBpm))
			print(bcolors.OKGREEN + "\ttempoUpdate: " + str(tempoUpdate) + bcolors.ENDC)

			needsUpdate = False
			if int(tempoUpdate * 10000) != 10000:
				print("\t" + bcolors.WARNING + "needs tempo update" +bcolors.ENDC)
				needsUpdate = True
			else:
				print("\t" + bcolors.OKGREEN + "doesnt need tempo update" +bcolors.ENDC)


			skip = False
			if filename.endswith("_174"):
				skip = True
				print("\tprocessed file, skipping")
			if os.path.isfile(ffc):
				skip = True
				print("\tfile already processed as " + ffc)

			if not skip and not needsUpdate and runUpdateTempo:
				copyfile(ff, ffc)

			if not skip and needsUpdate and runUpdateTempo:
				cmd = subprocess.Popen('sox -V1 ' + ff +' -C 320 ' + ffc + ' tempo ' + str(tempoUpdate), shell=True, stdout=subprocess.PIPE)
				cmd.wait()

				source = mutagen.File(ff)

				mp3 = MP3(ffc)
				if mp3.tags is None:
				    mp3.add_tags()

				tags = mp3.tags
				tags.add(source['TIT2'])
				tags.add(source['TKEY'])
				tags.add(source['TBPM'])
				tags.add(source['TKEY'])
				tags.add(source['TPE1'])
				tags.add(source['TPUB'])
				tags.add(source['TALB'])
				tags.add(source['TDRC'])
				tags.add(source['WOAF'])
				tags.add(source['WPUB'])
				tags.add(source['TSRC'])

				mp3.save()

				newBpm = 0
				cmd = subprocess.Popen('sox -V1 '+ ffc +' -t raw -r 44100 -e float -c 1 - | bpm', shell=True, stdout=subprocess.PIPE)
				for i, line in enumerate(cmd.stdout):
					if i == 0:
						newBpm = float(line.decode("utf-8"))
				if newBpm < 90:
					newBpm *= 2
				print(bcolors.OKGREEN + "\t" + ffc + ", bpm: "+ str(newBpm) + bcolors.ENDC)

		else:
			print(bcolors.FAIL + "\tunable to find correct bpm" + bcolors.ENDC)


		print("\n")