import sys

import memory

sys.stdout.reconfigure(encoding="utf-8")

user = "test"

print("১. সেভ")
print(memory.save_memory(user, "নাম", "রাফি"))
print(memory.save_memory(user, "শহর", "চট্টগ্রাম"))
print()

print("২. আবার পড়া")
print(memory.get_memory(user))
print()

print("৩. পুরনো পছন্দ বদলানো")
print(memory.save_memory(user, "শহর", "ঢাকা"))
print(memory.get_memory(user))
print()

print("৪. ভুলে যাওয়া")
print(memory.forget_all(user))
print(memory.get_memory(user))
print()

print("৫. ফাইলে যা আছে")
print(memory.FILE.read_text(encoding="utf-8"))
