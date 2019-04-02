from django.core.management.base import BaseCommand, CommandError

from search.models import Result, Query
import requests

class Command(BaseCommand):
    help = 'Grab hottest hackernews items'

    _topstories_endpoint = "https://hacker-news.firebaseio.com/v0/topstories.json"
    _details_endpoint = "https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

    def handle(self, *args, **kwargs):
        print("Grabbing stories ...", end=' ')
        top_story_ids = requests.get(
            self._topstories_endpoint,
            headers={'User-Agent':'Pengrabot'}
        ).json()
        print(len(top_story_ids), "stories found.")

        for story_id in top_story_ids[:50]:
            print("Grabbing story id:", story_id)
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
            
            queries = [Query.objects.get_or_create(query=word)[0] for word in "".join([_ for _ in title.lower() if _.isalnum() or _.isspace()]).split(' ') if word]
            queries.append(Query.objects.get_or_create(query=title.lower())[0])

            blurb = "Hackernews Post by {by} - {score} points - {comments} comments".format(by=author, score=score, comments=comments)

            result = Result.objects.get_or_create(
                url=url,
            )[0]
            
            result.blurb = blurb
            result.title = title
            result.hackernews = True
            result.save()

            for query in queries:
                query.results.add(result)
                query.save()

            

