from django.conf.urls import url, include
from .views import viewreport, receive, results, submit, dispatch, details

urlpatterns = [
    url(r'^viewreport/(?P<sample_id>\d+)/$', viewreport, name="viewreport"),
    url(r'^dispatch/', dispatch, name="dispatch"),
    url(r'^receive/', receive, name="receive"),
    url(r'^results/', results, name="results"),
    url(r'^submit/(?P<sample_id>\d+)/$', submit, name="submit"),
    url(r'^details/', details, name="details"),
]
