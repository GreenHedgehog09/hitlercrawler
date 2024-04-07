import asyncio
import re
import time

import aiohttp
from bs4 import BeautifulSoup


class HitlerLinksSearch:
    async def request(self, session, url):
        async with session.get(url) as response:
            body = await response.text()
            soup = BeautifulSoup(body, 'lxml')  # Parser lxml(fast)
            # Search
            tags = soup.find_all('a', href=re.compile(r'^/wiki/'))
            links = [tag['href'] for tag in tags]
            for i, link in enumerate(links):
                if link == '/wiki/Adolf_Hitler':
                    return [True, 'https://en.wikipedia.org/' + link]
                else:
                    links[i] = 'https://en.wikipedia.org/' + link
            return [False, links]

    async def create_tasks(self, urls):
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(self.request(session, url)) for url in urls]
            responses = await asyncio.gather(*tasks)
            return responses

    def main(self, link):
        output_link = 'Hitler`s page not found...'
        urls = []
        layer = 0
        while layer < 7:
            if not layer:
                urls = [link]
            else:
                print(f'Pass layer: {layer}')
            # Start tasks
            loop = asyncio.get_event_loop()
            responses = loop.run_until_complete(self.create_tasks(urls))
            urls.clear()
            for response in responses:
                if response[0]:
                    return response[1]
                else:
                    urls.extend(response[1])
            layer += 1
        return output_link


if __name__ == '__main__':
    while True:
        input_link = input('Enter link: ')
        if input_link == '':
            print('Exit...')
            break
        start_time = time.time()
        obj_hitler = HitlerLinksSearch()
        result = obj_hitler.main(input_link)
        print(f'Result: {result}')
        print(f'Duration: {time.time() - start_time}')
