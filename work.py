import aiohttp
import aiofiles
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Список URL для обхода
urls = [
    "https://regex101.com/",
    "https://docs.python.org/3/this-url-will-404.html",
    "https://www.nytimes.com/guides/",
    "https://www.mediamatters.org/",
    "https://1.1.1.1/",
    "https://www.politico.com/tipsheets/morning-money",
    "https://www.bloomberg.com/markets/economics",
    "https://www.ietf.org/rfc/rfc2616.txt"
]

async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Failed to retrieve {url}: Status {response.status}")
                return None
    except aiohttp.ClientError as e:
        print(f"Exception occurred while fetching {url}: {e}")
        return None
    except asyncio.TimeoutError:
        print(f"Timeout occurred while fetching {url}")
        return None

async def extract_links(html, base_url):
    links = set()
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all('a', href=True):
        link = urljoin(base_url, tag['href'])
        links.add(link)
    return links

async def write_links_to_file(file_path, links):
    async with aiofiles.open(file_path, 'a') as f:
        for link in links:
            await f.write(link + '\n')

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        pages = await asyncio.gather(*tasks)

        all_links = set()
        for page, url in zip(pages, urls):
            if page:
                links = await extract_links(page, url)
                all_links.update(links)

        await write_links_to_file('found_links_with_async.txt', all_links)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(f"RuntimeError: {e}")

