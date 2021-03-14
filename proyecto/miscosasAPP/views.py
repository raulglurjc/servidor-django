from django.shortcuts import render, redirect
from .apikeys import LASTFM_APIKEY
from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from .models import Database_Users, Alimentador, Item, Comentario, Voto
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from xml.sax import make_parser
from django.utils import timezone
from .parser import YTHandler, LastfmHandler
from django.core import serializers
import urllib.request
# Create your views here.
class LoginForm(forms.Form):
    Username = forms.CharField()
    Password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    Username = forms.CharField()
    Email = forms.EmailField()
    Password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    image = forms.ImageField(required=False)

def principal(request):
    try:
        user = request.user.username
        usuario = User.objects.get(username=user)
        if(usuario.night ==True):
            noche("miscosasAPP/templates/miscosasAPP/principal.html")
            return render(request, 'miscosasAPP/principal.html')
        else:
            dia("miscosasAPP/templates/miscosasAPP/principal.html")
            return render(request, 'miscosasAPP/principal.html')
    except User.DoesNotExist:
        dia("miscosasAPP/templates/miscosasAPP/principal.html")
        return render(request, 'miscosasAPP/principal.html')

def index(request):
    items =Item.objects.all()
    for item in items:
        item.popularidad = item.likes - item.dislikes
        item.save()

    top = Item.objects.all().order_by('-popularidad')[:10]

    youtube = Alimentador.objects.filter(tipo_alimentador="youtube", seleccionado=True)
    lastfm = Alimentador.objects.filter(tipo_alimentador="lastfm", seleccionado=True)
    user = request.user.username
    if user:
        try:
            user = Database_Users.objects.get(username=user)
        except Database_Users.DoesNotExist:
            user = Database_Users(username=user)
            user.save()

        votos_usuario = Voto.objects.filter(usuario=user)
        top5 = votos_usuario.order_by('-id')[:5]
        context = {"youtube": youtube,
                   "lastfm": lastfm,
                   "top": top,
                   "top5_aux":top5}
    else:
        context = {"youtube": youtube,
                   "lastfm": lastfm,
                   "top": top}


    if request.method == "POST":
        action = request.POST['tipo_alimentador']
        if action == "youtube" or "lastfm":
            clave = request.POST['clave']
            Parser = make_parser()
            if action == "youtube":
                id = clave
                Parser.setContentHandler(YTHandler())
                url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' \
                + id
            elif action == "lastfm":
                id = clave.replace(" ", "%20")
                Parser.setContentHandler(LastfmHandler())
                url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist=' + id + '&api_key=' + LASTFM_APIKEY
            try:
                xmlStream = urllib.request.urlopen(url)
                Parser.parse(xmlStream)
                alimentador = Alimentador.objects.get(clave=id)
                if action =="youtube":
                        return redirect('youtube/'+id)
                elif action == "lastfm":
                    return redirect('lastfm/'+id)

            except:
                if action =="youtube":
                    context['error_last']=id
                elif action == "lastfm":
                    context['error_last']=clave
                return render(request, 'miscosasAPP/index.html', context)

    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'miscosasAPP/index.xml', context, content_type='text/xml')
        if format == 'json':
            list = [*top, *youtube, *lastfm]
            if user:
                list = [*top,*top5, *youtube, *lastfm]
            lista = serializers.serialize('json', list)
            return HttpResponse(lista, content_type="application/json")
        return render(request, 'miscosasAPP/index.html', context)



def Deselect(request,tipo,identificador, pagina):
        if request.method == "POST":
            alimentador = Alimentador.objects.get(clave=identificador)
            alimentador.seleccionado = not alimentador.seleccionado
            alimentador.save()
            if pagina == "alimentadores":

                return redirect('alimentadores')
            elif pagina == "alimentador":
                return redirect("/miscosas/"+tipo+'/'+identificador)

            elif pagina =="Principal":
                return redirect('index')

def Select(request,tipo,identificador, pagina):
    if request.method == "POST":
        alimentador = Alimentador.objects.get(clave=identificador)
        alimentador.seleccionado = not alimentador.seleccionado
        alimentador.save()
        if pagina == "alimentadores":

            return redirect('alimentadores')
        elif pagina == "alimentador":
            print(tipo+'/'+identificador)
            return redirect("/miscosas/"+tipo+'/'+identificador)



def alimentador_yt(request, llave):
    alimentador = Alimentador.objects.get(clave=llave)
    items = Item.objects.filter(alimentador=alimentador)
    context = {'alimentador':alimentador,
                'items':items}

    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'miscosasAPP/alimentador.xml', context, content_type='text/xml')
        if format == 'json':
            list = [alimentador, *items]
            lista = serializers.serialize('json', list)
            return HttpResponse(lista, content_type="application/json")
    return render(request, 'miscosasAPP/alimentador_yt.html', context)

def alimentador_lastfm(request, llave):
    try:
        alimentador = Alimentador.objects.get(clave=llave)
    except:
        return render(request, 'miscosasAPP/404.html')
    items = Item.objects.filter(alimentador=alimentador)
    context = {'alimentador':alimentador,
                'items':items}
    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'miscosasAPP/alimentador.xml', context, content_type='text/xml')
        if format == 'json':
            list = [alimentador, *items]
            lista = serializers.serialize('json', list)
            return HttpResponse(lista, content_type="application/json")
    return render(request, 'miscosasAPP/alimentador_lastfm.html', context)

def item(request, tipo, identificador, item):
    alimentador = Alimentador.objects.get(clave=identificador)
    item_aux = item
    Items = Item.objects.get(clave=item)
    user = request.user.username
    context = {'alimentador':alimentador,
                'item':Items,
                'tipo': tipo}
    try:
        user = Database_Users.objects.get(username=user)
    except:
        try:
            user = User.objects.get(username=user)
        except:
            render(request, 'miscosasAPP/item.html', context)
    if request.method == "POST":
        try:

            comentario = request.POST['comentario']
            c = Comentario(usuario=user, fecha=timezone.now(), cuerpo=comentario, item=Items)
            c.save()
        except:
            action = request.POST['action']


            if action == "like":
                try:
                    v = Voto.objects.get(usuario=user, item=Items)
                    if v.estado == "dislike":
                        Items.likes = Items.likes + 1
                        Items.dislikes = Items.dislikes - 1
                        Items.save()
                    v.estado = "like"
                    v.save()
                except Voto.DoesNotExist:
                    Items.likes = Items.likes + 1
                    Items.save()
                    v = Voto(usuario=user, item=Items, estado="like")
                    v.save()
            elif action =="dislike":
                try:
                    v = Voto.objects.get(usuario=user, item=Items)
                    if v.estado == "like":
                        Items.likes = Items.likes - 1
                        Items.dislikes = Items.dislikes + 1
                        Items.save()
                    v.estado = "dislike"
                    v.save()
                except Voto.DoesNotExist:
                    Items.dislikes = Items.dislikes + 1
                    Items.save()
                    v = Voto(usuario=user, item=Items, estado="dislike")
                    v.save()
            a = Alimentador.objects.get(clave=identificador)
            items = Item.objects.filter(alimentador=a)
            for item in items:
                item.popularidad = item.likes - item.dislikes
                item.save()
            votospos = 0
            votosne = 0
            for votos in items:
                votospos = votos.likes + votospos
                votosne = votos.dislikes + votosne

            puntuacionAlimentador = votospos - votosne
            a.puntuacion = puntuacionAlimentador
            a.save()







    try:
        comments = Comentario.objects.filter(item__clave=item_aux)
        context['comment'] = comments
    except:
        print()

    try:
        voto = Voto.objects.get(usuario=user, item=Items)
        context['voto'] = voto
    except:
        print("ha fallado")
    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'miscosasAPP/item.xml', context, content_type='text/xml')
        if format == 'json':
            list = [a, i]
            if user:
                list = [alimentador, Items,*comentarios]
            lista = serializers.serialize('json', list)
            return HttpResponse(lista, content_type="application/json")
    return render(request, 'miscosasAPP/item.html', context)



def alimentadores(request):
    youtube = Alimentador.objects.filter(tipo_alimentador="youtube")
    lastfm = Alimentador.objects.filter(tipo_alimentador="lastfm")
    context={"youtube": youtube,
             "lastfm": lastfm}

    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'miscosasAPP/alimentadores.xml', context, content_type='text/xml')
        if format == 'json':
            list = [*youtube, *lastfm]
            lista = serializers.serialize('json', list)
            return HttpResponse(lista, content_type="application/json")
    return render(request, 'miscosasAPP/alimentadores.html',context)



def info(request):

    return render(request, 'miscosasAPP/info.html')


def logout_reg(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def login_reg(request):
    form = LoginForm()

    if request.method == "GET":
        return render(request, 'miscosasAPP/login.html')
    if request.method == "POST":
        form = LoginForm(request.POST,request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['Username']
            contraseña = form.cleaned_data['Password']
            user = authenticate(request, username=nombre, password=contraseña)

            if user:
                login(request, user)
                return redirect('index')
            else:
                context={'error': "Usuario o contraseña incorrectos, prueba otra vez."}
                return render(request, 'miscosasAPP/login.html', context)

def registro(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['Username']
            email = form.cleaned_data['Email']
            contraseña = form.cleaned_data['Password']

            try:
                superUser = User.objects.get(username=nombre)
                context = {'usuario': nombre}
                return render(request, 'miscosasAPP/registro.html', context)
            except User.DoesNotExist:
                try:
                    user = Database_Users.objects.get(username=nombre)
                    context = {'usuario': nombre}
                    return render(request, 'miscosasAPP/registro.html', context)
                except Database_Users.DoesNotExist:
                    usuario = Database_Users(username=nombre, email=email, password=contraseña)
                    usuario.save()
                    usuario = User.objects.create_user(username=nombre, email=email, password=contraseña)

                    usuario.save()
                    if usuario:
                        login(request,usuario)
                    return redirect('index')

    return render(request, 'miscosasAPP/registro.html')


def usuarios(request):
    usuarios = User.objects.all()
    context = {'users':usuarios}


    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'miscosasAPP/usuarios.xml', context, content_type='text/xml')
        if format == 'json':
            list = [*usuarios]
            list = serializers.serialize('json', list, fields=['username','email'])
            return HttpResponse(list, content_type="application/json")
    return render(request, 'miscosasAPP/usuarios.html', context)

def usuario(request, usuario):
    user = Database_Users.objects.get(username=usuario)
    comentarios = Comentario.objects.filter(usuario=user)
    votos=Voto.objects.filter(usuario=user)
    context = {'usuario':user,
                'comentarios':comentarios,
                'votos':votos}
    if user.username == request.user.username:
        sameuser = True
        context['bienvenido'] = sameuser


    if request.method == "POST":
        action = request.POST['fileToUpload']
        user.image=action
        user.save()
    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'miscosasAPP/user.xml', context, content_type='text/xml')
        if format == 'json':
            list = [user,*votos,*comentarios]
            list = serializers.serialize('json', list)
            return HttpResponse(list, content_type="application/json")
    return render(request, 'miscosasAPP/usuario.html', context)

def noche(a):
	old = "<body>"
	new = "<body class=\"night\">"
	archivo = open(a, 'r')
	string = archivo.read()
	archivo.close()
	if(string.find("<body>")!=-1):
		archivo = open(a, 'w')
		archivo.write(string.replace(old, new))
		archivo.close()
def dia(a):
	old = "<body class=\"night\">"
	new = "<body>"
	archivo = open(a, 'r')
	string = archivo.read()
	archivo.close()
	if(string.find("<body class=\"night\">")!=-1):
		archivo = open(a, 'w')
		archivo.write(string.replace(old, new))
		archivo.close()


def prueba(request):

	try:
		user = request.user.username
		usuario = User.objects.get(username=user)
		if(usuario.night ==True):
			noche("miscosasAPP/templates/miscosasAPP/prueba.html")
			return render(request, 'miscosasAPP/prueba.html')
		else:
			dia("miscosasAPP/templates/miscosasAPP/prueba.html")
			return render(request, 'miscosasAPP/prueba.html')
	except User.DoesNotExist:
		dia("miscosasAPP/templates/miscosasAPP/prueba.html")
		return render(request, 'miscosasAPP/prueba.html')



def prueba_reg(request):
	if request.method == "POST":
		usuario = request.POST.get("usuario")
		passwd = request.POST.get("passwd")
		email = request.POST.get("email")
		try:
			superUser = User.objects.get(username=usuario)
			context = {'usuario': usuario}
			return render(request, 'miscosasAPP/prueba_reg.html', context)
		except User.DoesNotExist:
			usuario = User.objects.create_user(username=usuario, email=email, password=passwd)
			usuario.save()
			if usuario:
				login(request,usuario)
			return redirect('prueba')
	if request.method == "GET":
		try:
			user = request.user.username
			usuario = User.objects.get(username=user)
			if(usuario.night ==True):
				return render(request, 'miscosasAPP/prueba_reg.html')
			else:
				return render(request, 'miscosasAPP/prueba_reg.html')
		except User.DoesNotExist:
			return render(request, 'miscosasAPP/prueba_reg.html')

def prueba_log(request):
	if request.method == "POST":
		usuario = request.POST.get("usuario")
		passwd = request.POST.get("passwd")
		user = authenticate(request, username=usuario, password=passwd)
		if user:
			login(request, user)
			return redirect('prueba')
		else:
			context={'usuario': usuario}
			return render(request, 'miscosasAPP/prueba-log.html', context)

	if request.method == "GET":
		try:
			user = request.user.username
			usuario = User.objects.get(username=user)
			if(usuario.night ==True):
				return render(request, 'miscosasAPP/prueba-log.html')
			else:
				return render(request, 'miscosasAPP/prueba-log.html')
		except User.DoesNotExist:
			return render(request, 'miscosasAPP/prueba-log.html')

def prueba_users(request):

	if request.method == "GET":

		try:
			usuarios = User.objects.all()
			context = {'users':usuarios}
			user = request.user.username
			usuario = User.objects.get(username=user)
			if(usuario.night ==True):
				return render(request, 'miscosasAPP/prueba-users.html', context)
			else:
				return render(request, 'miscosasAPP/prueba-users.html', context)
		except User.DoesNotExist:
			return render(request, 'miscosasAPP/prueba-users.html', context)

def night(request):

	user = request.user.username
	usuario = User.objects.get(username=user)
	if(usuario.night == True):
		usuario.night = False
	else:
		usuario.night = True


	usuario.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def glow_box(request):

    return render(request, 'miscosasAPP/glow_box.html')
