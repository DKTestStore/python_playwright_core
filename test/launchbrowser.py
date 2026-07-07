
from playwright.sync_api import Page, expect, sync_playwright

def  test_validate_url(page:Page):
    page.goto("https://www.google.com/")
    my_url= page.url
    print(my_url)
    expect(page).to_have_url("https://www.google.com/")

def test_title_of_page(page:Page):
    page.goto("https://www.google.com/")
    page_title=page.title()
    print(page_title)
    expect(page).to_have_title("Google")

# @pytest.mark.asyncio
# async def test_verify_url_01():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch()
#         my_page = await browser.new_page()
#         await my_page.goto("https://www.google.com/")
#         my_url=my_page.url
#         print(my_url)
#         expect(my_page).to_have_url("https://www.google.com/")

def test_launch_chrome_browser():
    with sync_playwright() as page:
        print("test_launch_chrome_browser...")
        chrome_browser=page.chromium.launch(channel="chrome", headless=False)
        chrome_page=chrome_browser.new_page()
        chrome_page.goto("https://www.google.com/")
        print("Chrome Title:", chrome_page.title())
        expect(chrome_page).to_have_title("Google")
        chrome_browser.close()

def test_launch_msedge_browser():
    with (sync_playwright() as page):
        print("test_launch_msedge_browser...")
        msedge_browser=page.chromium.launch(channel="msedge", headless=False)
        msedge_page=msedge_browser.new_page()
        msedge_page.goto("https://www.google.com/")
        print("MS Edge Title:", msedge_page.title())
        expect(msedge_page).to_have_title("Google")
        msedge_browser.close()

def test_launch_firefox_browser():
    with (sync_playwright() as page):
        print("test_launch_firefox_browser...")
        firefox_browser=page.firefox.launch(headless=False)
        firefox_page=firefox_browser.new_page()
        firefox_page.goto("https://www.google.com/")
        print("Firefox Title:", firefox_page.title())
        expect(firefox_page).to_have_title("Google")
        firefox_browser.close()

def test_launch_safari_browser():
    with (sync_playwright() as page):
        print("test_launch_safari_browser...")
        safari_browser=page.webkit.launch(headless=False)
        safari_page=safari_browser.new_page()
        safari_page.goto("https://www.google.com/")
        print("Safari Title:", safari_page.title())
        expect(safari_page).to_have_title("Google")
        safari_browser.close()


def launch_browser(p,browser_name: str, url: str, headless: bool=False):
    browser_name = browser_name.lower()
    print("launch_browser...")
    try:
        if browser_name == "chrome":
            browser = p.chromium.launch(channel="chrome", headless=headless)
        elif browser_name == "msedge":
            browser = p.chromium.launch(channel="msedge", headless=headless)
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=headless)
        elif browser_name == "safari":
            browser = p.webkit.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        page = browser.new_page()
        page.goto(url)
        print(f"{browser_name.capitalize()} Title:", page.title())
        expect(page).to_have_title("Google")
        browser.close()
    except Exception as e:
        print(f"Error launching {browser_name} browser: {e}")


def test_launch_browser_logic():
    with (sync_playwright() as page):
        print("test_launch_browser_logic...")
        target_url="https://www.google.com/"
        browser_to_test=["chrome","firefox","safari"]
        for browser_name in browser_to_test:
            launch_browser(page, browser_name, target_url, headless=False )