"""
[
    {
        'olivier.loustaunau@gmail.com': [
            {},
            {},
        ]
    },
]
"""

import json
import requests
from time import sleep
from itertools import product
from config import API_KEY, API_URL, DOMAINS, NAMES

headers = {"User-Agent": "pwned", "hibp-api-key": API_KEY}


class Account(object):
    def __init__(self, email):
        super(Account, self).__init__()
        self.email = email
        self.breaches = []


class Breach(object):
    def __init__(self, data):
        super(Breach, self).__init__()
        self.name = data["Name"]
        self.title = data["Title"]
        self.domain = data["Domain"]
        self.breach_date = data["BreachDate"]
        self.added_date = data["AddedDate"]
        self.modified_date = data["ModifiedDate"]
        self.pwn_count = data["PwnCount"]
        self.description = data["Description"]
        self.logo_path = data["LogoPath"]
        self.data_classes = data["DataClasses"]
        self.is_verified = data["IsVerified"]
        self.is_fabricated = data["IsFabricated"]
        self.is_sensitive = data["IsSensitive"]
        self.is_retired = data["IsRetired"]
        self.is_spam_list = data["IsSpamList"]


def display_results(results):
    for user in results:
        print(f"{user.email}:")
        for breach in user.breaches:
            print(
                f"\tName: {breach.title}\n"
                f"\t{breach.pwn_count} people pwned on {breach.breach_date}"
            )


def to_dict(response):
    return json.loads(response.content)


def request(service=None, query=None):
    sleep(2)
    response = requests.get(f"{API_URL}/{service}/{query}", headers=headers)
    if response:
        return to_dict(response)


def main():
    emails = ["".join(x) for x in list(product(NAMES, DOMAINS))]
    results = []

    for email in emails:
        account = Account(email)
        response = request("breachedaccount", email)
        if response:
            for breach in response:
                response = request("breach", breach["Name"])
                account.breaches.append(Breach(response))
        results.append(account)
    display_results(results)


if __name__ == "__main__":
    main()