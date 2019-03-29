from django.core.management.base import BaseCommand, CommandError
from search.models import Result, Query
from django.db.utils import IntegrityError

from django.core.files import File

import requests
import urllib.parse
import json

board = "wg"

class Command(BaseCommand):
    help = 'List all active threads on 4chan/wg/ and show the images'

    _catalog_endpoint = "https://a.4cdn.org/{board}/catalog.json".format(board=board)
    # _image_endpoint = "https://i.4cdn.org/{board}/{tim}.{ext}".format(board=board)
    # _thumb_endpoint = "https://i.4cdn.org/{board}/{tim}s.jpg".format(board=board)
    # _thread_endpoint = "https://a.4cdn.org/{board}/thread/{no}.json".format(board=board)

    def handle(self, *args, **kwargs):
        print("Grabbing /{}/...".format(board))

        for page in requests.get(self._catalog_endpoint).json():
            for thread in page['threads']:
                print("Thread:", thread['no'])
                no = thread['no']
                tim = thread['tim']
                title = thread.get('sub', "/wg/ thread {}".format(no))
                blurb = thread.get('com', "/wg/ thread {}".format(no))
                url = "https://boards.4chan.org/{board}/thread/{no}".format(board=board, no=no)
                result = Result.objects.get_or_create(
                    url=url
                )[0]
                result.title = title
                result.url = url
                result.blurb = blurb
                result.image.save("{}s.jpg".format(tim), File(requests.get("https://i.4cdn.org/{board}/{tim}s.jpg".format(board=board, tim=tim), stream=True).raw))
                result.chan = True
                result.save()
                

