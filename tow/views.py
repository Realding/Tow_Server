from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from tow import models
from tow.forms import UserForm, RegisterForm


def sim(request):
    return render(request, 'sim.html')

def wait(request):
    if request.session.get('is_login', None):
        user = models.UserInfo.objects.get(username=request.session['user_name'])
        p = models.PlayerOnGame.objects.get(user=user)
        p.on_wait = True
        p.save()
        players = models.PlayerOnGame.objects.filter(game=(models.PlayerOnGame.objects.get(user=user).game))
        need_wait = False
        for player in players:

            if not player.on_wait:
                need_wait = True

        if not need_wait:
            return redirect("/game/")
    return render(request, 'wait.html')


def index(request):
    if request.session.get('is_login', None):
        if request.GET.get('back',None):
            try:
                player = models.PlayerOnGame.objects.get(user__username=request.session['user_name'])
                player.ready = False
                player.save()
                user = models.UserInfo.objects.get(username=request.session['user_name'])
                user.on_game = False
                user.save()
                user = models.UserInfo.objects.get(username=request.session['user_name'])
                p = models.PlayerOnGame.objects.get(user=user)
                game = p.game
                game.player_number -= 1
                game.full = False
                p.delete()
                game.save()

                user.on_game = False
                user.save()
            except:
                print("数据库退出异常")

    return render(request, 'index.html')


def ready(request):
    if request.session.get('is_login', None):
        user = models.UserInfo.objects.get(username=request.session['user_name'])
        mode = request.GET.get("mode", 1)
        request.session['mode'] = mode
        if not user.on_game:
            # 创建进入游戏
            m_game = models.GameInfo.objects.get(game_mode=mode)
            if m_game.full:
                return HttpResponse("游戏玩家已满")
            # m_game.game_mode = mode
            new_player = models.PlayerOnGame.objects.create(game=m_game, user=user)
            m_game.player_number += 1
            if m_game.player_number == m_game.max_game_number:
                m_game.full = True
            user.on_game = True
            m_game.save()
            user.save()

        players = models.PlayerOnGame.objects.filter(game=(models.PlayerOnGame.objects.get(user=user).game))

    return render(request, 'ready_room.html',locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.UserInfo.objects.get(username=username)

                if user.password == password:
                    # if user.on_game:
                    #     message = "用户已经登录！"
                    # else:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    return redirect("/index/")
                else:
                    message = "密码不正确！"
            except Exception as e:
                print(e)
                message = "用户名不存在！"
            return render(request, 'login.html', locals())
    login_form = UserForm()
    return render(request, 'login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")

    # 用户退出游戏
    try:
        user = models.UserInfo.objects.get(username=request.session['user_name'])
        p = models.PlayerOnGame.objects.get(user=user)
        game = p.game
        game.player_number -= 1
        game.full = False
        p.delete()
        game.save()

        user.on_game = False
        user.save()
    except:
        print("数据库退出异常")

    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.UserInfo.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.UserInfo.objects.create()
                new_user.username = username
                new_user.password = password1
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'register.html', locals())

def clean_data(request):
    if request.session.get('is_login', None):
        try:
            user = models.UserInfo.objects.get(username=request.session['user_name'])
            player = models.PlayerOnGame.objects.get(user=user)
            game = player.game
            game.player_number -= 1
            game.full = False
            player.delete()
            game.save()

            user.on_game = False
            user.save()
        except:
            print("数据库退出异常")
    return HttpResponse('finish')


def ajax_get_data(request):
    adict={}
    if request.session.get('is_login', None):

        user = models.UserInfo.objects.get(username=request.session['user_name'])
        players = models.PlayerOnGame.objects.filter(game=(models.PlayerOnGame.objects.get(user=user).game))
        total = 0
        for player in players:
            total += player.shake_times
        adict['total'] = total
        if(total !=0 ):
            for player in players:
                adict[player.user.username] = player.shake_times
        print('ajax', adict)

    return JsonResponse(adict, safe=False)


def ajax_get_ready_data(request):
    ready_dict={}
    if request.session.get('is_login', None):

        user = models.UserInfo.objects.get(username=request.session['user_name'])
        players = models.PlayerOnGame.objects.filter(game=(models.PlayerOnGame.objects.get(user=user).game))
        for player in players:
            ready_dict[player.user.username] = player.ready
        ready_dict['username'] = user.username
    return JsonResponse(ready_dict, safe=False)


# 数据接口
def data_port(request):
    if request.method == 'POST':
        if request.session.get('is_login', None):
            username = request.session.get('user_name', None)
            user = models.UserInfo.objects.get(username=username)
            if not user.on_game:
                return HttpResponse("请先进入游戏！")
            shake_times = request.POST.get('shake_times')
            m_player = models.PlayerOnGame.objects.get(user=user)
            m_player.shake_times = shake_times
            m_player.save()
            # m_game = m_player.game
            # players = models.PlayerOnGame.objects.filter(game=m_game)

            # if m_game.game_mode == 1:

                # total = 0
                # for player in players:
                #     total += player.shake_times
                # for player in players:
                #     player.percent = round(player.shake_times*100 / total, 2)
                #     player.save()
            return HttpResponse("数据发送成功!")
            # return redirect('/game/')
        else:
            return HttpResponse("未登录用户，请先登录!")
    else:
        return HttpResponse("请求方法错误！")


#游戏界面
def game(request):
    if request.session.get('is_login', None):
        username = request.session.get('user_name', None)
        user = models.UserInfo.objects.get(username=username)
        mode = request.session.get("mode", 1)


        m_player = models.PlayerOnGame.objects.get(user=user)
        m_game = m_player.game
        players = models.PlayerOnGame.objects.filter(game=m_game)
        print("game return")
        return render(request, 'game.html', {'username': username, 'players': players})
    else:
        print("未登录用户")
        login_form = UserForm()
        message = "请先登录!"
        return render(request, 'login.html', locals())


def be_ready(request):
    if request.session.get('is_login', None):
        player = models.PlayerOnGame.objects.get(user__username=request.session['user_name'])
        player.ready = not player.ready
        player.save()

    return redirect("/ready/")