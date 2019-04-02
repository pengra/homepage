from django.core.management.base import BaseCommand, CommandError
from search.models import Result
from django.core.files import File

import requests
import urllib.parse
from bs4.element import Comment
from bs4 import BeautifulSoup

client_id = "e75afefd605ec3649f9bc8e8d72cf9b8ed1f0395dfc36f2e7291d87084ea6ad9"

class Command(BaseCommand):
    help = 'Tag a result with an image from unsplash'

    _endpoint = "https://api.unsplash.com/search/photos?page=1&client_id={}&query=".format(client_id)

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)
        parser.add_argument('query', type=str)

    def handle(self, *args, **kwargs):
        result = Result.objects.get(id=kwargs['id'])
        response = requests.get(self._endpoint + urllib.parse.quote(kwargs['query'])).json()
        image_name = response['results'][0]['id'] + '.jpg'
        image_url = response['results'][0]['urls']['thumb']
        
        try:
            image = File(requests.get(image_url, stream=True).raw)
        except requests.exceptions.ConnectionError:
            print("Error:", image_url)
        
        print(image_url)
        result.image.save(image_name, image)
        result.clicks += 1
        result.save()
