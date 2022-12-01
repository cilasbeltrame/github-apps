#!/usr/bin/env python3
"""
Script done using https://docs.github.com/en/developers/apps/building-github-apps/authenticating-with-github-apps
"""
import os
import jwt
import requests
import time

PRIVATE_KEY = os.getenv('GH_APP_PRIVATE_KEY')
APP_ID = os.getenv('GH_APP_ID')
INSTALLATION_ID = os.getenv('GH_INSTALLATION_ID')

iat = int(time.time())
exp = int(time.time()) + 600

if 'other-domain' in os.getenv('GITHUB_ACTION'):
    github_api = "https://github.other-domain.com/api/v3"
    PRIVATE_KEY = os.getenv('GH_APP_OTHERDOMAIN_PRIVATE_KEY')
    APP_ID = os.getenv('GH_OTHERDOMAIN_APP_ID')
    INSTALLATION_ID = os.getenv('GH_OTHERDOMAIN_INSTALLATION_ID')
else:
    github_api = "https://api.github.com"

payload = {"iat": iat, "exp": exp, "iss": APP_ID}
jwt_token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
headers = {
    "Authorization": "Bearer {}".format(jwt_token),
    "Accept": "application/vnd.github.v3+json",
}
# Retrieving token
resp = requests.post(
    "{}/app/installations/{}/access_tokens".format(github_api,
                                                   INSTALLATION_ID
                                                   ),
    headers=headers,
)
token = resp.json()["token"]
print('::set-output name=token::{}'.format(token))
