import json
import requests

cache={
    "access_token": None 
}

def refresh(refresh_token_path):
    """
        refresh refresh_token and access_token using current refresh_token 
    """
    with open(refresh_token_path, "r") as fp:
        refresh_token=fp.readline()
    res = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data={
        "client_id": "9e5f94bc-e8a4-4e73-b8be-63364c29d753",
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    })
    res = json.loads(res.text)
    with open(refresh_token_path, "w") as fp:
        fp.write(res["refresh_token"])
    cache.update(res)

def generate_auth_string(username, refresh_token_path):
    """
        https://learn.microsoft.com/en-us/exchange/client-developer/legacy-protocols/how-to-authenticate-an-imap-pop-smtp-application-by-using-oauth
        auth_str base64 encoding part is done by imaplib
    """
    if cache["access_token"] is None:
        refresh(refresh_token_path)
    access_token=cache["access_token"]

    auth_str = f"user={username}\x01auth=Bearer {access_token}\x01\x01"
    
    return auth_str


if __name__=="__main__":
    auth_str = generate_auth_string("user@email.com", "config/refresh_token")
    print(auth_str)
