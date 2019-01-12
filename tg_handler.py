# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 17:55:59 2019

@author: Mikko Impiö
"""
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config['TOKENS']['TOKEN']


# INIT
from telegram.ext import Updater
from telegram.ext import CommandHandler
import telegram
import logging
from nfclogger import NFCLogger

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

db = NFCLogger()

count = 0


    
# DISPATCH
class TGHandler():
    def __init__(self):
        # TGbot initializations
        self.updater = Updater(token=TOKEN)
        self.dp = self.updater.dispatcher
        
        
        start_handler = CommandHandler('start', self.start)
        osaavaa_handler = CommandHandler('osaavaa', self.osaavaa)
        cnt_handler = CommandHandler('count',self.counter)
        cardinfo_handler = CommandHandler('cardinfo',self.cardinfo)
        readcard_handler = CommandHandler('readcard',self.readcard)
        newuser_handler = CommandHandler('newuser',self.newuser)
        logout_handler = CommandHandler('logout',self.logout)
        people_handler = CommandHandler('people',self.people)
        
        
        self.dp.add_handler(start_handler)
        self.dp.add_handler(osaavaa_handler)
        self.dp.add_handler(cnt_handler)
        self.dp.add_handler(cardinfo_handler)
        self.dp.add_handler(readcard_handler)
        self.dp.add_handler(newuser_handler)
        self.dp.add_handler(logout_handler)
        self.dp.add_handler(people_handler)
        
        
        self.dp.add_error_handler(self.error)
        
        self.updater.start_polling()
         
        # other variables
        self.current_card_state = False
        self.current_card_ID = ''
        
    # private functions
    def __add_ID(self,cardID):
        pass
        
    def __log_user(self, cardID):
        pass
    
    def __set_current_card_state(self, card_state):
        self.current_card_state = card_state
    
    # NFC public interface
    def set_current_card_ID(self, cardID):
        self.current_card_ID = cardID
        if cardID == 'No card':
            self.__set_current_card_state(False)
        else:
            self.__set_current_card_state(True)
            
        if db.is_user(cardID):
            userid = db.get_userid(cardID)
            if not db.is_logged_in(cardID):
                db.timer_login(cardID)
                self.send_login_confirmation(userid)
            else:
                pass
            

    # TG public interface random functions
    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
           
    def osaavaa(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="osaavaa")
   
    def counter(self, bot, update):
        global count
        count += 1
        bot.send_message(chat_id=update.message.chat_id, text=str(count))
        
        
    ## TG public interface NFC functions
    def cardinfo(self, bot, update):
        msg = 'Card present: {} \n\n Card ID: {}'.format(self.current_card_state,self.current_card_ID) 
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        
    def readcard(self, bot, update):
        print(update.message.from_user)
        cardID = self.current_card_ID
        msg = ''
        
        if db.is_user(cardID):
            username = db.get_username(cardID)
            msg = 'Card belongs to user: ' + username
        else:
            msg = 'No user for this card. Create new user with /newuser'
            
        bot.send_message(chat_id=update.message.chat_id, text=msg)
           
    def newuser(self, bot, update):
        user = update.message.from_user
        cardID = self.current_card_ID
        
        if self.current_card_state:
            if db.is_user(cardID):
                bot.send_message(chat_id=update.message.chat_id, text="Card already exists")
            else:
                db.add_ID(cardID,user)
                bot.send_message(chat_id=update.message.chat_id, text="User "+user['username']+" added")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="No card present")
            
    ## TG public interface functions not requiring NFC
            
    def logout(self, bot, update):
        user = update.message.from_user
        userid = user['id']
        cardID = db.get_cardID(userid)
        
        if db.is_logged_in(cardID):
            db.timer_logout(cardID)
            self.send_logout_confirmation(userid)
        else:
            self.send_message(userid, 'Already logged out')
            
    def people(self, bot, update):
        currently_in = db.currently_logged_in()
        txt = ""
        for u in currently_in:
            txt = txt+u+"\n"
        bot.send_message(chat_id=update.message.chat_id, text=txt)
        
            
    ## TG from bot to user functions
    def send_login_confirmation(self,userid):
        bot = telegram.Bot(token=TOKEN)
        bot.send_message(chat_id= userid, text="Logged in")
        
    def send_logout_confirmation(self,userid):
        bot = telegram.Bot(token=TOKEN)
        bot.send_message(chat_id= userid, text="Logged out")
        
    def send_message(self,userid, message):
        bot = telegram.Bot(token=TOKEN)
        bot.send_message(chat_id= userid, text=message)
    
    # Errors
    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)
        
    