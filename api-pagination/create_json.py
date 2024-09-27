import json
import random
from faker import Faker

f = Faker()

data = []
for i in range(1000):
    data.append({
        "first_name": f.first_name(),
        "last_name": f.last_name(),
        "country": f.country(),
        "age": random.randint(0, 100),
        "city": f.city(),
    })

with open("data.json", "w") as f:
    json.dump(data, f)