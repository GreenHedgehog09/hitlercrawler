import asyncio
import multiprocessing
import re
import time

import aiohttp
from bs4 import BeautifulSoup


class HitlerLinksSearch:
    async def request(self, session, url: str) -> list:
        try:
            async with session.get(url) as response:
                body = await response.text()
                soup = BeautifulSoup(body, 'lxml')  # Parser lxml(fast)
                # Search
                tags = soup.find_all('a', href=re.compile(r'^/wiki/'))
                links = [tag['href'] for tag in tags]
                if not links:
                    return [True, 'Hitler`s page not found...']
                for i, link in enumerate(links):
                    if link == '/wiki/Adolf_Hitler':
                        return [True, 'https://en.wikipedia.org' + link]
                    else:
                        links[i] = 'https://en.wikipedia.org' + link
                return [False, links]
        except aiohttp.InvalidURL as e:
            return [True, f'Error: Invalid URL.']

    async def create_tasks(self, urls: list) -> list:
        try:
            async with aiohttp.ClientSession() as session:
                tasks = [asyncio.ensure_future(self.request(session, url)) for url in urls]
                responses = await asyncio.gather(*tasks)
                return responses
        except aiohttp.ClientConnectionError:
            return [[True, f'Error: URL connection error.']]

    def main_process(self, urls: list, layer: int) -> str:
        """Start new process"""
        default = ''
        while layer < 7:
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
        return default

    def primary_search(self, link: str) -> list:
        urls = []
        # Start task
        loop = asyncio.get_event_loop()
        responses = loop.run_until_complete(self.create_tasks([link]))
        # Check
        for response in responses:
            if response[0]:
                return [True, response[1]]
            else:
                urls.extend(response[1])
        return [False, urls]


def run_processes(obj, method_name, urls, layer):
    method = getattr(obj, method_name)
    return method(urls, layer)


def main_search(link: str):
    layer = 0
    while layer < 7:
        # Search
        obj_hitler = HitlerLinksSearch()
        primary_result = obj_hitler.primary_search(link=link)
        # Check
        if primary_result[0]:
            print(f'Result: {primary_result[1]}')
            break
        else:
            # links on page 2 and more
            if len(primary_result[1]) > 1:
                # Data preparation
                urls = primary_result[1]
                nested_list = [urls[:len(urls) // 2], urls[len(urls) // 2:]]
                # Start 2 processes
                with multiprocessing.Pool(processes=2) as pool:
                    results = pool.starmap(run_processes, [(obj_hitler, 'main_process', urls, layer) for urls in nested_list])
                for result in results:
                    if result:
                        print(f'Result: {result}')
                        break
                else:
                    print(f'Result: Hitler`s page not found...')
                break
            else:
                layer += 1


if __name__ == '__main__':
    while True:
        input_link = input('Enter link: ')
        if input_link == '':
            print('Exit...')
            break
        start_time = time.time()
        main_search(input_link)
        print(f'Duration: {time.time() - start_time}')
