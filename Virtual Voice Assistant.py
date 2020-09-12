#author
#Viswamber Prasad
#viswamberprasad21@gmail.com

import wolframalpha
import wikipedia
import smtplib
import pyttsx3
import speech_recognition as sr  
import time
import datetime
import requests
import json
from bs4 import BeautifulSoup
import webbrowser
import re
import string
from translate import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#function to scrape,parse and return the temperature,precipitation
def temperature():
  url='https://rb.gy/bqqq92'
  headr={}#"User-Agent" header for your HTTP requests.
	page=requests.get(url,headers=headr)
	soup=BeautifulSoup(page.content,'html.parser')
	temp=soup.find(id="wob_tm").get_text().strip().encode('ascii', 'ignore').decode('ascii')
	precipitaion=soup.find(id="wob_pp").get_text().strip().encode('ascii', 'ignore').decode('ascii')
	return temp,precipitaion

def sentiment_analysis(statement):
	#removing static characters from the input statement
  cleaned_text=statement.lower().translate(str.maketrans('','',string.punctuation))
	#tallying the emotional score
  emotion_tally=SentimentIntensityAnalyzer().polarity_scores(cleaned_text)
	negative_emotion=emotion_tally['neg']
	positive_emotion=emotion_tally['pos']
	neutral=emotion_tally['neu']
	emotion=''
	if neg>pos:
		emotion='negative'
	elif pos>neg:
		emotion='positive'
	else:
		emotion='neutral'
	return emotion
	emotion=sentiment_analysis()		

#function to extract only the required question
def wolframalapha_question_parse(wolf_question):
	if len(wolf_question)>=6:
		answer=''.join(numb.split()[2:])
	return answer
	answer=wolframalapha_question_parse()	


def talk(command):
	#MicroSoft SAPI5 engine
  engine=pyttsx3.init('sapi5')
  voices = engine.getProperty('voices')
  #set voices[] to voices[1] for female voice
	engine.setProperty('voice', voices[0].id)
	#setting rate of speech
  engine.setProperty('rate', 130)
	engine.say(command)
	engine.runAndWait()

def lis_ten():
	r=sr.Recognizer()
	with sr.Microphone() as source:
		print('Assistant is listening')
		#adjusts to the environment's audio
    r.pause_threshold=1
		#adjusts to the background noise
    r.adjust_for_ambient_noise(source)
		audio=r.listen(source)
	try:
		global task
		task=r.recognize_google(audio).lower()
		print('you said: '+command+'\n')
	except sr.UnknownValueError:
		talk(" I didn't catch that,Could You Please repeat?")
		print('Could not understand,repeat')
		#listens again
    lis_ten()
		time.sleep(2)
	except sr.RequestError as e:
		print("Could not request results; {0}".format(e))
		talk("Unknown Error has Occured!")
	return task
	task=lis_ten()

def main_func(command):
	global listening
  #when listening is false,execution stops
	if 'hello' or 'hi' in task:
		listening=True
		talk('hello! how can i help you today?')
	elif 'how are you' in task:
		listening=True
		talk('I am good,hope you are too!')
	elif 'what is' in task:
		listening=True
		try:
			ap_id=''#your WolframAlpha API key
			ques=wolframalapha_question_parse(task)
			talk('Computing'+ques)
			client=wolframalpha.Client(ap_id)
			result=client.query(ques)
			ans=next(result.results).text
			talk('The Answer is '+ans)
			print('The Answer is: '+str(ans))
		except:
			talk('something went wrong')
			print('Unknown Error Occured!')	
	elif 'time' in task:
		listening=True
		t=time.localtime()
		current_time=time.strftime("%H:%M:%S",t)
		#assembling the time,in desired format
    hour=current_time[:2]
		minute=current_time[3:5:]
		second=current_time[6:]
		talk(f'the time now is,{hour}hours,{minute}minutes and {second}seconds')
		print(current_time)
	elif 'date' in task:
		listening=True
		current_date=datetime.datetime.now()
		talk(f'the date today is,{str(current_date.day)}{str(current_date.month)}{str(current_date.year)}')
		print(str(current_date.day)+'/'+str(current_date.month)+'/'+str(current_date.year))	
	elif 'corona virus' in task:	
		#computes the total corona virus cases,and the number of cases recorded today
    #returns result in JSON 
    listening=True
		try:
			api_req=requests.get("")#API key
			stat=json.loads(api_req.content)
			cases=stat["cases"]
			tod_cases=stat["todayCases"]
			talk(f'The total corona virus cases in India is{str(cases)},the number of cases recorded today {str(tod_cases)} ')
			print('total cases: '+str(cases)+' today cases: '+str(tod_cases))
		except Exception as e:
			stat='Error...'
			print(stat)
	elif 'translate' in task:
		talk('tell me the word or sentence,that i have to translate')
		to_trans=lis_ten()
		talk('to which language,should i translate it?')
		lang=lis_ten()
		translator=Translator(from_lang='English',to_lang=lang)
		trans_output=translator.translate(to_trans)
		print('translating...')
		print('the translated text: '+trans_output)
		talk(trans_output)
	elif 'open' in task:
		#opens the required webpage
    listening=True
		if command.split()[1]=='google':
			talk('opening google')
			webbrowser.open('https://www.google.co.in/')
		elif command.split()[1]=='youtube':
			talk('opening youtube') 
			webbrowser.open('https://www.youtube.com/')
		else:
			s=command.split()[1]
			talk('opening'+s)
			webbrowser.open('https://www.'+s+'.com/')					
	elif 'emotion analysis' in task:
		talk('okay!tell me the first five words that come to your mind')
		emo=lis_ten()
		print('analysing your emotion...')
		score=sentiment_analysis(emo)
		if score=='positive':
			print('emotional analysis positivity score: '+str(pos))
			talk('your emotion is positive')
		elif score=='negative':
			print('emotional analysis negativity score: '+str(neg))
			talk('your emotion is negative')
		else:
			print('emotional analysis score is: NEUTRAL')
			talk('your emotion is neutral')		
	elif 'email' in task:
		listening=True
		talk('What is the subject?')
		subject=lis_ten()
		talk('What should I say?')
		body=lis_ten()	
		talk('To Whom should I send it?')
		receiver_mail_id=lis_ten()
		smtp_obj=smtplib.SMTP('')
		smtp_obj.ehlo()
		smtp_obj.starttls()
		app_password=''
		sender_mail_id=''
		smtp_obj.login(sender_mail_id,app_password)
		from_add=sender_mail_id
		to_add=receiver_mail_id
		msg='Subject: '+subject+'\n'+body
		try:
			smtp_obj.sendmail(from_add,to_add,msg)
			smtp_obj.quit()
			talk('Email sent!')
		except:
			print('Error Occured!')
			talk('Email not sent')
	elif 'stop' in task:
		listening=False
	else:
		#default search up in wikipedia
		listening=True
		try:
			summry=str(wikipedia.summary(str(command),sentences=2))
			talk(summry)
			print(summry)
		except:
			talk('I did not quite understand that!')
			print('not understood')
	return listening
	listening=main_func()	 				

		
#a continous loop for the		
#Execution of assistant and wake word activation
while True:
	main_mic=sr.Recognizer()
	wake_word=''
	with sr.Microphone() as source:
		try:
			main_mic.pause_threshold=1
			main_mic.adjust_for_ambient_noise(source)
			audio=main_mic.listen(source)
			hotword=main_mic.recognize_google(audio).lower()
		except sr.UnknownValueError:
			#to continue listening,until the hotword is recognised
			continue	
		reg_ex=re.search(wake_word,hotword)
		temp_today,expected_precipitation=temperature()
		if reg_ex:
			talk('Activated!')
			talk('Welcome!')
			talk('the temperature today is'+temp_today+'degree celsius')
			talk('the expected precipitation today is'+expected_precipitation)
			listening=True
			while listening==True:
				main_func(lis_ten())
				
	



