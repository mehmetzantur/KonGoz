# -*- coding: utf-8 -*-
import sys
import os
from gtts import gTTS

# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def tts(text, lang):
	file = gTTS(text = text, lang = lang)
	filename = 'msg.mp3'
	file.save(filename)
	os.system('mpg321 "{0}"'.format(filename))
	os.remove(filename)
	

def SayHello():
	msg = "Merhaba. Benim adım Kongöz. Ben sana kitap okurken yardımcı olmak için geliştirildim."
	tts(msg,"tr")

def SayStart():
	msg = "Şimdi hazır bulunan bir resmi okuyarak deneme yapacağım."
	tts(msg,"tr")

def Alert():
	os.system('mpg321 "{0}"'.format("alert.mp3"))