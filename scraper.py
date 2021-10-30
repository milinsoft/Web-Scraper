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


def save_html():
    r = requests.get(user_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    #print(r.content)
    with open('source.html', 'wb') as file:
        file.write(r.content)
    print("Content saved.")

if __name__ == "__main__":
    user_url = takeurl()
    # user_url = "https://www.imdb.com/title/tt0080684/"
    url_status = requests.get(user_url).status_code
    if url_status == 200:
        save_html()
    else:
        print(f"The URL returned {url_status}")
