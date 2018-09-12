import requests
import json

def handle(st):
    # parse Github event
    req = json.loads(st)

    if req["action"] != "started":
        print("not a 'stared' event")
        exit(1)

    parsed = {} 

    parsed["login_name"] = req["sender"]["login"]
    parsed["repo_name"] =  req["repository"]["full_name"]
    parsed["avatar_url"] = req["sender"]["avatar_url"]

    # Useful for logging, GitHub's invoker will receive this string
    print(json.dumps(parsed))
