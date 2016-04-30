# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, HttpResponse


@csrf_exempt
def reply_to_one_page(request):
    return render_to_response('music_rss/one_page.html')

if __name__ == '__main__':
    reply_to_one_page('1234')
