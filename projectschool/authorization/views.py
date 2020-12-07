import logging
import os
import socket
import time
import uuid as ud

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import RequestAborted
from django.http import FileResponse
from django.shortcuts import HttpResponse, render, redirect
from django.views.generic import View
from psycopg2 import IntegrityError

from . import services
from .models import *

logger = logging.getLogger(__name__)


# TODO на главной странице, чтобы при нажатии на кнопки создать комнату, подключиться, итд было слева, что вписывать("введите пароль для вашей комнаты", что-то типа того)


class Index(View):

    def get(self, request):
        print(request.GET)
        if request.user.is_authenticated:
            user_code = CodesConnecting.objects.get(username=request.user)
            user = User.objects.get(username=request.user)
            return render(request, "loginForm/main.html",
                          {"username": {'first_name': user.first_name, 'last_name': user.last_name},
                           "code": user_code.code})

        else:
            return redirect("/accounts/login")

    def post(self, request):
        print(request.POST)
        if 'username' in request.POST:
            change_username(request)
            return redirect("/")
        elif 'password' in request.POST:
            change_password(request)
            return redirect("/")
        elif 'connecting_key' in request.POST:
            logger.info("connecting_key " + request.POST.get("connecting_key"))
            user = CodesConnecting.objects.get(code=request.POST.get("connecting_key"))
            if user is not None:
                return redirect(f'/room/{user.uuid}')
            else:
                return HttpResponse('пользователя не существует!')
        elif 'set_password_session' in request.POST:
            logger.info("password_session:" + request.POST["set_password_session"])
            set_password_room(request.POST['set_password_session'], request.user)
            user = CodesConnecting.objects.get(username=request.user)
            uuid_user = user.uuid
            try:
                host_room = Rooms.objects.get(host=request.user, room=user.code)
                if host_room:
                    pass
                else:
                    Rooms(host=request.user, room=user.code).save()
            except Rooms.DoesNotExist:
                Rooms(host=request.user, room=user.code).save()

            return redirect(
                f'/room/{uuid_user}/change_file?pwd={uuid.uuid5(ud.NAMESPACE_DNS, request.POST["set_password_session"])}')
        elif 'logout' in request.POST:
            if request.user.is_authenticated:
                logout(request)
            return redirect('/accounts/login')


class LoginForm(View):
    def get(self, request):
        return render(request, "loginForm/index.html")

    def post(self, request):
        username: str = request.POST.get('username')
        password: str = request.POST.get('password')
        print(request.POST)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                set_unique_code(username, services.change_tempo_code())
                return redirect('/')
            except CodesConnecting.DoesNotExist:
                logger.error("записи " + username + " не существует")
                return HttpResponse("Ошибка сервера")
            except Exception as e:
                logger.error("не известная ошибка " + "{" + str(e) + "}")
                return HttpResponse("Неизвестная ошибка!")
        else:
            logger.info(username + "пытался войти в аккаунт")
            return HttpResponse("Пользователя не существует!")


class RegistrationUser(View):
    def get(self, request):

        return render(request, 'loginForm/register.html')

    def post(self, request):

        print(request.POST)

        try:
            username: str = request.POST.get('username')
            email: str = request.POST.get('email')
            password: str = request.POST.get('password')
            services.registration_user(username, email, password)
            try:
                services.add_record_table_unique_codes(username)
                return redirect('./login')
            except Exception as e:
                logger.error("ошибка: ", e)
        except IntegrityError:
            logger.error("Такой пользователь существует!")
            return HttpResponse("Такой пользователь существует!")
        except RequestAborted:
            logger.error("Соединение закрыто или тайм-аут просрочен!")
            return HttpResponse("Соединение закрыто или тайм-аут просрочен!")
        except Exception as e:
            logger.error("ошибка: ", e)
            return HttpResponse("неизвестная ошибка")


class CheckPassword(View):
    def get(self, request, uuid):
        print(request.GET)
        try:
            user = CodesConnecting.objects.get(uuid=uuid)
            del user
            return render(request, 'changingForm/check_password.html')
        except CodesConnecting.DoesNotExist:
            return HttpResponse("Пользователя с таким ID не существует!")

    def post(self, request, uuid):
        print(request.POST)
        password = request.POST.get("password")
        try:
            passwd = CodesConnecting.objects.get(uuid=uuid)
            uuid_key = str(ud.uuid5(ud.NAMESPACE_DNS, password))
            print(passwd.tempo_password_room, uuid_key)
            if uuid_key == str(passwd.tempo_password_room):
                return redirect(f"/room/{uuid}/change_file?pwd={uuid_key}")
            else:
                return HttpResponse("пароль не верен")
        except CodesConnecting.DoesNotExist:
            logger.error(str(uuid) + " отсутсвует в базе данных!")
            return HttpResponse("Пользователя с таким ID не существует!")


class ChangeFiles(View):
    def get(self, request, uuid):

        print(request.GET.get("pwd"))
        logger.info(request.user)
        try:
            if 'pwd' in request.GET:
                user = CodesConnecting.objects.get(uuid=uuid)
                if user.tempo_password_room == request.GET.get('pwd'):
                    user = CodesConnecting.objects.get(uuid=uuid)
                    file_data = create_dict_data(user)
                    if file_data[0] is not None:
                        user = Rooms.objects.get(host=CodesConnecting.objects.get(uuid=uuid).username)
                        logger.info(str(str(user.host) == str(request.user)) + " " + user.room)
                        if str(user.host) == str(request.user):

                            return render(request, 'changingForm/change_file.html',
                                          {'data': file_data[1], 'code': user.room})
                        else:
                            return render(request, 'changingForm/change_file.html',
                                          {'data': file_data[1], 'code': None})
                    else:
                        user = Rooms.objects.get(host=CodesConnecting.objects.get(uuid=uuid).username)
                        logger.info(str(str(user.host) == str(request.user)) + " " + user.room)
                        if user.host == request.user:

                            return render(request, 'changingForm/change_file.html', {'code': user.room})
                        else:
                            return render(request, 'changingForm/change_file.html',
                                          {'code': None})
                else:
                    return redirect(f'/room/{uuid}')
            else:
                return redirect(f'/room/{uuid}')
        except CodesConnecting.DoesNotExist:
            return HttpResponse("Пользователя с таким ID не существует!")

    def post(self, request, uuid):
        print(request.POST, request.FILES)
        try:
            if 'downloading_file' in request.POST:
                return FileResponse(open('/users_files/' + request.POST['downloading_file'], 'rb'))
            elif 'exit-button' in request.POST:
                exit_from_room(request, uuid)
                return redirect('/')

            elif 'file_input' in request.FILES:
                for x in range(0, len(request.FILES.getlist('file_input'))):
                    file = URLsUsersFiles(
                        url=content_file_name(str(uuid),
                                              (request.FILES.getlist('file_input')[x].name + str(time.time()))),
                        really_name_file=request.FILES.getlist('file_input')[x].name,
                        id_room=CodesConnecting.objects.get(uuid=uuid).code)
                    file.save()
                    print(request.FILES.getlist('file_input')[x])
                    handle_uploaded_file(request.FILES.getlist('file_input')[x], file.url, uuid)
            user = CodesConnecting.objects.get(uuid=uuid)
            file_data = create_dict_data(user)
            if file_data[0] is not None:
                return render(request, 'changingForm/change_file.html', {'data': file_data[1]})
            else:
                return render(request, 'changingForm/change_file.html')
        except socket.error:
            exit_from_room(request, uuid)
            return redirect('/')


class ProfileHandler(View):
    def get(self, request):
        services.add_record_table_unique_codes(username=request.user)
        return redirect('/')


def change_password(request):
    user = User.objects.get(username=request.user)
    user.set_password(request.POST.get('password'))
    user.save()


def change_username(request):
    try:
        user = User.objects.get(username=request.user)
        user.username = request.POST.get('username')
        user.save()
        user_object = CodesConnecting.objects.get(username=request.user)
        user_object.username = request.POST.get("username")
        user_object.save()
    except IntegrityError:
        logger.error("ошибка: ", IntegrityError)


def set_unique_code(username, generated_code: int):
    user = CodesConnecting.objects.get(username=username)
    user.code = generated_code
    user.save()


def set_password_room(password, username):
    passwd = CodesConnecting.objects.get(username=username)
    passwd.tempo_password_room = ud.uuid5(ud.NAMESPACE_DNS, password)
    passwd.save()


def handle_uploaded_file(f, uuid_name, uuid):
    filename, file_extension = os.path.splitext(f.name)
    path = uuid_name.name + file_extension
    print(os.getcwd())
    tempo_code = str(CodesConnecting.objects.get(uuid=uuid).code)
    if os.path.isdir(os.getcwd() + '/users_files/' + tempo_code) is False:
        os.mkdir(os.getcwd() + '/users_files/' + tempo_code)
        create_user_file(path, f)
    else:
        create_user_file(path, f)


def create_user_file(path, f):
    print(path)
    with open(os.getcwd() + path, 'wb+') as destination:
        save_file_from_chunk(destination, f)


def save_file_from_chunk(file, data):
    for chunk in data.chunks():
        file.write(chunk)


def create_dict_data(user):
    file_data = URLsUsersFiles.objects.filter(id_room=user.code)

    if file_data is not None:
        data = {}
        num = 0
        for _ in file_data:
            uuid_filename = str(file_data[num].url).split('/')[-1]
            real_filename = file_data[num].really_name_file
            filename, file_extension = os.path.splitext(real_filename)
            id_room = user.code
            data[real_filename] = {'uuid_filename': uuid_filename, 'id_room': id_room,
                                   "file_extension": str(file_extension)}
            num += 1
        print(data)
        return file_data, data


def exit_from_room(request, uuid):
    print(request.POST)
    host = Rooms.objects.get(room=CodesConnecting.objects.get(uuid=uuid).code)
    print(host.host)
    print(host.host, ' ', request.user)
    print(str(host.host) == str(request.user))
    if str(host.host) == str(request.user):

        user = CodesConnecting.objects.get(username=request.user, uuid=uuid)
        user.tempo_password_room = None
        user.save()
        host.delete()


