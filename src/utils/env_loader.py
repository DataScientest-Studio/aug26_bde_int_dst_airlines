import os
from dotenv import load_dotenv
load_dotenv()

def load_env_var(var_name: str):
    val = os.getenv(var_name)
    if not val:
        print(f"Variable not found: {val}")
    else:
        return val