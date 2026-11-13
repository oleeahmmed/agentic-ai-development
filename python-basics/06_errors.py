try:
    number = int("আমি সংখ্যা নই")
    print(number)
except ValueError:
    print("এটা সংখ্যা নয়।")

customer = {"name": "রাফি"}

print(customer.get("phone", "ফোন নম্বর নেই"))
