import os
from dotenv import load_dotenv

load_dotenv()

# GEMINI_KEY="AIzaSyD1j7IP60BaNKkFJvNjAbe4vaYPUwbcfF8"
# UPSTAGE_KEY="up_ULzGbJVs57bcnNHm8D0KdI51Nzl4F"


GEMINI_KEY=os.getenv("GEMINI_API_KEY")
UPSTAGE_KEY=os.getenv("UPSTAGE_API_KEY")

print(f"GEMINI_KEY: {GEMINI_KEY}")
print(f"UPSTAGE_KEY: {UPSTAGE_KEY}")