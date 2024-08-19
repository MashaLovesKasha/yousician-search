import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def main():
    if len(sys.argv) < 2 or (len(sys.argv) == 2 and sys.argv[1] == "--headless"):
        print("Usage: pyth on yousician_search.py <search_string> [--headless]")
        sys.exit(1)

    search_string = " ".join(arg for arg in sys.argv[1:] if arg != "--headless")
    headless = "--headless" in sys.argv

    try:
        get_sorted_results(search_string, headless)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def get_sorted_results(search_string, headless=False):
    """
    Orchestrates the search, processing, sorting, and displaying of the results
    Allows running in headless mode if specified
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    with webdriver.Chrome(options=chrome_options) as driver:
        try:
            perform_search(driver, search_string)
            process_and_sort_songs(driver)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            driver.quit()


def perform_search(driver, search_string):
    """
    Opens the Yousician songs page, accepts cookies
    and performs a search using the provided search string
    """
    # Go to the Yousician songs page
    driver.get("https://yousician.com/songs")
    wait_for_page_load(driver)

    # Clicks "Accept All" on the cookie banner
    handle_cookie_banner(driver)

    print(f"Performing search for: {search_string}")
    search_input = driver.find_element(By.CSS_SELECTOR, "input[class^='SearchInput']")
    # Type the search string and press Enter
    search_input.send_keys(search_string + Keys.RETURN)


def process_and_sort_songs(driver):
    """
    Parses the song and artist information from the loaded page,
    handles pagination by clicking the "Next" button until the button becomes disabled
    and sorts the results by artist and song name in a case-insensitive manner
    """
    all_songs = []
    pagination_detected = False

    while True:
        wait_for_page_load(driver)

        # Find all song rows on the current page
        song_elements = driver.find_elements(By.CSS_SELECTOR, "a[class^='TableHead']")

        for song_element in song_elements:
            song_info = extract_song_info(song_element)
            if song_info:
                all_songs.append(song_info)

        # Check for pagination buttons
        pagination_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class^='PaginationButton']")

        if pagination_buttons and not pagination_detected:
            print("Pagination detected. Navigating through pages...")
            pagination_detected = True

        if not pagination_buttons or pagination_buttons[-1].get_attribute("disabled") is not None:
            if pagination_detected:
                print("Reached the last page. Stopping pagination")
            break

        # Click 'Next' button to go to the next page
        next_button = pagination_buttons[-1]
        driver.execute_script("arguments[0].click();", next_button)

    # If no songs were found, skip sorting
    if not all_songs:
        print("No songs found in the search results")
        return

    print("Sorting the collected songs by artist and song name...")
    print()
    all_songs.sort(key=lambda song: (song[0].lower(), song[1].lower()))
    for artist, song in all_songs:
        print(f"{artist} - {song}")


def wait_for_page_load(driver, timeout=10):
    """
    Waits for the page to fully load by checking that document.readyState is 'complete'
    """
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def handle_cookie_banner(driver):
    """
    Handles the cookie consent banner by clicking the "Accept All" button
    """
    try:
        time.sleep(1)
        accept_button = WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "onetrust-accept-btn-handler")
        )
        accept_button.click()

        print("Cookie banner is closed")
    except TimeoutException:
        print("Cookie banner did not appear within the timeout, proceeding with the test")
    except NoSuchElementException:
        print("No cookie banner found, proceeding with the test")
    except Exception as e:
        print(f"Error interacting with cookie banner: {e}")


def extract_song_info(song_element):
    """
    Extracts the song name and artist name from a song element
    Returns a tuple of (artist_name, song_name)
    """
    try:
        song_name = song_element.find_elements(By.CSS_SELECTOR, "p[class^='Typography']")[0].text
        artist_name = song_element.find_elements(By.CSS_SELECTOR, "p[class^='Typography']")[1].text
        return artist_name, song_name
    except IndexError:
        print("Could not parse song or artist name")
        return None


if __name__ == "__main__":
    main()
