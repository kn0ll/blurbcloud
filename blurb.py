import re
import os
import random
import urllib
import urllib2
import soundcloud
import subprocess
from pydub import AudioSegment

client_id = 'your_client_id'
track_url = 'https://soundcloud.com/mizukislastchance/sonic-2-chemical-plant-zone-mizukis-fireside-flip'
num_comments = 22

def get_track(client_id, sc_url):
    client = soundcloud.Client(client_id=client_id)
    track = client.get('/resolve', url=sc_url)
    stream = client.get(track.stream_url, allow_redirects=False)
    mp3 = (urllib2.urlopen(stream.location)).read()
    comments = client.get('/tracks/%s/comments' % (track.id))
    return {
        'track': track,
        'mp3': mp3,
        'comments': comments
    }

def write_file(data, location):
    f = open(location, 'wb')
    f.write(data)

def get_random_comment(comments):
    return random.choice(comments).body

def get_random_comments(comments, count):
    return [comments[i] for i in sorted(random.sample(xrange(len(comments)), count))]

track = get_track(client_id, track_url)

# create dirs
filename = 'tmp/song.mp3'
if not os.path.exists(os.path.dirname(filename)):
    os.makedirs(os.path.dirname(filename))

# create song mp3
write_file(track['mp3'], filename)

# get comments to speechify
comments = get_random_comments(track['comments'], num_comments)

# mix audio
song = AudioSegment.from_mp3('tmp/song.mp3')
combined = song

for comment in comments:
    body = re.sub(r"[^A-Za-z\ ]+", '', comment.body)
    print 'writing comment', body, comment.timestamp
    subprocess.call(['say', '-o', 'tmp/speech.wav', '--data-format=LEF32@22050', body])
    speech = AudioSegment.from_wav('tmp/speech.wav')
    speech = speech.apply_gain(+5.5)
    combined = combined.overlay(speech, position=comment.timestamp)

# write combined wav
combined.export('tmp/combined.wav', format='wav')
