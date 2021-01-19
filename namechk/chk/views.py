from django.shortcuts import render
from msedge.selenium_tools import Edge, EdgeOptions


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
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument('--headless')
        driver = Edge(executable_path=r'D:\Git\namechk_avatar\namechk\msedgedriver.exe', options=options)
        check_list = [check_youtube, check_twitter, check_insta, check_vk]
        if not os.path.exists("chk/static/chk/img/" + nickname):
            os.mkdir("chk/static/chk/img/" + nickname)
        for check in check_list:
            check(nickname, data, driver)
        check_avatars(data, nickname)
    return render(request, 'chk/index.html', data)


def about(request):
    return render(request, 'chk/about.html')
