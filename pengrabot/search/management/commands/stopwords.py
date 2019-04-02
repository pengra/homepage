from django.core.management.base import BaseCommand, CommandError

from search.models import Query, Result

import glob
import requests
from bs4 import BeautifulSoup
import os

class Command(BaseCommand):
    help = 'Given a large blob of text, get all stop words and mark them so in the database.'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)
        parser.add_argument('threshold', type=float)
        parser.add_argument('scrapes', type=int)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        threshold = kwargs['threshold']
        scrapes = kwargs['scrapes']

        results = Result.objects.all()
        index = -1

        word_bank = {}
        total = 0

        for _ in range(scrapes):
            id = None
            new_file_path = os.path.join(path, str(id) + '.txt')

            try:
                while id is None or os.path.isfile(new_file_path):
                    index += 1
                    r = results[index]
                    new_file_path = os.path.join(path, str(id) + '.txt')
                    id = r.id
            except IndexError:
                print("No more scrapes available")
                break

            print("Scraping", r.url, end=" ... ")
            
            with open(new_file_path, 'w') as handle:
                response = requests.get(r.url, headers={
                    "User-Agent": "Pengrabot (Contact: nortonjp@uw.edu)"
                })
                if 'text' in response.headers['content-type']:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    texts = " ".join([_.get_text(separator=' ').replace('\n', ' ').strip() for _ in soup.find_all('p', text=True)])

                    if texts:
                        handle.write(texts)
                
                    print(len(texts.split(' ')), " words")
                
                else:
                    print("Unacceptable File Format:", response.headers['content-type'])

        for file_path in glob.glob(path + '*.txt'):
            with open(file_path) as handle:
                words = [_.strip() for _ in "".join([_ for _ in handle.read().lower().replace("\n", " ") if _.isalpha() or _.isspace()]).split(" ")]

            for word in words:
                if word:
                    word_bank.setdefault(word, 0)
                    word_bank[word] += 1
                    total += 1

        stopwords = [(_[0], _[1] * 100 / total) for _ in sorted(word_bank.items(), key=lambda i: i[1]) if _[1] >= (threshold * total)]

        for q in Query.objects.filter(stopword=True):
            q.stopword = False
            q.save()

        for stopword, rate in stopwords:
            print("Ignoring '{}' @ {:.3f}%".format(stopword, rate))
            q = Query.objects.get_or_create(query=stopword)[0]
            q.stopword = True
            q.save()