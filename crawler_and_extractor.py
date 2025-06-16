import asyncio
import os
import re
import io
import urllib.robotparser
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from PIL import Image
from fpdf import FPDF
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# --- CONFIGURATION FROM YOUR ORIGINAL SCRIPT ---
BASE_URL = "https://occamsadvisory.com/"
OUTPUT_DIR = "extracted"
CRAWL_MAX_LINKS = None     # None => no artificial cap
CONCURRENT_TASKS = 5        # how many pages to fetch/extract in parallel
PAGE_LOAD_TIMEOUT = 120000  # ms
SCROLL_PAUSE = 3          # seconds pause between scrolls, adjusted for new logic

# --- SCREENSHOT SETTINGS FROM YOUR REFERENCE SCRIPT ---
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 832
FINAL_DELAY = 4             # seconds before screenshot to settle layout

# --- NEW CONFIGURATION MERGED FROM REFERENCE SCRIPT ---
EXPAND_ALL_SELECTORS = [
    'div.wp-block-group.is-layout-constrained div[tabindex="0"]',
    'div.accordion-item > button',
    'div.faq-question-title',
    'button.accordion-toggle',
    'div[role="button"][aria-expanded="false"]',
    '.toggle-arrow',
    '.question-header'
]
EXPAND_CLICK_DELAY_SECONDS = 0.4

# --- HELPER FUNCTIONS (FROM YOUR ORIGINAL SCRIPT) ---
def extract_markdown_hierarchy(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
        tag.decompose()
    lines = []
    heading_re = re.compile(r"^h([1-6])$", re.I)
    for el in soup.body.descendants:
        if getattr(el, "name", None) and heading_re.fullmatch(el.name):
            level = int(el.name[1])
            text = el.get_text(strip=True)
            lines.append("#" * level + " " + text)
        elif el.name is None:
            text = str(el).strip()
            if text and not text.isspace():
                lines.append(text)
    return "\n\n".join(lines)

def sanitize_segment(seg: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "", seg)

# --- LINK DISCOVERY (FROM YOUR ORIGINAL SCRIPT, UNCHANGED) ---
async def get_all_website_links(base_url, rp, max_links=None):
    parsed = urlparse(base_url)
    base_domain = parsed.netloc
    queue = asyncio.Queue()
    await queue.put(base_url)
    found = {base_url}
    visited = set()
    count = 0

    print("Discovering links…", end=" ", flush=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        while not queue.empty() and (max_links is None or len(found) < max_links):
            url = await queue.get()
            if url in visited:
                continue
            visited.add(url)
            count += 1
            print(count, end=" ", flush=True)

            if not rp.can_fetch("*", url):
                continue
            try:
                await page.goto(url, timeout=PAGE_LOAD_TIMEOUT, wait_until="domcontentloaded")
                await asyncio.sleep(2) # Brief wait
                html = await page.content()
                soup = BeautifulSoup(html, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = urljoin(url, a["href"])
                    parsed_href = urlparse(href)
                    clean = href.split('#')[0].rstrip('/')
                    if (parsed_href.scheme in ("http", "https")
                        and parsed_href.netloc == base_domain
                        and clean not in found):
                        found.add(clean)
                        await queue.put(clean)
            except Exception:
                pass
        await browser.close()
    print()
    return found

# --- MODIFIED PAGE PROCESSING FUNCTION ---
async def process_page(sem, browser, url):
    async with sem:
        html = None
        screenshot_bytes = None
        print(f"\nProcessing: {url}")
        try:
            page = await browser.new_page()
            await page.set_viewport_size({"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT})
            await page.goto(url, wait_until="networkidle", timeout=PAGE_LOAD_TIMEOUT)

            # --- 1. Expand all hidden content (from reference code) ---
            print("Attempting to expand hidden content...")
            for selector in EXPAND_ALL_SELECTORS:
                elements_to_click = await page.locator(selector + ':visible:enabled').all()
                if elements_to_click:
                    for element in elements_to_click:
                        try:
                            await element.click(timeout=2000)
                            await asyncio.sleep(EXPAND_CLICK_DELAY_SECONDS)
                        except (PlaywrightTimeoutError, Exception):
                            pass # Ignore elements that can't be clicked

            # --- 2. Intelligently scroll to load all content (from reference code) ---
            print("Scrolling to load all content...")
            last_height = await page.evaluate("document.body.scrollHeight")
            max_scrolls = 20
            for _ in range(max_scrolls):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(SCROLL_PAUSE)
                new_height = await page.evaluate("document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # --- 3. Hide sticky/fixed elements for clean screenshot (from reference code) ---
            print("Adjusting fixed/sticky elements...")
            await page.evaluate("""
                () => {
                    document.querySelectorAll('body *').forEach(el => {
                        const style = window.getComputedStyle(el);
                        if (style.position === 'fixed' || style.position === 'sticky') {
                            el.style.position = 'static';
                        }
                    });
                }
            """)
            await asyncio.sleep(1) # Wait for style changes to apply

            if FINAL_DELAY > 0:
                await asyncio.sleep(FINAL_DELAY)

            # --- 4. Grab HTML and take screenshot ---
            html = await page.content()
            screenshot_bytes = await page.screenshot(full_page=True)
            print(f"Successfully captured screenshot for: {url}")
            await page.close()

        except Exception as e:
            print(f"Failed to process {url}: {e}")
            if 'page' in locals() and not page.is_closed():
                await page.close()
            return # Exit this function if processing fails

        # If processing was successful, proceed to save files
        if html and screenshot_bytes:
            # --- 5. Save markdown (from your original code) ---
            md = extract_markdown_hierarchy(html)
            parsed = urlparse(url)
            segments = [seg for seg in parsed.path.strip("/").split("/") if seg]
            folder = OUTPUT_DIR
            for seg in segments:
                folder = os.path.join(folder, sanitize_segment(seg))
            os.makedirs(folder, exist_ok=True)
            name = "index" if not segments else "_".join(sanitize_segment(s) for s in segments)
            md_path = os.path.join(folder, f"{name}.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(f"{url}\n\n")
                f.write(md)
            print(f"Saved markdown: {md_path}")

            # --- 6. Convert screenshot to PDF (from your original code) ---
            try:
                img = Image.open(io.BytesIO(screenshot_bytes))
                if img.mode == 'RGBA':
                    img = img.convert('RGB')

                w_px, h_px = img.size
                mm_per_px = 25.4 / 96
                w_mm, h_mm = w_px * mm_per_px, h_px * mm_per_px
                pdf = FPDF(unit="mm", format=(w_mm, h_mm))
                pdf.add_page()
                pdf.image(io.BytesIO(screenshot_bytes), 0, 0, w_mm, h_mm)
                pdf_path = os.path.join(folder, f"{name}.pdf")
                pdf.output(pdf_path)
                print(f"Saved PDF: {pdf_path}")
            except Exception as e:
                print(f"Error creating PDF for {url}: {e}")


async def main():
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urljoin(BASE_URL, "/robots.txt"))
    try:
        rp.read()
    except:
        rp.can_fetch = lambda *_: True

    links = await get_all_website_links(BASE_URL, rp, max_links=CRAWL_MAX_LINKS)
    print(f"\nFound {len(links)} pages. Starting parallel extraction ({CONCURRENT_TASKS} at a time)...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    sem = asyncio.Semaphore(CONCURRENT_TASKS)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        tasks = [process_page(sem, browser, url) for url in sorted(list(links))]
        await asyncio.gather(*tasks)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())