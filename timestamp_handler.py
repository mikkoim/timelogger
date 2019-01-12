# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 15:35:32 2019

@author: Mikko Impiö
"""

from datetime import datetime as dt
import pandas as pd

def read_time_df(fname):
    df = pd.read_csv(fname, header=None)
    
    # timestamps to datetime series
    df.iloc[:,0] = df.iloc[:,0].apply(lambda x: dt.fromtimestamp(x))
    
    df.columns = ['timestamp', 'direction']
    
    return df

class TimeStampHandler():
    
    def __init__(self):
        pass
    
    def create_log(self, path, login='in'):
        ts = dt.now().timestamp()
        f = open(path,"a")
        f.write(str(ts)+ ',' + login + '\n')
        f.close()
    
    def get_last_log(self, path):
        df = read_time_df(path)
        lasttime = df.iloc[-1,0]
        direction = df.iloc[-1,1]
        return (lasttime, direction)
    
    def get_time_delta(self, path):
        (lasttime, direction) = self.get_last_log(path)
        now = dt.now()
        
        td = now-lasttime
        return td.total_seconds()
        