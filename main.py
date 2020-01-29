import json
import requests
from time import sleep
from itertools import product
from config import API_URL, DOMAINS, NAMES, HEADERS


class HIPB(object):
    def __init__(self):
        super(HIPB, self).__init__()


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
        print("{}:".format(user.email))
        for breach in user.breaches:
            print(
                "\tName: {}\n\t{} people pwned on {}".format(
                    breach.title, breach.pwn_count, breach.breach_date
                )
            )


def to_dict(response):
    return json.loads(response.content)


def request(service=None, query=None, params=None):
    sleep(2)
    response = requests.get(
        "{}/{}/{}?{}".format(API_URL, service, query, params), headers=HEADERS
    )
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
