import json

from django import views, http
from notes.models import Entry


class SortedEntries(views.View):
    """
    Return all objects in sorted object based on category.
    """
    def get(self, request: http.HttpRequest):
        """
        Retreive all of the notes in the database.

        Return them in a sorted ordering groupedby their category.
        """
        sorted_entries = {}
        entry_cat = Entry.objects.all().distinct('category')
        print(entry_cat)
        if not len(entry_cat):
            return http.JsonResponse(
                'Please insert some categories into the database.'
            )
        #
        for obj in entry_cat:
            local_category = obj.category
            sorted_entries[local_category] = []
            objs_matching_cat = Entry.objects.filter(category=local_category)
            print(objs_matching_cat)
            for sub_obj in objs_matching_cat:
                new_obj = {
                    'id': sub_obj.id,
                    'entry_content': sub_obj.entry_content,
                    'entry_title': sub_obj.entry_title,
                    'entry_description': sub_obj.entry_description,
                    'date_created': str(sub_obj.date_created),
                }
                sorted_entries[obj.category].append(new_obj)

        return http.JsonResponse(
            sorted_entries,
            safe=False
        )


class RetrieveEntry(views.View):
    def get(self, request, note_id):
        """
        Retreive by id. I know this implementation is scuffed.
        """

        try:
            sub_obj = Entry.objects.get(id=note_id)
            new_obj = {
                'id': sub_obj.id,
                'entry_content': sub_obj.entry_content,
                'entry_title': sub_obj.entry_title,
                'category': sub_obj.category,
                'entry_description': sub_obj.entry_description,
                'date_created': str(sub_obj.date_created),
            }
            return http.JsonResponse(
                new_obj,
                safe=False,
            )
        except Entry.DoesNotExist:
            return http.HttpResponseBadRequest(f'Note of {note_id} does not exist')
class TitleView(views.View):
    """
    Title.
    """
    def get(self, request):
        """
        Select all the titles and ids in the entries table.
        """

        queryset = Entry.objects.values_list('id', 'entry_title')
        output = []
        for k,v in queryset:
            new_obj = {
                'id':k,
                'entry_title':v,
            }
            output.append(new_obj)

        return http.JsonResponse(
            output,
            safe=False
        )

class EntryView(views.View):
    """
    CRUD Endpoints for Entry.
    """

    def get(self, request):

        output = []
        entry_objs = list(Entry.objects.all())

        for obj in entry_objs:
            new_obj = {
                'id': obj.id,
                'category': obj.category,
                'entry_content': obj.entry_content,
                'entry_title': obj.entry_title,
                'entry_description': obj.entry_description,
                'date_created': str(obj.date_created),
            }
            output.append(new_obj)

        return http.JsonResponse(
            output,
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

