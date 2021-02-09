from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from calculations.serializers import UserSerializer, GroupSerializer, CalculationDocumentSerializer


from  django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend, 
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from calculations.documents import CalculationDocument
# from calculations import serializers as calculations_serilaizers

# Create your views here.
def TestCalculation(request):
    return render(request,'home.html', {})

# class SaifiCalculation(ListView):
#     template_name = 'home.html'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_class = [ permissions.IsAuthenticated ]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_class = [ permissions.IsAuthenticated ]


class ActiveViewSet(DocumentViewSet):
    document = CalculationDocument
    serializer_class = CalculationDocumentSerializer

    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend
    ]
    # Define search fields
    search_fields= (
        'title',
        'body'
    )
    # Filter fields
    filter_fields = {
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'title': 'title.raw',
        'body': 'body.raw',
        'author': {
            'field': 'author_id',
            'lookups': [
                LOOKUP_QUERY_IN,
            ]
        },
        'created': 'created',
        'modified': 'modified',
        'pub_date': 'pub_date',
    }

    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        'title': 'title.raw',
        'author': 'author_id',
        'created': 'created',
        'modified': 'modified',
        'pub_date': 'pub_date',
    }

    # Specify default ordering
    ordering = ('id', 'created',)