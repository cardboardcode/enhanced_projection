"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^posts/', include("openedprojects.urls", namespace = 'posts')),
    url(r'^hiddenposts/', include("hiddenforum.urls",namespace = 'hiddenposts')),
    url(r'^comments/', include("comments.urls", namespace = 'comments')),
    url(r'^$','newsletter.views.home', name='home'),
    url(r'^contact/$','newsletter.views.contact', name='contact'),
    url(r'^about/$','trydjango.views.about', name='about'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^messages/', include('projection_messages.urls')),
    
    url(r'^categories/', 'openedprojects.views.categories', name = 'categories'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/', "openedprojects.views.show_category", name = 'posts'),

    url(r'^openedprojects/','openedprojects.views.openedgenres', name='openedgenres'),
    url(r'^opened_subcategories/','openedprojects.views.opened_subcategories', name='opened_subcategories'),
    
    url(r'^closedprojects/','closedprojects.views.closedgenres', name='closedgenres'),
    url(r'^closed_subcategories/','closedprojects.views.closed_subcategories', name='closed_subcategories'),

    url(r'^involvedprojects/','involvedprojects.views.display_involved', name='involvedprojects'),
]   




#Inefficient Method (Get rid of these two lines during production where DEBUG = False)
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
