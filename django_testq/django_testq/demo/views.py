import random
from django.http import JsonResponse
from django.shortcuts import render
from django_q.tasks import async_task, schedule


# Create your views here.
def index(request):
    key = random.randint(1, 1000000)
    req = async_task('demo.tasks.task_a', key, "abc", group=f'task_a_for_{key}')
    return JsonResponse({'foo':'bar', 'req': req})