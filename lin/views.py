# -*- coding: utf-8 -*-


from django.shortcuts import render_to_response


def reply_to_do_you_love_me(request):
    return render_to_response('do_you_love_me.html')


def reply_to_you_are_the_one(request):
    return render_to_response('you_are_the_one.html')


def reply_to_ppt(request):
    return render_to_response('power_point/my_ppt/ppt.html')


def reply_to_exam(request):
    return render_to_response('exam.html')
