from django.core.management.base import BaseCommand, CommandError
from search.models import Result, Word

import requests
import urllib.parse
from bs4.element import Comment
from bs4 import BeautifulSoup
import re


class Command(BaseCommand):
    help = 'Read the words/links on a result page. Store results in a database.'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **kwargs):
        if kwargs['id'] < 0:
            results = Result.objects.filter(scanned=False)
        else:
            results = Result.objects.filter(id=kwargs['id'], scanned=False)

        total = len(results)

        for i, result in enumerate(results):
            self.result = result
            self.url = result.url
            self.base_url = "/".join(self.url.split('/')[:3])
            self.domain = urllib.parse.urlparse(self.base_url).netloc
            print("({}/{})".format(i + 1, total), self.url)
            response = requests.get(self.url, headers={
                "User-Agent": "Pengrabot (Contact: nortonjp@uw.edu)"
            })
            soup = BeautifulSoup(response.text, 'html.parser')

            # self.collect_links(soup)
            self.collect_words(soup)

            result.scanned = True
            result.save()

    def collect_links(self, soup):
        anchors = soup.find_all('a', attrs={'href': True})
        for anchor in anchors:
            href = anchor['href']
            if href.startswith('#') or len(href) == 0:
                continue
            elif href.startswith('https://') or href.startswith('http://'):
                domain = Domain.objects.get_or_create(
                    domain=urllib.parse.urlparse(href).netloc,
                )[0]
                url = URL.objects.get_or_create(
                    url=href,
                    domain=domain
                )[0]
            elif href.startswith('//'):
                domain = Domain.objects.get_or_create(
                    domain=urllib.parse.urlparse('https:' + href).netloc,
                )[0]
                url = URL.objects.get_or_create(
                    url='https:' + href,
                    domain= domain
                )[0]
            elif href.startswith('/'):
                domain = self.domain
                url = URL.objects.get_or_create(
                    url=self.base_url + href,
                    domain=self.domain
                )[0]
            elif href.startswith('./'):
                domain = self.domain
                url = URL.objects.get_or_create(
                    url=self.base_url + href[1:],
                    domain=self.domain
                )[0]
            elif href[0].isalpha():
                domain = self.domain
                url = URL.objects.get_or_create(
                    url=self.base_url + '/' + href,
                    domain=self.domain
                )[0]
            elif href.startswith('../'):
                continue

            print(href)
            print(self.url.url, "->", url, href)

            self.result.links_to.add(url)
            self.result.links_to_domains.add(domain)

    def collect_words(self, soup):
        texts = soup.find_all(text=True)
        visible_texts = filter(tag_visible, texts)
        
        title = soup.title
        
        if title and title.string:
            title_text = title.string
            for word in title_text.strip().split(' '):
                word = "".join([_ for _ in word.replace('\n', ' ').replace('\t', ' ').strip().lower() if _ in "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()-=_+[]{},./<>?`~\\|;':\""])
                if word:
                    # print('title:', word)
                    word = Word.objects.get_or_create(
                        word=word
                    )[0]
                    word.count += 1
                    word.save()
                    self.result.words.add(word)

        if visible_texts:
            for texts in visible_texts:
                for word in texts.strip().split(' '):
                    word = "".join([_ for _ in word.replace('\n', ' ').replace('\t', ' ').strip().lower() if _ in "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()-=_+[]{},./<>?`~\\|;':\""])
                    if len(word) == 1 and not word.isalnum():
                        word = ''
                    while word and word[-1] in ">,.?!:;\"']})": # so hello, -> hello
                        word = word[:-1]
                    while word and word[0] in '<[(?"\'':
                        word = word[1:]
                    
                    if word:
                        # print('visible:', word)
                        word = Word.objects.get_or_create(
                            word=word
                        )[0]
                        word.count += 1
                        word.save()
                        self.result.words.add(word)



def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
