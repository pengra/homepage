from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from search import models, serializers

from django.core.management import call_command

from datetime import datetime, timedelta


# Create your views here.

class HomePage(TemplateView):
    template_name = "search/index.html"

class QueryAPI(ListAPIView):
    serializer_class = serializers.QuerySerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '').lower().strip()

        suggestions = models.Query.objects.none()

        if query:
            suggestions |= models.Query.objects.filter(stopword=False, query__startswith=query)

        return suggestions

class SearchAPI(ListAPIView):
    serializer_class = serializers.ResultSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '').lower().strip() # what the user typed so far
        force = self.request.query_params.get('force', '').lower() # if user hit "enter"
        hn = self.request.query_params.get('hackernews', '').lower() # if user typed "/hackernews"
        
        wg = self.request.query_params.get('wg', '').lower() # if user typed "/wg"
        
        news = self.request.query_params.get('news', '').lower() # if user typed "/news <query>"

        
        is_scholarly = bool(self.request.query_params.get('scholarly', '')) # is this query scholarly? overrides academic flag
        is_academic = bool(self.request.query_params.get('academic', '')) # is this query academic?
        is_programming = bool(self.request.query_params.get('programming', '')) # is this a programming query?

        results = models.Result.objects.none()

        thirty_mins = datetime.now() - timedelta(hours=0.5)

        if hn:
            query = None
            if force or len(models.Result.objects.filter(hackernews=True, grabbed__gt=thirty_mins)) == 0:
                call_command('hackernews')
            results |= models.Result.objects.filter(hackernews=True)

        elif wg:
            query = None
            if force or len(models.Result.objects.filter(chan=True, grabbed__gt=thirty_mins)) == 0:
                call_command('chan')
            results |= models.Result.objects.filter(chan=True)

        elif news and query:
            if force:
                call_command('newsapi', query)
                results |= models.Query.objects.get(query=query).results.filter(news=True, grabbed__gt=thirty_mins)
            else:
                for suggested in models.Query.objects.filter(stopword=False, query__startswith=query):
                    results |= suggested.results.filter(news=True, grabbed__gt=thirty_mins)
            
        elif is_scholarly and query:
            if force:
                call_command('arxiv', query)
                results |= models.Query.objects.get(query=query).results.all()
            else:
                for suggested in models.Query.objects.filter(stopword=False, query__startswith=query):
                    results |= suggested.results.all()

        elif is_academic and query:
            if force:
                call_command('wiki', query)
                results |= models.Query.objects.get(query=query).results.all()
            else:
                for suggested in models.Query.objects.filter(stopword=False, query__startswith=query):
                    results |= suggested.results.all()

        elif query:
            if force:
                call_command('duckduckgo', query)
                results |= models.Query.objects.get(query=query).results.all()
            else:
                queries = models.Query.objects.filter(stopword=False, query=query)
                if queries:
                    results |= queries[0].results.all()
                else:
                    for suggested in models.Query.objects.filter(stopword=False, query__startswith=query):
                        results |= suggested.results.all()

        order = ['-personal']
        generic = ['-clicks', 'grabbed']

        if is_programming or news:
            order.append('-hackernews')
            order.append('-sx')
        if is_scholarly:
            order.append('-arxiv')
            order.append('-edu')
        elif is_academic:
            order.append('-wiki')
            order.append('-edu')
            order.append('-arxiv')
        elif wg:
            generic.reverse()
        elif hn:
            generic = ['-grabbed']
        else:
            order.append('-duckduckgo')

        results = results.filter(blacklist=False).order_by(*order, *generic).distinct()

        if force and results and not results[0].image:
            try:
                call_command('unsplash', results[0].id, query.split(' ')[0])
            except Exception as e:
                print(e)
                pass # probably reached API limit or whatever
            

        return results


def search_redirect(request, result_id):
    try:
        result = models.Result.objects.get(id=result_id)
        result.clicks += 1
        result.save()
    except models.Result.DoesNotExist:
        return redirect("/")
    return redirect(result.url)
    
