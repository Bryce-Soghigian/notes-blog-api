from django.urls import path

from . import views

urlpatterns = [
    path('v1/notes/sorted', views.SortedEntries.as_view(), name='sorted_entries'),
    path('v1/notes/entry', views.EntryView.as_view(), name='entry_crud'),
 ]