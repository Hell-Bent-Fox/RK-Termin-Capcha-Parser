from python3_anticaptcha import ImageToTextTask
import requests
from bs4 import BeautifulSoup as BS
import base64
import time
import telebot
import logging
import datetime
import os
os.system('chcp 65001')
logging.basicConfig(filename="main.log",level=logging.INFO)
#Получаем ANTICAPTCHA_KEY из файла
def get_api():
    try:
        file=open("api.txt","r")
        api=file.read()
        logging.info("ANTICAPTCHA_KEY get")
        file.close()
        return api
    except FileNotFoundError:
        logging.error("FileNotFoundError(ANTICAPTCHA_KEY)")
        file=open("api.txt","w")
        file.close()
def captcha(captcha_file):
    result = ImageToTextTask.ImageToTextTask(
        anticaptcha_key=ANTICAPTCHA_KEY, save_format="const"
    ).captcha_handler(captcha_file=captcha_file)
    return (result)
def pars_site(site_ad,month):
    mass_with_date=[]
    headers={'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    session = requests.Session()
    request = session.get(site_ad,headers=headers,verify=False)
    soup = BS(request.content, 'html.parser')
    base64_img=(str(soup.find('div').find('captcha')).split('url')[1].split('"')[0].split("base64,")[1].split("')")[0])
    try:
        base64_img_bytes = base64_img.encode('utf-8')
        name_of_captcha_file='captcha_file.png'
        with open(name_of_captcha_file, 'wb') as file_to_save:
            decoded_image_data = base64.decodebytes(base64_img_bytes)
            file_to_save.write(decoded_image_data)
    except:
        return "Error(Incorrect padding)"
    rez=captcha(name_of_captcha_file)
    logging.info("Get rez captcha")
    if rez['errorId']==0:
        answer=(rez["solution"]["text"])
    elif rez['errorId']==1:
        return "Неверный ключ антикапчи"
    else:
        if rez['errorId']==10:
            return "Пополни баланс антикапчи"
        else:
            return "Error(Captcha error)"
    # add_with_capthca='captchaText=74nen4&rebooking=false&token=&lastname=&firstname=&email=&locationCode=kamp&realmId=539&categoryId=868&openingPeriodId=&date=18.07.2021&dateStr=18.07.2021&action%3Aappointment_showMonth=%D0%92%D0%BF%D0%B5%D1%80%D0%B5%D0%B4'
    if 1 in month:
        add_with_capthca='&rebooking=false&locationCode=kamp&realmId=539&categoryId=868&openingPeriodId=&date=18.07.2021&dateStr=18.07.2021&action%3Aappointment_showMonth=%D0%92%D0%BF%D0%B5%D1%80%D0%B5%D0%B4'
        new_site_ad=(site_ad.split('?')[0]+"?captchaText="+answer+add_with_capthca)
        request = session.get(new_site_ad,headers=headers,verify=False)
        soup = BS(request.content, 'html.parser')
        div_with_inf=soup.find('div',{"class":"wrapper"}).find_all('div',{"style":"width: 100%;"})
        for i in div_with_inf:
            i_split=str(i).split('</div>')
            if len(i_split)>2:
                date_frome_site=i_split[0].split('<h4>')[1].split('</h4>')[0].split('\n')[-2].split(' ')[-1]
                if len([i for i in str(date_frome_site).split('.') if i.isdigit()])==3:
                    mass_with_date.append("Запись на прием возможна: "+date_frome_site)
    if 2 in month:
        add_with_capthca='&rebooking=false&locationCode=kamp&realmId=539&categoryId=868&openingPeriodId=&date=18.08.2021&dateStr=18.08.2021&action%3Aappointment_showMonth=%D0%92%D0%BF%D0%B5%D1%80%D0%B5%D0%B4'
        new_site_ad=(site_ad.split('?')[0]+"?captchaText="+answer+add_with_capthca)
        request = session.get(new_site_ad,headers=headers,verify=False)
        soup = BS(request.content, 'html.parser')
        div_with_inf=soup.find('div',{"class":"wrapper"}).find_all('div',{"style":"width: 100%;"})
        for i in div_with_inf:
            i_split=str(i).split('</div>')
            if len(i_split)>2:
                date_frome_site=i_split[0].split('<h4>')[1].split('</h4>')[0].split('\n')[-2].split(' ')[-1]
                if len([i for i in str(date_frome_site).split('.') if i.isdigit()])==3:
                    mass_with_date.append("Запись на прием возможна: "+date_frome_site)
    logging.info(("Get mass_with_date"+str(mass_with_date)).encode("utf-8"))
    return (mass_with_date)
#Получаем chat_id из файла
def get_chat_id():
    try:
        file=open("chat_id.txt","r")
        chat_id=file.read()
        if chat_id.isdigit()==False:
            logging.error("Invalid chat_id")
            print("Invalid chat_id")
        else:
            logging.info("Chat_id get")
            return chat_id
        file.close()
    except FileNotFoundError:
        logging.error("FileNotFoundError(chat_id)")
        file=open("chat_id.txt","w")
        file.close()
#Получаем токен из файла
def get_token():
    try:
        file=open("token.txt","r")
        token=file.read()
        if ":" not in token:
            logging.error("Invalid token")
            print("Invalid token")
        else:
            if token.split(":")[0].isdigit()==False:
                logging.error("Invalid token")
                print("Invalid token")
            else:
                logging.info("Token get")
                return token
        file.close()
    except FileNotFoundError:
        logging.error("FileNotFoundError(token)")
        file=open("token.txt","w")
        file.close()
ANTICAPTCHA_KEY = str(get_api())
token=get_token()
chat_id=int(get_chat_id())
if ANTICAPTCHA_KEY!='' and token!='' and chat_id!='':
    bot = telebot.TeleBot(token)
    logging.info("BOT start at {}".format(datetime.datetime.now()))
    print("Bot work")
    good=True
    k1=0
    k2=0
    link1='https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kamp&realmId=539&categoryId=868'
    link2='https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=stpe&realmId=384&categoryId=628'
    while good and (k1<10 or k2<10):
        try:
            sleep=False
            if k1<10:
                rez=(pars_site(link1,[1]))
                if type(rez)==str:
                    if rez=='Пополни баланс антикапчи':
                        sending_text='Пополни баланс антикапчи'
                        send_message = bot.send_message(chat_id, text=sending_text)
                        logging.info("Sending successful")
                        good=False
                        bot.send_message(613776549, text=sending_text)
                    elif rez =='Неверный ключ антикапчи':
                        sending_text = 'Неверный ключ антикапчи'
                        send_message = bot.send_message(chat_id, text=sending_text)
                        logging.info("Sending successful")
                        good=False
                        bot.send_message(613776549, text=sending_text)
                elif type(rez)==list:
                    if len(rez)>0:
                        sending_text=rez[0]+'\n'+link1
                        send_message = bot.send_message(chat_id, text=sending_text)
                        logging.info(("Sending successful "+sending_text).encode("utf-8"))
                        k1+=1
                        bot.send_message(613776549,text=sending_text)
                    sleep=True
            if k2<10:
                rez=(pars_site(link2,[1,2]))
                if type(rez)==str:
                    if rez=='Пополни баланс антикапчи':
                        sending_text='Пополни баланс антикапчи'
                        send_message = bot.send_message(chat_id, text=sending_text)
                        logging.info("Sending successful")
                        good=False
                        bot.send_message(613776549, text=sending_text)
                    elif rez =='Неверный ключ антикапчи':
                        sending_text = 'Неверный ключ антикапчи'
                        send_message = bot.send_message(chat_id, text=sending_text)
                        logging.info("Sending successful")
                        good=False
                        bot.send_message(613776549, text=sending_text)
                elif type(rez)==list:
                    if len(rez)>0:
                        sending_text=rez[0]+'\n'+link2
                        send_message = bot.send_message(chat_id, text=sending_text)
                        logging.info(("Sending successful "+sending_text).encode("utf-8"))
                        k2+=1
                        bot.send_message(613776549, text=sending_text)
                    sleep=True
            if sleep==True:
                time.sleep(60*10)
        except Exception as e:
            logging.error(str(e))
else:
    print("Error with data")
    logging.info("Error with data")