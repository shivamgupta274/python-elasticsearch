from django.contrib.auth.models import User, Group
from rest_framework import serializers

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from calculations.documents import CalculationDocument

class CalculationDocumentSerializer(DocumentSerializer):
    class Meta:
        document = CalculationDocument
        fields = ('id', 'title', 'body', 'author', 'created', 'modified', 'pub_date',)

class UserSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = Group
        fields = ['url', 'name']