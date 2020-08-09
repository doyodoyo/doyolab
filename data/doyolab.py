# doyolab package
# ver1.0 20200714

import sys
import glob
import serial
import os
import time
import requests
import datetime

def get_SerialPortsList():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def set_serial(port,baudrate):
    """
    :param port:
    :param baudrate:
    :return: serial
    """
    ser = serial.Serial()
    ser.port = port  #Arduinoのポート確認
    ser.baudrate = baudrate  # Arduinoと同じボーレート
    ser.setDTR(False)  # DTRを常にLOWにしReset阻止
    ser.open()
    time.sleep(1)
    ser.flushInput()
    ser.readline()
    print("set_serial success")
    return ser

def addData_To_textfile(filepath,data):
    """
    :param filepath:
    :param data:
    :return: nothing
    """
    with open(filepath, mode='a') as f:
        if type(data) is list:
            mydata=''
            for value in data:
                mydata= mydata + str(value) + ','
            mydata=mydata[:-1]
        else:
            mydata=str(data)
        f.write('\n')
        f.write(mydata)

def remove_file(filepath):
    """
    :param filepath:
    :return:nothing
    """
    try:
        os.remove(filepath)
    except:
        pass



def sendData_To_doyolabIoTserver(user_key,sub_id,date_data,int_data,float_data,text_data):
    # payload = {'user_key': user_key, 'sub_id': sub_id, 'date_data': date_data, 'int_data': int_data, 'float_data': float_data, 'text_data': text_data}
    payload = {'user_key': user_key, 'sub_id': sub_id}
    if date_data !='':
        payload['date_data']=date_data
    if int_data !='':
        payload['int_data']=int_data
    if float_data !='':
        payload['float_data']=float_data
    if text_data !='':
        payload['text_data']=text_data
    response = requests.post("https://doyolab.net/appli/iot/add", data=payload)

    # date_data= str(date_data).replace(' ','-')
    # response = requests.get('https://doyolab.net/appli/iot/add?d='+user_key+','+sub_id+','+date_data+','+str(int_data)+','+str(float_data)+','+str(text_data))
    return response.text
def getData_To_doyolabIoTserver(user_key,sub_id):
    payload = {'user_key': user_key, 'sub_id': sub_id}
    response = requests.post("https://doyolab.net/appli/iot/raw_data", data=payload)

    # getはセキュリティのため使えなくした
    # response = requests.get('https://doyolab.net/appli/iot/direct_dataview?uk='+user_key+'&sid='+sub_id)
    return response.text.replace("<br>","\n")

def sendMessage_To_Line(token,message):
    payload = {'token': token, 'message': message}
    response = requests.post("https://doyolab.net/appli/iot/line", data=payload)
    return response.text


def get_now_time():
    return datetime.datetime.now().time()

def get_now():
    return datetime.datetime.now()