"""cmsc495tm7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from povreg import views as povreg_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('povreg/', include('povreg.urls')),
    path('', RedirectView.as_view(url='povreg/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', povreg_views.signup, name="signup"),
    path('password/', povreg_views.change_password, name="change-password")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
admin.site.site_header = "CMSC 495 Team 7 Admin"
admin.site.index_title = "Welcom to CMSC 495 Team 7 Admin Site "
