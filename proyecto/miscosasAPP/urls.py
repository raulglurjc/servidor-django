from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal,name='principal'),
    path('principal/', views.principal,name='principal'),
    path('info/', views.info,name='info'),
    path('prueba/', views.prueba,name='prueba'),
    path('night/', views.night,name='night'),
    path('prueba_reg/', views.prueba_reg,name='prueba_reg'),
    path('prueba_log/', views.prueba_log,name='prueba_log'),
    path('prueba_users/', views.prueba_users,name='prueba_users'),
    path('glow_box/', views.glow_box,name='glow_box'),
    path('registro/', views.registro,name='registro'),
    path('logout/', views.logout_reg,name='logout_reg'),
    path('login/', views.login_reg,name='logout_reg'),
    path('usuarios/', views.usuarios,name='usuarios'),
    path('usuarios/<str:usuario>', views.usuario,name='usuario'),
    path('alimentadores/', views.alimentadores,name='alimentadores'),
    path('youtube/<str:llave>', views.alimentador_yt, name='alimentador_yt'),
    path('lastfm/<str:llave>', views.alimentador_lastfm, name='alimentador_lastfm'),
    path('<str:tipo>/<str:identificador>/<str:item>', views.item, name='item'),
    path('<str:tipo>/<str:identificador>/Deselect/<str:pagina>', views.Deselect, name='Deselect'),
    path('<str:tipo>/<str:identificador>/Select/<str:pagina>', views.Select, name='Select')
]
