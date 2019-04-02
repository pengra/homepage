from django.db import models

# Create your models here.


class Query(models.Model):
    """
    A query tied to a list of results.
    """
    query = models.CharField(max_length=200, unique=True)
    results = models.ManyToManyField('Result', related_name='queries')
    last_update = models.DateTimeField(auto_now=True)

    is_news_topic = models.BooleanField(
        default=False, help_text="Is this a news topic? - Moves news topics to the top")
    is_academic = models.BooleanField(
        default=False, help_text="Is this an academic topic? - Moves wikipedia articles to the top")
    is_scholarly = models.BooleanField(
        default=False, help_text="Is this a scholarly topic? - Shoves more arxiv articles into search result")
    is_programming = models.BooleanField(
        default=False, help_text="Is this a programming topic? - Moves stackoverflow questions to the top")
    is_cs = models.BooleanField(
        default=False, help_text="Is this a computer science topic? - Moves CS material to the top")

    stopword = models.BooleanField(default=False)  # is this word a stop word?

    @property
    def results_count(self):
        return len(self.results.all())

    def __str__(self):
        return self.query


class Word(models.Model):
    """
    A word for tracking purposes. Made when crawling a page.
    """
    word = models.CharField(max_length=200, unique=True)
    results = models.ManyToManyField('Result', related_name='words')

    # times this word has been found total
    count = models.IntegerField(default=0)
    # number of pages that has this word
    pages = models.IntegerField(default=0)
    nexts = models.ManyToManyField(
        'Word', related_name='prevs')  # trigrams and whatnot


class Result(models.Model):
    """
    A search result.
    """

    scanned = models.BooleanField(default=False)

    url = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)

    title = models.CharField(max_length=255)
    blurb = models.TextField(default="No blurb")
    image = models.ImageField(upload_to='img/', null=True)

    news = models.BooleanField(default=False)

    reddit = models.BooleanField(default=False)

    duckduckgo = models.BooleanField(default=False)
    wiki = models.BooleanField(default=False)
    arxiv = models.BooleanField(default=False)
    semanticscholar = models.BooleanField(default=False)  # semanticscholar.org
    hackernews = models.BooleanField(default=False)
    uw = models.BooleanField(default=False)

    # from stackoverflow or stackexchange
    sx = models.BooleanField(default=False)

    personal = models.BooleanField(default=False)  # added manually

    edu = models.BooleanField(default=False)
    chan = models.BooleanField(default=False)

    grabbed = models.DateTimeField(auto_now=True)
    
    blacklist = models.BooleanField(default=False) # never show

    @property
    def filtered_queries(self):
        return self.queries.filter(stopword=False)

    def __str__(self):
        return self.url
