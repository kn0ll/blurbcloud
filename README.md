# blurbcloud

a script that remixes SoundCloud songs by incessantly overlaying SoundCloud
comments over the original audio.

## configure

set your SoundCloud client_id in blurb.py and the track_url of the track you
would like to blurb. requires you have `say` command available, which is used
to turn comments into audible speech.

## use

```
python blurb.py
```

this will create a few files; `tmp/combined.wav` is the final output.

## todo

- beatmatching
- autotuning
