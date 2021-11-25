import json

from django import views, http
from notes.models import Entry


class SortedEntries(views.View):
    """
    Return all objects in sorted object based on category.
    """
    def get(self):
        """
        Retreive all of the notes in the database.

        Return them in a sorted ordering groupedby their category.
        """
        sorted_entries = {}
        entry_cat = Entry.objects.raw('SELECT category FROM notes_entry')
        print(entry_cat)
        if not len(entry_cat):
            return http.JsonResponse(
                'Please insert some categories into the database.'
            )

        for obj in entry_cat:
            sorted_entries[obj] = Entry.objects.filter(category=obj)

        return http.JsonResponse(
            sorted_entries,
            safe=False
        )


class EntryView(views.View):
    """
    CRUD Endpoints for Entry.
    """

    def get(self):

        return http.JsonResponse(
            Entry.objects.all(),
            safe=False,
        )

    def post(self, request: http.request):
        """
        Post a new Markdown Note to the database.
        """
        # TODO replace try except here with django validator class.
        try:
            request_body = json.loads(request.body)
        except json.JSONDecodeError:
            return http.HttpResponseBadRequest('Invalid JSON Body')

        for key in ["category, entry_content", "entry_title"]:
            if key not in request_body:
                return http.HttpResponseBadRequest(f'Missing required Field:{key}')
            # this covers the case of an empty dict or a empty string.
            if len(request_body[key]) == 0:
                return http.HttpResponseBadRequest(f'Required field: {key} is empty')

        try:
            new_entry = Entry(**request_body)
            new_entry.save()
            return http.JsonResponse(
                {
                    "data": new_entry,
                    "message": f'Successfully inserted {new_entry.entry_title} into the database :)'
                }
            )
        except ValueError:
            return http.HttpResponseBadRequest('Issue inserting request body as an entry to the database.')



class CategoryView(views.View):
    """
    Management Class of the Entries Objects.
    """
    def get(self, request, category):
        """
        get by the category.
        """
        if category == "":
            return http.HttpResponseBadRequest('Category Field cannot be empty.')
        try:
            entries = Entry.objects.get(category=category)
        except Entry.DoesNotExist:
            return http.HttpResponseBadRequest(f'Category of type:{category} does not exist in db.')

        return http.JsonResponse(
            entries,
            safe=True,
        )

