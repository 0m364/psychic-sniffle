import datetime

now = datetime.datetime.now()
hour = now.hour

if hour >= 5 and hour < 12:
    print("good morning")
elif hour >= 12 and hour < 18:
    print("good afternoon")
elif hour >= 18 and hour < 21:
    print("good evening")
else:
    print("good middle of the night")
