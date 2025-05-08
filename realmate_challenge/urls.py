from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponseRedirect
from realmate_challenge.view import login_view, lougout_view


def redirect_404(request, exception):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    return HttpResponseRedirect("/conversations/view/")


handler404 = redirect_404

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chat_hooks.urls")),
    path("login/", login_view, name="login"),
    path("logout/", lougout_view, name="logout"),
]
