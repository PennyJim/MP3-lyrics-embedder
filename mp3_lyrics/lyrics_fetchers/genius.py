import requests
from bs4 import BeautifulSoup
import urllib.parse as parse

access_token = os.environ['GENIUS_ACCESS_TOKEN']
url = "https://api.genius.com/"

def search_string(artist, song):
    return parse.quote_plus(artist+" "+song)

def search_genius(query):
    endpoint = "search?q="+query
    result = requests.get(url+endpoint, headers={'Authorization': 'Bearer '+access_token})

    result = result.json()
    return result

def get_song_from_search(response):
    return response['result']['title'].lower()

def get_artist_from_search(response):
    return response['result']['primary_artist']['name'].lower()

def get_url_from_search(response):
    return response['result']['url']

def does_song_match(artist, title, song):
    artist = artist.lower()
    title = title.lower()

    possible_title = song['title'].lower()
    primary_artist = song['primary_artist']['name'].lower()

    return title == possible_title and primary_artist == artist

def get_url(artist, song):
    query = search_string(artist, song)
    result = search_genius(query)
    
    if result['meta']['status'] == 200:
        responses = result['response']['hits']
    else:
        raise Exception("No response from Genius API")

    for response in responses:
        if does_song_match(artist, song, response['result']):
            return get_url_from_search(response)
    
    raise Exception("Song not found in Search for '"+query+"'")

def handle_element(element):
    if isinstance(element, str):
        return element
    elif element.name == "br":
        return '\n'
    else:
        return ""

def extract_lyrics(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    lyric_container = soup.find('div', {'data-lyrics-container': 'true'})
    if lyric_container is None:
        raise Exception("Song didn't have lyrics in Genius")

    direct_children = lyric_container.children
    next(direct_children) # Discard first child
    first_element = next(direct_children)
    elements = first_element.next_elements

    lyrics = handle_element(first_element)
    for element in elements:
        if element.name == "div":
            break
        lyrics += handle_element(element)


    return lyrics
    
def get_lyrics(song_details):
    artist = song_details['artist']
    song = song_details['title']

    if "(instrumental)" in song.lower():
        raise Exception("Song is named instrumental.. Skipping")


    song_url = get_url(artist, song)
    html_response = requests.get(song_url)
    # html_doc = web_tools.get_webpage(song_url)

    lyrics = extract_lyrics(html_response.text)

    return lyrics, song_url
