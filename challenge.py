from clearblade.ClearBladeCore import System, Query, Developer
import psutil
import time
import keyboard
import matplotlib.pyplot as plt
import numpy as np


SystemKey = "d2e69be50baef9c6dff7be94fdcc01"
SystemSecret = "D2E69BE50BD0F3EDD0C5DAC3BF7A"
url = "https://platform.clearblade.com"

mySystem = System(SystemKey, SystemSecret, url, safe=False)

answer = input("Do you have an account registered in this system? Y/n\n")
answer = answer.lower();
while(answer != "y" or answer != "n"):
    if(answer == "y"):
        enterEmail = input("enter your email\n")
        enterPass = input("enter your password\n")
        break
    elif(answer == "n"):
        anon = mySystem.AnonUser()
        enterEmail = input("enter your email\n")
        enterPass = input("enter your password\n")
        newUser = mySystem.registerUser(anon, enterEmail, enterPass)
        break
    else:
        answer = input("wrong answer, input Y/n again.\n")


email = enterEmail
password = enterPass

newUser = mySystem.User(email, password)    #access the platform and generate a token
mqtt = mySystem.Messaging(newUser)          #use the token to access messaging on your account

mqtt.connect()         #connect to messaging client
counter = 0
time.sleep(1)
print("\nPlease press 'S' to start scanning your CPU average.")
while True:
    try:
        if keyboard.is_pressed('s'):
            print("Scanning is about to start!")
            time.sleep(1)
            break
    except:
        break

CPU_values = []

while(counter < 75):   #scanning loop
        cpu = str(psutil.cpu_percent())
        mqtt.publish('CPU-Usage', cpu)
        CPU_values.append(float(cpu))
        time.sleep(2)
        counter += 1


mqtt.disconnect()

plt.style.use('dark_background')
plt.xlabel('Seconds since starts')
plt.ylabel('CPU-Usage in %')
plt.xticks(np.arange(min(CPU_values), max(CPU_values), 10))
plt.plot(CPU_values)
plt.show()