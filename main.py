import base64, os, json, requests, random, string

appId = "f68a4bb5-608a-4ff2-8123-be8ef797e0a6"

DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

def b64(message):
    return base64.b64encode(message.encode('ascii')).decode('ascii')

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def login_with_2fa():
    os.system("cls")
    cfg = load_config()

    if cfg.get('autoUseConfig'):
        email = cfg['email']
        password = cfg['password']
    else:
        print("Type \"config\" to use email & password from config.json")
        email = input("Email: ")
        if email == "config":
            email = cfg['email']
            password = cfg['password']
        else:
            password = input("Password: ")

    url = "https://public-ubiservices.ubi.com/v3/profiles/sessions"
    headers = {
        "Ubi-AppId": appId,
        "Authorization": "Basic " + b64(email + ":" + password),
        "Ubi-RequestedPlatformType": "uplay",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "content-type": "application/json"
    }

    resp = requests.post(url, headers=headers)
    if resp.status_code != 200:
        print(f"Login failed: {resp.status_code}")
        os.system("pause")
        return None

    data = resp.json()
    os.system("cls")
    facode = input("Enter 2FA code sent to your email: ")

    headers = {
        "Ubi-AppId": appId,
        "Authorization": "ubi_2fa_v1 t=" + data['twoFactorAuthenticationTicket'],
        "Ubi-2facode": facode,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "content-type": "application/json"
    }

    resp = requests.post(url, headers=headers)
    data = resp.json()

    if resp.status_code == 200:
        print("Login successful!")
        return data['ticket']
    else:
        print("2FA failed:", data)
        os.system("pause")
        return None

def send_to_discord(username):
    url = f"https://r6.tracker.network/profile/pc/{username}"
    message = f"The username [{username}]({url}) is available."
    payload = {
        "content": "@here",
        "embeds": [
            {
                "author": {"name": "Name Checker"},
                "description": message,
                "color": 16776960
            }
        ]
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})
    if response.status_code != 204:
        print("Failed to send to webhook.")

def check_username(ticket, username):
    url = f"https://public-ubiservices.ubi.com/v1/profiles?nameOnPlatform={username}&platformType=uplay"
    headers = {
        "Ubi-AppId": appId,
        "Content-Type": "application/json",
        "Ubi-RequestedPlatformType": "uplay",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Authorization": f"ubi_v1 t={ticket}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return not bool(response.json().get("profiles", []))
    else:
        print("Rate limited.")
        return False

def generate_random_username(length, symbols=False):
    if length == 4:
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
    elif length == 3 and not symbols:
        chars = string.ascii_lowercase + string.digits
        return random.choice(string.ascii_lowercase) + ''.join(random.choice(chars) for _ in range(2))
    elif length == 3 and symbols:
        chars = string.ascii_lowercase + string.digits
        sym = "._-"
        return random.choice(string.ascii_lowercase) + random.choice(sym) + random.choice(chars + sym)

def read_from_file():
    try:
        with open("uplays.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("uplays.json not found.")
        return []

def run_checker(ticket):
    while True:
        os.system("cls")
        choice = input("Choose an option:\n1. Check 4 Letters\n2. Check 3 Chars\n3. Check 3 Chars with Symbols\n4. Read From File\n5. Exit\nEnter your choice: ")

        if choice == "5" or choice.lower() == "exit":
            break

        if choice in ("1", "2", "3"):
            length = 4 if choice == "1" else 3
            symbols = choice == "3"
            for _ in range(250):
                username = generate_random_username(length, symbols=symbols)
                if check_username(ticket, username):
                    print(f"AVAILABLE: '{username}'")
                    send_to_discord(username)
                else:
                    print(f"Taken: '{username}'")

        elif choice == "4":
            for username in read_from_file():
                if check_username(ticket, username):
                    print(f"AVAILABLE: '{username}'")
                    send_to_discord(username)
                else:
                    print(f"Taken: '{username}'")

        print("\nDone checking.")
        input("Press Enter to continue...")

def main():
    ticket = login_with_2fa()
    if ticket:
        run_checker(ticket)

if __name__ == "__main__":
    main()