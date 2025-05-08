from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponseRedirect
from django.conf.urls.static import static


def redirect_404(request, exception):
    return HttpResponseRedirect("/conversations/view/")


handler404 = redirect_404

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chat_hooks.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
