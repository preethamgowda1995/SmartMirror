#import files
from tkinter import *
from urllib.request import *
import requests
from PIL import Image,ImageTk
from json import load
import random
import imaplib
import email
import feedparser
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(13,GPIO.OUT)

#functions
def get_ip():
	try:
		ip = urlopen('http://ip.42.pl/raw').read().decode('utf-8')
		return ip
	except Exception as e:
		print("cannot get ip %s"%(e))
#print(get_ip())

#Function for Gmail
def gmail():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username,password)
    mail.select("inbox")
    result,data = mail.uid("search",None,"ALL")
    inbox_item = data[0].split()
    FROMS = []
    SUBJECTS = []
    for i in range(-3, 0):
        message = inbox_item[i]
        result2, email_Data = mail.uid("fetch", message, "(RFC822)")
        raw_email = email_Data[0][1].decode('utf-8')
        email_message = email.message_from_string(raw_email)
        FROMS.append(email_message['From'])
        SUBJECTS.append(email_message['Subject'])
    From1.configure(text="From : "+FROMS[0].split(' ')[0])
    #print(FROMS)
    From2.configure(text="From : "+FROMS[1].split(' ')[0])
    From3.configure(text="From : "+FROMS[2].split(' ')[0])
    Subject1.configure(text="Subject : "+SUBJECTS[0])
    Subject2.configure(text="Subject : "+SUBJECTS[1])
    Subject3.configure(text="Subject :"+SUBJECTS[2])

#Funtion for time
def getTime():
	value = time.strftime("%H:%M:%S")
	time_label.config(text=value)
	root.after(200,getTime)

#Function for NEws
def neWS():
	results = feedparser.parse("https://timesofindia.indiatimes.com/rssfeedstopstories.cms")
	Titles = []
	GMT = []
	for values in results.entries:
		Titles.append(values.title)
		GMT.append(values.published)
	Title1.configure(text=Titles[0])
	GMT1.configure(text=GMT[0])
	Title2.configure(text=Titles[1])
	GMT2.configure(text=GMT[1])
	Title3.configure(text=Titles[2])
	GMT3.configure(text=GMT[2])
	Title4.configure(text=Titles[3])
	GMT4.configure(text=GMT[3])
	Title5.configure(text=Titles[4])
	GMT5.configure(text=GMT[4])
	root.after(5000,neWS)

#Function to get HeartRate
def HeartRate():
	with open("HeartRate/hearrate.txt","r") as r:
		h_values = r.read()
		h_Rate.configure(text=h_values)
	root.after(1000,HeartRate)
			

def get_weather():
        ip_address =get_ip()
        result = Weather_api_token+ip_address
        json_data = requests.get(result).json()
        temperature = str(json_data[u'current'][u'temp_c'])
        TemperatureLabel.configure(text=temperature+degreesign+"C")
        location = json_data[u'location'][u'name']
        Citylabel.configure(text=location)
        icontext1 = json_data[u'current'][u'condition'][u'code']
        icontext = None
        if icontext1 in icon_lookup:
            icontext = icon_lookup[icontext1]
        if icontext is not None:
            if icontext1!=icontext:
                icontext1 = icontext
                Typeof.config(text=icontext1)
        else:
            Typeof.config(text="")
        iconImage = str(json_data[u'current'][u'condition'][u'icon']).split("4/")
        Icon_value = iconImage[-1]
        if Icon_value is not None:
            if iconImage!=Icon_value:
                iconImage = Icon_value
                image = Image.open(Icon_value)
                photo = ImageTk.PhotoImage(image)
                iconLb.config(image=photo)
                iconLb.image = photo
        else:
            iconLb.config(image='')

def show():
	with open("Ultrasonic/Values.txt","r") as f:
		contents = f.read()
		try:
			value = int(contents)
		except ValueError:
			value = 0
		
		if value<150:
			frame1.tkraise()
			try:
				with open("ldrdata.txt","r") as f:
					value = f.read()
				if int(value)==1:
					GPIO.output(13,GPIO.HIGH)
				else:
					GPIO.output(13,GPIO.LOW)
			except ValueError:
				pass
		else:
			GPIO.output(13,GPIO.LOW)
			frame2.tkraise()
	root.after(2000,show)


#icon dictionary
icon_lookup = {

    1000:"Clear",
    1003:"Partly Cloudy",
    1006:"Cloudy",
    1009:"Overcast",
    1030:"Mist",
    1063:"Patchy rain possible",
    1066:"Patchy snow possible",
    1069:"Patchy sleet possible",
    1072:"Patchy freezing drizzle possible",
    1087:"Thundery outbreaks possible",
    1114:"Blowing snow",
    1117:"Blizzard",
    1135:"Fog",
    1147:"Freezing fog",
    1150:"Patchy light drizzle",
    1153:"Light drizzle",
    1168:"Freezing drizzle",
    1171:"Heavy freezing drizzle",
    1180:"Patchy light rain",
    1183:"Light rain",
    1186:"Moderate rain at times",
    1189:"Moderate rain",
    1192:"Heavy rain at times",
    1195:"Heavy rain",
    1198:"Light freezing rain",
    1201:"Moderate or heavy freezing rain",
    1204:"Light sleet",
    1207:"Moderate or heavy sleet",
    1210:"Patchy light snow",
    1213:"Light snow",
    1216:"Patchy moderate snow",
    1219:"Moderate snow",
    1222:"Patchy heavy snow",
    1225:"Heavy snow",
    1237:"Ice pellets",
    1240:"Light rain shower",
    1243:"Moderate or heavy rain shower",
    1246:"Torrential rain shower",
    1249:"Light sleet showers",
    1252:"Moderate or heavy snow showers",
    1255:"Light snow showers",
    1258:"Moderate or heavy snow showers",
    1261:"Light showers of ice pellets",
    1264:"Moderate or heavy showers of ice pellets",
    1273:"Patchy light rain with thunder",
    1276:"Moderate or heavy rain with thunder",
    1279:"Patchy light snow with thunder",
    1282:"Moderate or heavy snow with thunder"
}

#variables
count = 0
degreesign= u"\xb0"
Weather_api_token = 'http://api.apixu.com/v1/current.json?key=b9d137cbec0a43fab9d145931182201&q='
username = "preethamgowda0395@gmail.com"
password = "123234345"


#mainwindow
root = Tk()
root.attributes("-fullscreen",True)

#first frame
container = Frame(root)
container.pack(side=TOP,fill="both",expand=True)
container.grid_rowconfigure(0,weight=1)
container.grid_columnconfigure(0,weight=1)

#secondframe
frame1 = Frame(container,bg='black')
frame1.grid(row=0,column=0,sticky="nsew")


#second frame attributes
TemperatureLabel = Label(frame1,font=("Helvetica", 30),fg='white',bg='black')
TemperatureLabel.place(x=200,y=100)
iconLb = Label(frame1,bg='black')
iconLb.place(x=100,y=100)
Citylabel = Label(frame1,font=("Helvetica",20),fg='white',bg='black')
Citylabel.place(x=100,y=150)
Typeof = Label(frame1,font=("Helvetica",20),fg='white',bg='black')
Typeof.place(x=100,y=200)


#frame Heart Icon
Heart_image = Image.open("Images/Heart.png")
Heart_photo = ImageTk.PhotoImage(Heart_image)
Heart_icon = Label(frame1,bg='black',fg='white',image=Heart_photo)
Heart_icon.place(x=100,y=350)

#frame Hear rate
h_Rate = Label(frame1,bg='black',fg='white',font=("Helvetica",25))
h_Rate.place(x=200,y=350)

#frame attributes for gmailicon
g_image = Image.open("Images/Gmail.png")
g_photo = ImageTk.PhotoImage(g_image)
gmail_icon = Label(frame1,bg='black',text="hello",fg='white',image=g_photo)
gmail_icon.place(x=1000,y=100)

#frame attributes for mail
From1 = Label(frame1,bg='black',fg='white',font=("Helvetica",15))
From1.place(x=1100,y=100)
From2 = Label(frame1,bg='black',fg='white',font=("Helvetica",15))
From2.place(x=1100,y=160)
From3 = Label(frame1,bg='black',fg='white',font=("Helvetica",15))
From3.place(x=1100,y=220)
Subject1 = Label(frame1,bg='black',fg='white',font=("Helvetica",15))
Subject1.place(x=1100,y=130)
Subject2 = Label(frame1,bg='black',fg='white',font=("Helvetica",15))
Subject2.place(x=1100,y=190)
Subject3 = Label(frame1,bg='black',fg='white',font=("Helvetica",15))
Subject3.place(x=1100,y=250)

#Frame attributes for News Icon
News_image = Image.open("Images/News.png")
News_photo = ImageTk.PhotoImage(News_image)
News_icon = Label(frame1,bg='black',text="hello",fg='white',image=News_photo)
News_icon.place(x=100,y=600)



#frame attributes for News TItle
Title1 = Label(frame1,bg='black',fg='white',font=("Helvetica",13),wraplength=800)
Title1.place(x=200,y=600)
Title2 = Label(frame1,bg='black',fg='white',font=("Helvetica",13),wraplength=800)
Title2.place(x=200,y=650)
Title3 = Label(frame1,bg='black',fg='white',font=("Helvetica",13),wraplength=800)
Title3.place(x=200,y=700)
Title4 = Label(frame1,bg='black',fg='white',font=("Helvetica",13),wraplength=800)
Title4.place(x=200,y=750)
Title5 = Label(frame1,bg='black',fg='white',font=("Helvetica",13),wraplength=800)
Title5.place(x=200,y=800)


#frame attributes for News GMT
GMT1 = Label(frame1,bg='black',fg='white',font=("Helvetica",13))
GMT1.place(x=1100,y=600)
GMT2 = Label(frame1,bg='black',fg='white',font=("Helvetica",13))
GMT2.place(x=1100,y=650)
GMT3 = Label(frame1,bg='black',fg='white',font=("Helvetica",13))
GMT3.place(x=1100,y=700)
GMT4 = Label(frame1,bg='black',fg='white',font=("Helvetica",13))
GMT4.place(x=1100,y=750)
GMT5 = Label(frame1,bg='black',fg='white',font=("Helvetica",13))
GMT5.place(x=1100,y=800)

#label for time
time_label = Label(frame1,bg='black',fg='white',font=("Helvetica",30))
time_label.place(x=1100,y=350)


#third frame
frame2 = Frame(container,bg='black')
frame2.grid(row=0,column=0,sticky="nsew")

#thirdframe attributes
label2 = Label(frame2,bg='black',fg='white')
label2.pack(side=TOP,anchor=E)


getTime()
get_weather()
gmail()
HeartRate()
neWS()
show()

root.mainloop()
