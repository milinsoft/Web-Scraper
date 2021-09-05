import json
import requests


def takeurl():
    return input()


def obtain_quote():
    url_to_json = requests.get(user_url).json()
    try:
        content = url_to_json['content']
    except KeyError:
        print("Invalid quote resource!")
        # return takeurl()
    else:
        print(content)


if __name__ == "__main__":
    user_url = takeurl()
    url_status = requests.get(user_url).status_code
    if url_status == 200:
        obtain_quote()
    else:
        print("Invalid quote resource!")
