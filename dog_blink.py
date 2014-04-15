'''
Created on Apr 15, 2014

@author: bonino
'''
from dog import DogGateway
import tts,time

if __name__ == '__main__':
    dog_zwave = DogGateway('http://192.168.0.102:8080/api/v1/')
    dog_zigbee = DogGateway('http://192.168.0.103:8080/api/v1/')
    
    dog_zwave.sendCommand('MeteringPowerOutlet_6', 'on')
    dog_zigbee.sendCommand('MeteringPowerOutlet_3781220529323341', 'on')
    
    power_peak = 0
        
    for i in range (0,20):
        #get the current power consumption
        status = dog_zwave.getStatus('MeteringPowerOutlet_6')
        power_1 = float(status['status']['SinglePhaseActivePowerMeasurementState'][0]['value'][:-1])
        status = dog_zigbee.getStatus('MeteringPowerOutlet_3781220529323341')
        power_2 = float(status['status']['SinglePhaseActivePowerMeasurementState'][0]['value'][:-1])
        
        print '%d W + %d W = %d W'%(power_1,power_2,(power_1+power_2))
        
        total_power = power_1+power_2
        
        if(total_power < (power_peak -10)) or (total_power > (power_peak +10)):
            #store the new maximum
            power_peak = total_power
            #warn the user
            tts.say("Reached a new power peak of %s Watt"%power_peak, "en")
        
        
        time.sleep(1)  
      
    dog_zwave.sendCommand('MeteringPowerOutlet_6', 'off')
    dog_zigbee.sendCommand('MeteringPowerOutlet_3781220529323341', 'off')
    
    for i in range (0,20):
        #get the current power consumption
        status = dog_zwave.getStatus('MeteringPowerOutlet_6')
        power_1 = float(status['status']['SinglePhaseActivePowerMeasurementState'][0]['value'][:-1])
        status = dog_zigbee.getStatus('MeteringPowerOutlet_3781220529323341')
        power_2 = float(status['status']['SinglePhaseActivePowerMeasurementState'][0]['value'][:-1])
        
        print '%d W + %d W = %d W'%(power_1,power_2,(power_1+power_2))
        
        total_power = power_1+power_2
        
        if(total_power < (power_peak -10)) or (total_power > (power_peak +10)):
            #store the new maximum
            power_peak = total_power
            #warn the user
            if(power_peak > 0):
                tts.say("Reached a new power peak of %s Watt"%power_peak, "en")
            else:
                tts.say("All devices are off")
        
        time.sleep(1) 
