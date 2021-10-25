import gc
gc.collect()
import music
_m=['c6:1','r','c6,1','r','r','r']
def setAlarm(on):
 if on:
  music.play(_m,wait=False,loop=True) 
 else:
  music.stop()
def beep():
 music.pitch(2000,200,wait=False)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
