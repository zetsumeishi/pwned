# -*- coding: utf-8 -*-
API_KEY = "YOUR_KEY"
API_URL = "https://haveibeenpwned.com/api/v3"

HEADERS = {"User-Agent": "user-agent", "hibp-api-key": API_KEY}

DOMAINS = ["@example.com", "@test.com"]
NAMES = ["john.doe", "john"]

# Once combined, you get the following list:
# ['john.doe@example.com', 'john.doe@test.com', 'john@example.com', 'john@test.com']
