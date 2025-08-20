from dotenv import load_dotenv, set_key
import secrets
import random
import os
import sys

if len(sys.argv) > 1:
    print("Too many args. Usage: python3 init.py <y>(optional)")

def ask(option_name):
    if len(sys.argv) > 1 and (sys.argv[1] == "y" or sys.argv[1] == "-y" or sys.argv[1] == "--y"):
        return True
    print(f"Do you want to generate a value for {option_name}? (y/n)")
    return input().strip().lower() == 'y'

if not os.path.exists('.env'): # Create .env if it does not exist
    open('.env', 'w').close()

load_dotenv()

# Start of script
print("Initializing .env...")

if ask("flask: secret_key"):
    set_key('.env', "FLASK_SECRET_KEY", secrets.token_urlsafe(32))

if ask("postgres: db"):
    set_key('.env', "POSTGRES_DB", "HvGdb")

if ask("postgres: user"):
    set_key('.env', "POSTGRES_USER", "HvG")

if ask("postgres: password"):
    set_key('.env', "POSTGRES_PASSWORD", secrets.token_urlsafe(32))

if ask("pgadmin: default email"):
    name = ''.join(random.choice('0123456789ABCDEF') for i in range(8))
    set_key('.env', "PGADMIN_DEFAULT_EMAIL", f"{name}@example.com")

if ask("pgadmin: default password"):
    set_key('.env', "PGADMIN_DEFAULT_PASSWORD", secrets.token_urlsafe(32))

print("Done")