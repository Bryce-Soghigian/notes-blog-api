from django.urls import path

from . import views

urlpatterns = [
    path('v1/notes/sorted', views.SortedEntries.as_view(), name='sorted_entries'),
    path('v1/notes/retrieve/<note_id>', views.RetrieveEntry.as_view(), name='retrieve_entry'),
    path('v1/notes/titles/try', views.TitleView.as_view(), name='titles'),
    path('v1/notes/entry', views.EntryView.as_view(), name='entry_crud'),
 ]