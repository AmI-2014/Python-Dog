'''
Created on Apr 15, 2014

@author: bonino
'''
import time, math
from dog import DogGateway
from hue import HueBridge

def computeTotalPower(devices, gw):
    total_power = 0;
    #ask the status for the plugs
    for device in devices.keys():
        
        #print device
        
        #get the plug status
        status = gw.getStatus(device)
        
        #print status
        
        #extract the power value
        power_in_watt =  float(status['status']['SinglePhaseActivePowerMeasurementState'][0]['value'][:-1])
        #update the total power
        total_power += power_in_watt
        
    return total_power

def computeHue(power,max_power):
    hue_red = 65535
    hue_green = 25500
    #drive the hue with colors depending on the current power, use simple learning of maximum value
    ratio = 1
    if(max_power > 0):
        ratio = min(1, power / max_power) 
    #compute the current hue
    #return math.floor(abs(hue_green*(1-ratio))) 
    return math.floor(hue_green+(hue_red-hue_green)*ratio)

if __name__ == '__main__':
    
    dog_zwave = DogGateway('http://192.168.0.102:8080/api/v1/')
    dog_zigbee = DogGateway('http://192.168.0.103:8080/api/v1/')
    dog_gateways = [dog_zwave, dog_zigbee]
    
    hue_bridge = HueBridge('http://192.168.0.101/api/dog-gateway')
    
    #init the dictionary for holding all metering plug devices
    metering_plugs = {}
    
    #get all the metering plugs, in all gateways regardless of the network type
    for gw in dog_gateways:
        metering_plugs[gw.url]=gw.getDevicesOfType('MeteringPowerOutlet')
        
    # initial maximu set at 0
    max_power = 0;
    
    
    #turn on all devices
    for gw  in dog_gateways:
        for device in metering_plugs[gw.url ]:
            gw.sendCommand(device,'on')
            
        
    #start monitoring the status of devices
    while(True): 
        # power by gateway
        power_by_gw = {}
        
        for gw in dog_gateways:
            power_by_gw[gw.url] = computeTotalPower(metering_plugs[gw.url], gw)
        
        total_power = sum(power_by_gw.values())
        
        print total_power
        
        #drive the hue with colors depending on the current power, use simple learning of maximum value
        
        #set the hue
        i = 1
        hue_bridge.setHue(i, int(computeHue(total_power, max_power)))
    
        print int(computeHue(total_power, max_power))
        
        for gw_url in metering_plugs.keys():
            i+=1
            #set the hue
            hue_bridge.setHue(i, computeHue(power_by_gw[gw_url], max_power))
            
        if(max_power<total_power):
            max_power = total_power
        
        time.sleep(2)
    
            
    
       
            
        
    
        
    