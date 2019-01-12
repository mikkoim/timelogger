import subprocess
import os
from tg_handler import TGHandler
tgh = TGHandler()
while True:
    FNULL = open(os.devnull,'w')
    poll =  subprocess.call(['nfc-poll'], stdout=FNULL, stderr=subprocess.STDOUT) 
    #poll =  subprocess.call(['nfc-poll'])
    while not poll:
        try:
            #poll = subprocess.call
            poll =  subprocess.call(['nfc-poll'], stdout=FNULL, stderr=subprocess.STDOUT)
            output = subprocess.check_output(['nfc-poll'])
            print("Card present")
            #print('{}'.format(output))
            cardID = str(output[192:])
            cardID = cardID.strip()
            print('{}'.format(cardID))
            tgh.set_current_card_ID(cardID)

        except subprocess.CalledProcessError:
        #poll = subprocess.call(['nfc-poll'])
        #output = subprocess.check_output(['nfc-poll'])
            print("Card removed")
            tgh.set_current_card_ID('No card')
    print("No cards")
    tgh.set_current_card_ID('No card')
