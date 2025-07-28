from playwright.sync_api import sync_playwright

def test_main_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:5000/')
        assert 'Singapore News' in page.title()
        assert page.locator('article').count() > 0

def test_category_filter():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:5000/category/politics')
        assert 'Politics' in page.inner_text('h1')
        articles = page.locator('article')
        assert articles.count() > 0

def test_search():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:5000/search?q=election')
        assert 'Search Results' in page.inner_text('h2')
        assert page.locator('article').count() > 0

def test_article_detail():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:5000/article?url=test&title=Test+Article')
        assert 'Test Article' in page.title()
        assert page.locator('.article-content').is_visible()

def test_responsiveness():
    devices = [
        {'name': 'Desktop', 'width': 1280, 'height': 800},
        {'name': 'Mobile', 'width': 375, 'height': 667}
    ]
    with sync_playwright() as p:
        for device in devices:
            browser = p.chromium.launch()
            context = browser.new_context(**device)
            page = context.new_page()
            page.goto('http://localhost:5000/')
            assert page.locator('nav').is_visible()

def test_error_handling():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:5000/search?q=invalid')
        assert 'Error' in page.inner_text('h1')
        assert 'Failed to fetch news' in page.inner_text('p')