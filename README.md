# ubisoft-name-checker
A Ubisoft/Rainbow Six Siege username availability checker with login, random name generation, and Discord webhook notifications.

## Requirements
- Python 3.x
- `requests`

Install dependencies:
```bash
pip install requests
```

## Setup
Configure `config.json` in the same folder as the script:
```json
{
    "autoUseConfig": true,
    "email": "your@email.com",
    "password": "yourpassword"
}
```

---

## Usage
Run the script:
```bash
python main.py
```
You will be prompted for a 2FA code sent to your email, then presented with the following options:

1. **Check 4 Letters** — generates and checks 250 random 4-letter usernames
2. **Check 3 Chars** — generates and checks 250 random 3-character usernames
3. **Check 3 Chars with Symbols** — same as above but includes `._-` symbols
4. **Read From File** — checks a list of usernames from `uplays.json`

---

## uplays.json
To use option 4, create an `uplays.json` file in the same folder:
```json
["PlayerName1", "PlayerName2", "PlayerName3"]
```

---

## Discord Notifications
Available usernames are sent to a Discord webhook as an embed with a link to the [R6 Tracker](https://r6.tracker.network) profile page.

To change the webhook, update `DISCORD_WEBHOOK_URL` at the top of the script.

---

## Contact
[Discord](https://discord.gg/tKNRwVAyjd)
