import sys

from tools import read_page, search_and_read, search_wikipedia

sys.stdout.reconfigure(encoding="utf-8")

print("১. সার্চ")
for item in search_wikipedia("Artificial intelligence", 3):
    print("-", item["title"])
    print(" ", item["url"])
    print(" ", item["snippet"][:80])
print()

print("২. একটি পাতা পড়া")
page = read_page("Artificial intelligence")
print("শিরোনাম:", page["title"])
print("লিংক:", page["url"])
print("লেখা:", page["text"][:200], "...")
print()

print("৩. সার্চ + পড়া একসাথে")
for page in search_and_read("Python programming language", 2):
    print("-", page["title"], "| অক্ষর:", len(page["text"]))
print()

print("৪. অচেনা বিষয়")
print(search_wikipedia("Xyzzyville qwerty", 2))
