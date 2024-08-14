import sys
import requests
from bs4 import BeautifulSoup


def main():
    if len(sys.argv) != 2:
        print("Usage: python yousician_search.py <search_string>")
        sys.exit(1)

    search_string = sys.argv[1]
    try:
        search_and_print_results(search_string)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the HTTP request: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def search_and_print_results(search_string):
    base_url = build_search_url(search_string)
    all_songs = []
    page_number = 1

    while True:
        url = f"{base_url}?page={page_number}"
        response = fetch_search_results(url)
        songs, has_more_pages = parse_songs_and_check_pagination(response.text)
        all_songs.extend(songs)

        if not has_more_pages:
            break

        page_number += 1  # Move to the next page

    if not all_songs:
        print("No songs found.")
        return

    all_songs.sort()
    print_songs(all_songs)


def build_search_url(search_string):
    """
    Constructs the search URL for Yousician songs.
    Joins multiple words with hyphens.
    """
    formatted_search_string = "-".join(search_string.split())
    return f"https://yousician.com/songs/search/{formatted_search_string}"


def fetch_search_results(url):
    """
    Fetches the search results page from the given URL.
    """
    print(f"Fetching URL: {url}")
    response = requests.get(url)
    response.raise_for_status()  # This will raise an error for HTTP errors
    return response


def parse_songs_and_check_pagination(html):
    """
    Parses the song and artist information from the HTML content.
    Also checks if there are more pages by inspecting the pagination buttons.
    """
    soup = BeautifulSoup(html, 'html.parser')
    print("HTML fetched successfully, parsing...")

    songs = []

    for song_element in soup.find_all('a', class_=lambda x: x and x.startswith('TableHead')):
        try:
            divs = song_element.find_all('div', class_=lambda x: x and x.startswith('TableCell'))
            song_name = divs[0].find('p', class_=lambda x: x and x.startswith('Typography')).text.strip()
            artist_name = divs[1].find('p', class_=lambda x: x and x.startswith('Typography')).text.strip()
            songs.append((artist_name, song_name))
        except (AttributeError, IndexError) as e:
            print(f"Could not find song or artist information: {e}")

    # Determine if there is a next page by checking the pagination buttons
    has_more_pages = False
    pagination_buttons = soup.find_all('button', class_=lambda x: x and x.startswith('PaginationButton'))

    if pagination_buttons:
        last_button = pagination_buttons[-1]
        if 'disabled' not in last_button.attrs:
            has_more_pages = True  # If the last button is not disabled, there's a next page

    return songs, has_more_pages


def print_songs(songs):
    """
    Prints the list of songs, sorted by artist and song name.
    """
    for artist, song in songs:
        print(f"{artist} - {song}")


if __name__ == "__main__":
    main()
