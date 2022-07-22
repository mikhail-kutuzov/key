from django.urls import path
from . import views
urlpatterns = [
    path("home", views.home, name="home"),
    path("",views.outlet,name="outlet"),
    path("logger",views.logger,name="logger"),
    path("signer",views.signer,name="signer"),
    path("otp",views.otp,name="otp"),
    path("updater",views.update,name="updater"),
    path("adder",views.adder,name="adder"),
    path("deleter",views.delete,name="deleter"),
    path("logout",views.logout,name="logout"),
    path("mailer",views.mailer,name="mailer"),
]