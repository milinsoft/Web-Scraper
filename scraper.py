import requests
from bs4 import BeautifulSoup


def takeurl():
    return input()


def obtain_quote():
    url_to_json = requests.get(user_url, headers={'Accept-Language': 'en-US,en;q=0.5'}).json()
    try:
        content = url_to_json['content']
    except KeyError:
        print("Invalid quote resource!")
    else:
        print(content)


def obtain_desctiption():

    if "www.imdb.com/title/" not in user_url:
        print("Invalid movie page!")
    else:
        r = requests.get(user_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        soup = BeautifulSoup(r.content, 'html.parser')
        # print(soup.prettify())
        title = soup.find('title').text
        movie_desctiption = soup.find('meta', {"name": "description"}).get('content')
        movie_data = {"title": title, "description": movie_desctiption}

        print(movie_data)


if __name__ == "__main__":
    user_url = takeurl()
    # user_url = "https://www.imdb.com/title/tt0080684/"
    url_status = requests.get(user_url).status_code
    if url_status == 200:
        obtain_desctiption()
    else:
        print("no response!")
