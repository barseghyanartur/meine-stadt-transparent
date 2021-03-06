from django.db.models import Prefetch
from django_elasticsearch_dsl import DocType, TextField, IntegerField, DateField

from mainapp.documents.index import elastic_index_person
from mainapp.models import Person, Membership
from .index import autocomplete_analyzer


@elastic_index_person.doc_type
class PersonDocument(DocType):
    autocomplete = TextField(attr="name_autocomplete", analyzer=autocomplete_analyzer)
    sort_date = DateField()
    organization_ids = IntegerField(attr="organization_ids")

    def get_queryset(self):
        sort_date_queryset = Membership.objects.filter(start__isnull=False).order_by(
            "-start"
        )

        return (
            Person.objects.order_by("id")
            .prefetch_related("membership_set")
            .prefetch_related(
                Prefetch(
                    "membership_set",
                    queryset=sort_date_queryset,
                    to_attr="sort_date_prefetch",
                )
            )
        )

    class Meta:
        model = Person
        queryset_pagination = 500

        fields = ["id", "name", "given_name", "family_name"]
