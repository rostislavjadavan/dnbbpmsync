# dnbbpmsync

Sync drum'n'bass tracks to 174bpm

## process.py

Python3 script that scans directory for mp3 files and try to change tempo to 174bpm. It only works on tracks donwload from Beatport.

Sometimes bpm is not detected correctly so it will try to use bpm from ID3 tag originaly set by Beatport. Also Beatport sometimes detect
wrong bpm. In this case track is left as it is.

_Note:_ It won't overwrite original track. It will make a copy with \_174 suffix.

### Requirements
- pyhon3 with mutagen library
  '''
  brew install python3
  pip3 install mutagen
  '''
- sox
  '''
  brew install sox
  '''
- bpm tools
  '''
  brew install bpm-tools
  '''

### How to use
'''
python3 process.py [directory_path]
'''

### Output

![screenshot][screenshot.png]


## info.py

Python3 script that scans directory for mp3 files and display info based on ID3 tags.