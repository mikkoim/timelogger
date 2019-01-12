# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 19:07:59 2019

@author: Mikko Impiö
"""

import pandas as pd
import os
from timestamp_handler import TimeStampHandler

LOGOUT_INTERVAL = 3600 # minimum seconds between logs

def my_readcsv(fname):
    df = pd.read_csv(fname)
    df = df.set_index('cardID')
    return df

class NFCLogger():
    def __init__(self):
        self._currently_in = set()
        self.tsh = TimeStampHandler()
    
    # HELP FUNCTIONS
    def __getpath(self, cardID):
        userid = self.get_userid(cardID)
        path = './logs' + os.sep + str(userid)
        return path
    
    # USER FUNCTIONS
    def add_ID(self,cardID, user):
        
        if not self.is_user(cardID):
            f= open("users.csv","a")
            f.write(cardID + ',' + str(user['id']) + ',' + user['username'] + '\n')
            f.close()
            self.timer_login(cardID)
        else:
            raise KeyError('user already exists')
        
    def is_user(self, cardID):
        df = my_readcsv('users.csv')
        try:
            df.loc[cardID]
            return True
        except KeyError:
            return False
        
    def get_username(self, cardID):
        df = my_readcsv('users.csv')
        return df.loc[cardID].values[1]
    
    def get_userid(self, cardID):
        df = my_readcsv('users.csv')
        return int(df.loc[cardID].values[0])
    
    def get_cardID(self, userid):
        df = my_readcsv('users.csv')
        return df[df.loc[:,'id']==userid].index.values[0]
    
    def currently_logged_in(self, listtype='username'):
        if listtype == 'cardID':
            return self._currently_in
        elif listtype == 'username':
            s = set()
            cardIDs = self._currently_in
            for cid in cardIDs:
                uname = self.get_username(cid)
                s.add(uname)
            return s

    # TIMER FUNCTIONS
    def timer_login(self, cardID):
        path = self.__getpath(cardID)
        
        self.tsh.create_log(path)
        self._currently_in.add(cardID)
        
    def timer_logout(self, cardID):
        path = self.__getpath(cardID)
        self.tsh.create_log(path, login='out')
        self._currently_in.remove(cardID)
        
#    def is_logged_in(self, cardID):
#        path = self.__getpath(cardID)
#        (lasttime, direction) = tsh.get_last_log(path)
#        
#        if direction == 'in':
#            return True
#        elif direction == 'out':
#            return False
    def is_logged_in(self, cardID):
        return cardID in self._currently_in
    