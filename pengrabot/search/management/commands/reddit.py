from django.core.management.base import BaseCommand, CommandError

from search.models import Result, Query
import requests

class Command(BaseCommand):
    help = 'Grab hottest hackernews items'

    _endpoint = "https://www.reddit.com/r/programming.json"

    def handle(self, *args, **kwargs):
        print("Grabbing stories ...", end=' ')
        payload = requests.get(
            self._endpoint,
            headers={'User-Agent':'Pengrabot'}
        ).json()
        stories = payload['data']['children']
        print(len(stories), "stories found.")

        for story_json in stories[:50]:
            if story_json['kind'] != 't3':
                continue

            url = story_json['data']['url']

            story, created = Result.objects.get_or_create(
                url=url
            )

            story.reddit = True

            if created:
                story.title = story_json['data']['title']
                print(story.title)
                author = story_json['data']['author']
                score = story_json['data']['score']
                comments = story_json['data']['num_comments']
                blurb = "/r/programming Post by {by} - {score} points - {comments} comments".format(by=author, score=score, comments=comments)
                if story_json['data']['selftext']:
                    story.blurb = story_json['data']['selftext']
                else:
                    story.blurb = blurb
            
                story.save()

            queries = [Query.objects.get_or_create(query=word)[0] for word in "".join([_ for _ in story.title.lower() if _.isalnum() or _.isspace()]).split(' ') if word]
            queries.append(Query.objects.get_or_create(query=story.title.lower())[0])

            for query in queries:
                query.results.add(story)
                query.save()

            

