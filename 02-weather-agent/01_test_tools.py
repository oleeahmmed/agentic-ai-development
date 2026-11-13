import sys

from tools import get_current_weather, get_forecast, convert_temperature

sys.stdout.reconfigure(encoding="utf-8")

print("১. এখনকার আবহাওয়া")
print(get_current_weather("Dhaka"))
print()

print("২. ৩ দিনের পূর্বাভাস")
print(get_forecast("Chattogram", 3))
print()

print("৩. তাপমাত্রা রূপান্তর")
print(convert_temperature(30, "C"))
print()

print("৪. ভুল শহর")
print(get_current_weather("Xyzzyville"))
