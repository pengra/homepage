from django.core.management.base import BaseCommand, CommandError

from search.models import Result, Query
import requests

class Command(BaseCommand):
    help = 'Grab hottest hackernews items'

    _topstories_endpoint = "https://hacker-news.firebaseio.com/v0/topstories.json"
    _details_endpoint = "https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

    def handle(self, *args, **kwargs):
        query = Query.objects.get_or_create(query='!hackernews')[0] # A custom command

        print("Grabbing stories ...", end=' ')
        top_story_ids = requests.get(
            self._topstories_endpoint,
            headers={'User-Agent':'Pengrabot'}
        ).json()
        print(len(top_story_ids), "stories found.")

        for story_id in top_story_ids[:50]:
            story = requests.get(
                self._details_endpoint.format(story_id=story_id),
                headers={'User-Agent':'Pengrabot'}
            ).json()
            
            score = story.get('score', 0)
            comments = len(story.get('kids', []))
            author = story.get('by', "Anonymous")
            title = story.get('title', "No Title")
            try:
                url = story['url']
            except KeyError:
                continue
            
            blurb = "Hackernews Post by {by} - {score} points - {comments} comments".format(by=author, score=score, comments=comments)

            result = Result.objects.get_or_create(
                url=url,
            )[0]
            
            result.blurb = blurb
            result.title = title
            result.hackernews = True
            result.save()

            query.results.add(result)

            

