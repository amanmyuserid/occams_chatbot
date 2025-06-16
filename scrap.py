from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse
import os
from collections import deque
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
import re

# --- CONFIG ---
base_url = "https://www.occamsadvisory.com/"
output_dir = "extracted"
os.makedirs(output_dir, exist_ok=True)
EXTRACT_MODE = "full"   # Use "full" or number as string

IST = timezone(timedelta(hours=5, minutes=30))
visited = set()

def safe_filename(url):
    path = urlparse(url).path.strip("/")
    if not path:
        return "index"
    name = path.replace("/", "_")
    return name

def get_limit_from_mode(mode):
    if mode == "full":
        return None
    try:
        return int(mode)
    except:
        return 7

def is_valid_link(link):
    # Only follow internal, non-media, non-mailto/javascript links
    if not link.startswith(base_url):
        return False
    if any(link.endswith(ext) for ext in [".pdf", ".jpg", ".jpeg", ".png", ".zip"]):
        return False
    if link.startswith("mailto:") or link.startswith("tel:") or "javascript:" in link:
        return False
    return True

def extract_markdown_hierarchy(html):
    soup = BeautifulSoup(html, "html.parser")
    # Remove unwanted elements
    for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
        tag.decompose()

    result_lines = []
    heading_re = re.compile(r"h([1-6])", re.I)
    last_level = 0

    body = soup.body or soup
    elements = list(body.descendants)

    for el in elements:
        if el.name and heading_re.fullmatch(el.name):
            level = int(el.name[1])  # Markdown uses 1-based heading levels
            text = el.get_text(strip=True)
            # Markdown heading, e.g., ## Heading
            result_lines.append("#" * level + " " + text)
            last_level = level
        elif el.name is None:
            text = str(el).strip()
            # Skip empty text and whitespace-only
            if text and not re.match(r"^\s*$", text):
                # Normal paragraph/content under last heading
                result_lines.append(text)

    return "\n\n".join(result_lines)

def crawl_first_n_pages(page, base_url, max_pages):
    queue = deque([base_url])
    count = 0
    while queue and (max_pages is None or count < max_pages):
        url = queue.popleft()
        if url in visited or urlparse(url).netloc != urlparse(base_url).netloc:
            continue
        visited.add(url)
        try:
            print(f"[+] Visiting: {url}")
            page.set_default_navigation_timeout(120000)
            page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"})
            page.goto(url, wait_until="networkidle", timeout=120000)
            page.wait_for_timeout(3000)
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            # Extract and save only Markdown hierarchy
            markdown_text = extract_markdown_hierarchy(html)
            md_filename = os.path.join(output_dir, safe_filename(url) + ".md")
            with open(md_filename, "w", encoding="utf-8") as f:
                f.write(markdown_text)
            print(f"[✓] Saved: {md_filename}")
            count += 1
            # Crawl links
            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"])
                if is_valid_link(link) and link not in visited:
                    queue.append(link)
        except Exception as e:
            print(f"[!] Failed on {url}: {e}")
    print(f"[✓] Saved for {count} page(s).")

if __name__ == "__main__":
    extract_limit = get_limit_from_mode(EXTRACT_MODE)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        crawl_first_n_pages(page, base_url, extract_limit)
        browser.close()
    print("[✓] Extraction complete.")