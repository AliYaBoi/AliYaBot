import json
import os
import random

# Get the directory of this script
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "precepts.json")

# Load the precepts
with open(file_path, "r", encoding="utf-8") as f:
    precepts = json.load(f)

# Pick one at random
random_precept = random.choice(precepts)

print("💭 Random Precept of Zote 💭\n")
print(random_precept)

