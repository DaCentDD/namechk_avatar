from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .handl_requests import *


def index(request):
    return render(request, 'chk/index.html')


def result(request):
    data = dict()
    if request.method == 'POST':
        nickname = request.POST.get("nick_input", None)
        if not nickname:
            return render(request, 'chk/index.html', data)
        data['nickname'] = nickname
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)
        check_list = [check_youtube, check_twitter, check_insta, check_vk]
        if not os.path.exists("chk/static/chk/img/" + nickname):
            os.mkdir("chk/static/chk/img/" + nickname)
        for check in check_list:
            check(nickname, data, driver)
        check_avatars(data, nickname)
    return render(request, 'chk/index.html', data)


def about(request):
    return render(request, 'chk/about.html')
