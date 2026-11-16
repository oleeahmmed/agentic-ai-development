import sys

from tools import get_forecast, get_weather

sys.stdout.reconfigure(encoding="utf-8")

print("১. ঢাকার এখনকার আবহাওয়া")
print(get_weather("Dhaka"))

print("\n২. চট্টগ্রামের ৩ দিনের পূর্বাভাস")
print(get_forecast("Chattogram"))

print("\n৩. ভুল শহর")
print(get_weather("Xyzzyville"))
