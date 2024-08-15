import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def main():
    if len(sys.argv) != 2:
        print("Usage: python yousician_search.py <search_string>")
        sys.exit(1)

    search_string = sys.argv[1]
    try:
        search_and_print_results(search_string)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def search_and_print_results(search_string):
    """
    Performs the search and prints the results
    """
    with webdriver.Chrome() as driver:
        try:
            # Go to the Yousician songs page
            driver.get("https://yousician.com/songs")
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            # Clicks "Accept All" on the cookie banner
            handle_cookie_banner(driver)

            print(f"Performing search for: {search_string}")
            search_input = driver.find_element(By.CSS_SELECTOR, "input[class^='SearchInput']")
            # Type the search string and press Enter
            search_input.send_keys(search_string + Keys.RETURN)

            parse_and_print_songs(driver)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            driver.quit()


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


def parse_and_print_songs(driver):
    """
    Parses the song and artist information from the loaded page.
    Handles pagination by clicking the "Next" button until the button becomes disabled.
    Logs if the initial search result is empty.
    """
    all_songs = []

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    # Find all song rows on the first page
    song_elements = driver.find_elements(By.CSS_SELECTOR, "a[class^='TableHead']")

    if not song_elements:
        print("No songs found on the initial search page")
        return

    for song_element in song_elements:
        try:
            song_name = song_element.find_elements(By.CSS_SELECTOR, "p[class^='Typography']")[0].text
            artist_name = song_element.find_elements(By.CSS_SELECTOR, "p[class^='Typography']")[1].text
            all_songs.append((artist_name, song_name))
        except IndexError:
            print("Could not parse song or artist name")

    # Check for pagination buttons
    pagination_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class^='PaginationButton']")
    if len(pagination_buttons) > 1:
        print("Pagination detected. Preparing to navigate through pages...")

        while True:
            # Select the last button in the list (">" button)
            next_button = pagination_buttons[-1]

            # Check if the last button is disabled
            if next_button.get_attribute("disabled") is not None:
                print("Reached the last page. Stopping pagination")
                break

            print("Clicking 'Next' button to go to the next page...")
            driver.execute_script("arguments[0].click();", next_button)

            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            # Process the new page
            song_elements = driver.find_elements(By.CSS_SELECTOR, "a[class^='TableHead']")
            if not song_elements:
                print("Warning: No items found on this page after clicking 'Next'. Possible issue with pagination!")
                break

            for song_element in song_elements:
                try:
                    song_name = song_element.find_elements(By.CSS_SELECTOR, "p[class^='Typography']")[0].text
                    artist_name = song_element.find_elements(By.CSS_SELECTOR, "p[class^='Typography']")[1].text
                    all_songs.append((artist_name, song_name))
                except IndexError:
                    print("Could not parse song or artist name")

            # Update pagination buttons for the next iteration
            pagination_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class^='PaginationButton']")

    # Log before starting the sorting process
    print("Sorting the collected songs by artist and song name...")
    print()

    # Sort and print the songs
    all_songs.sort()
    for artist, song in all_songs:
        print(f"{artist} - {song}")


if __name__ == "__main__":
    main()
