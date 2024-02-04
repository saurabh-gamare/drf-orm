from django.shortcuts import render
from django.db import connection
from django.db.models import Q, F, Count, Min, Max, Avg, Sum
import datetime
from .models import Teacher, Student, Blog, Author, Entry

def orm(request):
    posts = Student.objects.all()
    mysql_query = posts.query #Gives the actual database query
    all_mysql_queries_info = connection.queries #Gives extra info about queries like response time


    filter_posts = Student.objects.filter(firstname='Saurabh')
    # print(filter_posts.query)
    filter_posts = Student.objects.filter(firstname__startswith='A')
    # print(filter_posts.query)
    # print(filter_posts)


    filter_posts = Student.objects.filter(firstname__startswith='R') | Student.objects.filter(lastname__startswith='S')
    filter_posts = Student.objects.filter(Q(firstname__startswith='R') | Q(lastname__startswith='S'))
    # Q objects are used to encapsulate collection of keyword arguments (&, |, and ^)
    # print(filter_posts.query)

    filter_posts = Student.objects.filter(Q(firstname__startswith='S') & Q(lastname__startswith='G'))
    filter_posts = Student.objects.filter(firstname__startswith='S', lastname__startswith='G')
    # print(filter_posts.query)

    filter_posts = Student.objects.filter(Q(firstname='Saurabh') & Q(lastname='Gamare'), Q(classroom=1) | Q(classroom=2))

    filter_posts = Student.objects.filter(Q(firstname='Saurabh') & ~Q(lastname='Gamare'))


    print(filter_posts.query)

    context = {'post': filter_posts}
    return render(request, 'index.html', context)


def orm2(request):
    # for i in post:
    #     print(vars(i))
    # whenever there is a join consider the columns of second or first table to be
    # added in the place of ForeignKey column. It will be easier to understand
    post = Entry.objects.exclude(pub_date__gt='2024-01-03', headline="Hello")
    post = Entry.objects.exclude(pub_date__gt='2025-01-03').exclude(headline="Hello")
    post = Entry.objects.aggregate(Count('headline'))
    # aggregate loops through the entire queryset and returns a single value in a dict
    post = Entry.objects.values('headline').annotate(noc=Count('number_of_comments'))
    # annotate aggregates for each item in queryset and returns a queryset
    postq = Entry.objects.annotate(noc=Min('number_of_comments'))
    # In this noc and number_of_comments columns will have same value. Check the mysql query
    post = Blog.objects.annotate(noc=Max('entries__number_of_comments'))
    # In this it will perform the join and we will get valid data. Check mysql query
    post = Entry.objects.values('blog').annotate(noc=Max('number_of_comments'))
    # This is similar to the above query.
    post = Entry.objects.values('blog').annotate(noc=Max('number_of_comments')).filter(noc__gt=20)
    # Filtering the aggregated column is similar to having clause in mysql
    post = Entry.objects.values('authors').annotate(noc=Count('number_of_comments'))
    # In this it will perform a join as authors column is a ManyToManyField. Check mysql query
    post = Entry.objects.values('id', 'headline', 'body_text', 'authors').filter(id=5)
    post = Entry.objects.values('id', 'headline', 'body_text', 'authors').all()
    post = Entry.objects.aggregate(Avg('number_of_comments'))
    post = Entry.objects.aggregate(Sum('number_of_comments'))
    post = Entry.objects.filter(rating__gt=3).aggregate(Sum('number_of_comments'))
    post = Entry.objects.aggregate(Sum('number_of_comments'))
    post = Blog.objects.filter(name='Juices and their benefits').aggregate(Sum('entries__number_of_comments'))
    post = Entry.objects.values('authors').annotate(entry_id=Count('id'))
    # post = Entry.objects.get(id=1)
    # get() method is used only when we want to fetch a single record. It will throw an error if the id is not present
    # post = Entry.objects.filter(number_of_comments__gt=20).filter(rating=2)

    # postq = Entry.objects.prefetch_related('authors').all()
    # Is used in ManyToManyField and prefetch_related uses in operator
    post = Entry.objects.select_related('blog').filter(blog__tagline='Eat healthy juices updated 1')
    # inner joins entry and blog table

    # print(post[0].email, 'post')
    # for data in post:
    #     print(data.blog.tagline)
    # print(post.rating)
    # post.rating = 3
    # post.save()
    post = Entry.objects.all().order_by('number_of_comments')
    post = Entry.objects.all().order_by('-number_of_comments')

    post = Entry.objects.aggregate(Max('number_of_comments'))

    # post = Entry.objects.all().filter(headline__exact='juices')

    post1 = Entry.objects.all().filter(number_of_comments__gt=2)
    post2 = Entry.objects.all().filter(number_of_pingbacks__lt=10)
    post = post1.union(post2)

    post = Entry.objects.values('headline').distinct()

    post = Entry.objects.filter(number_of_comments__in=[2, 5])

    post = Entry.objects.all().order_by('-id')[:1]
    # post = Entry.objects.all().first()

    post = Entry.objects.filter(headline__icontains='Ju')

    post = Entry.objects.get(id=1)
    # print(post.number_of_comments)
    post = Entry.objects.filter(id=1).update(number_of_comments=30)
    postq = Entry.objects.get(id=1)
    # print(post.query)

    query = 'select * from myapp_entry where number_of_comments = 30'
    post = Entry.objects.raw(query)
    # for data in post:
    #     print(data.number_of_comments)

    print(type(postq))

    context = {'post': post}
    return render(request, 'index2.html', context)
