tasks = ["ইমেইল দেখা", "রিপোর্ট লেখা", "মিটিং"]

print("প্রথম কাজ:", tasks[0])
print("মোট কাজ:", len(tasks))

tasks.append("কাস্টমারকে উত্তর দেওয়া")
print("এখন কাজ:", tasks)

customer = {
    "name": "রাফি",
    "city": "চট্টগ্রাম",
    "orders": 3,
}

print("কাস্টমার:", customer["name"])
print("ফোন:", customer.get("phone", "নেই"))
