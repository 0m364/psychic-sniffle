import datetime

now = datetime.datetime.now()
hour = now.hour

if hour >= 5 && hour < 12:
    print("good morning")
elif hour >= 12 && hour < 18:
    print("good afternoon")
elif hour >= 18 && hour < 21:
    print("good evening")
else:
    print("good middle of the night")
