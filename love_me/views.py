# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, HttpResponse

from k_util.django_util import get_request_body


def reply_to_show_form(request):
    print '====================   get req   ===================='
    return render_to_response('show_form.html')


def reply_to_paper_plane(request):
    req = get_request_body(request)
    return render_to_response('paper_plane.html')
