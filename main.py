import asyncio
import multiprocessing
import re
import time

import aiohttp
from bs4 import BeautifulSoup


class HitlerLinksSearch:
    async def request(self, session, url: str) -> list:
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

    async def create_tasks(self, urls: list) -> tuple:
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(self.request(session, url)) for url in urls]
            responses = await asyncio.gather(*tasks)
            return responses

    def main_process(self, urls: list) -> str:
        """Start new process"""
        default = ''
        count = 0
        while count < 6:
            # Start tasks
            loop = asyncio.get_event_loop()
            responses = loop.run_until_complete(self.create_tasks(urls))
            urls.clear()
            for response in responses:
                if response[0]:
                    return response[1]
                else:
                    urls.extend(response[1])
            count += 1
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


def run_processes(obj, method_name, urls):
    method = getattr(obj, method_name)
    return method(urls)


if __name__ == '__main__':
    while True:
        input_link = input('Enter link: ')
        if input_link == '':
            print('Exit...')
            break

        # Search
        start_time = time.time()
        obj_hitler = HitlerLinksSearch()
        first_result = obj_hitler.primary_search(link=input_link)
        if first_result[0]:
            print(f'Result: {first_result[1]}')
        else:
            # Data preparation
            urls = first_result[1]
            nested_list = [urls[:len(urls)//2], urls[len(urls)//2:]]
            # Start 2 processes
            with multiprocessing.Pool(processes=2) as pool:
                results = pool.starmap(run_processes, [(obj_hitler, 'main_process', urls) for urls in nested_list])
            for result in results:
                if result:
                    print(f'Result: {result}')
                    break
            else:
                print(f'Result: Hitler`s page not found...')
        print(f'Duration: {time.time() - start_time}')
