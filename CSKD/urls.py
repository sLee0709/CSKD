"""CSKD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from .views import CSKD_index, simple_search, tutorial, contact, about_us,adv_search,downloads,submit_data,network_construction,testpage, functional_enrichment, browse, gene_detailed,case_detail, adv_search_clinical_res
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, handler400, handler404
from django.conf.urls.static import static
from django.conf import settings

handler404 = "CSKD.views.page_not_found"
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', CSKD_index, name='CSKD_index'),
    url(r'^quick_search/$', simple_search,name='simple_search'),
    url(r'^tutorial/$',tutorial, name='tutorial'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^about/$', about_us, name='about_us'),
    url(r'^search/$', adv_search, name='adv_search'),
    url(r'^download/$', downloads, name='downloads'),
    url(r'^submit/$', submit_data, name='submit_data'),
    url(r'^network_construction/$', network_construction, name='network_constuction'),
    url(r'^enrichment/$', functional_enrichment, name='functional_enrichment'),
    url(r'^browse/$', browse, name='browse'),
    url(r'^test/$', testpage, name='testpage'),
    path('cytokines/<str:slug>', gene_detailed, name='gene_detailed'),
    path('cases/<str:slug>', case_detail, name='case_detail'),
    url(r'^case_search_results/$', adv_search_clinical_res, name='case_search_results'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
