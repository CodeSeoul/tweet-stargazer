import requests
import json

def handle(st):
    # parse Github event
    req = json.loads(st)

    if req["action"] != "started":
        print("not a 'stared' event")
        return

    login_name = req["sender"]["login"]
    repo_name =  req["repository"]["full_name"]

    # Get avatar url
    avatar_req = {}
    avatar_req["avatar_url"] = req["sender"]["avatar_url"]

    # download the avatar binary using getavatar function
    r = requests.post("http://gateway:8080/function/get-avatar", json=avatar_req)
    res = r.json()

    gazer = {}
    gazer["login"] = login_name
    gazer["contentType"] = res["contentType"]
    gazer["image"] = res["content"]
    gazer["repository"] = repo_name

    r2 = requests.post("http://gateway:8080/function/tweet-stargazer", json=gazer)

    club_res = {}
    club_res["tweet_result"] = r2.text
    club_res["status"] = "success"
    club_res["username"] = login_name
    club_res["repository"] = repo_name

    # Useful for logging, GitHub's invoker will receive this string
    print(json.dumps(club_res))
