
from datetime import datetime

now = datetime.now()


current_time = now.strftime("%H:%M:%S")

print("Current Time =", current_time)

if now.hour == 19 :
    print("Il est 19h")
