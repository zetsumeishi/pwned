import re
import json
import requests
from time import sleep
from itertools import product
from config import API_URL, DOMAINS, NAMES, HEADERS


class HIPB(object):
    def __init__(self):
        super(HIPB, self).__init__()

    def to_dict(self, response):
        return json.loads(response.content)

    def request(self, service=None, query=None, params=None):
        sleep(2)
        response = requests.get(
            "{}/{}/{}?{}".format(API_URL, service, query, params),
            headers=HEADERS,
        )
        if response:
            return self.to_dict(response)


class Account(object):
    def __init__(self, email):
        super(Account, self).__init__()
        self.email = email
        self.breaches = []


class Breach(object):
    def __init__(self, data):
        super(Breach, self).__init__()
        for key in data:
            setattr(
                self, re.sub(r"(?<!^)(?=[A-Z])", "_", key).lower(), data[key]
            )


def main():
    emails = ["".join(x) for x in list(product(NAMES, DOMAINS))]
    results = []
    hipb = HIPB()

    for email in emails:
        account = Account(email)
        response = hipb.request("breachedaccount", email)
        if response:
            for breach in response:
                response = hipb.request("breach", breach["Name"])
                account.breaches.append(Breach(response))
        results.append(account)
    return results


if __name__ == "__main__":
    main()
