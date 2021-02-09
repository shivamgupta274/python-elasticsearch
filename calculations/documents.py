from elasticsearch_dsl import analyzer
from django_elasticsearch_dsl.registries import registry
# from elasticsearch_dsl import analyzer,Index
from django_elasticsearch_dsl import Document,Index, fields 
from calculations import models as calculations_models

calculations_index = Index('calculations')
calculations_index.settings(
    number_of_shards = 1,
    number_of_replicas = 0
)

html_strip = analyzer(
    'html_strip',
    tokenizer = "standard",
    filter = ["stanard", "lowercase", "stop", "snowball"],
    char_filter = ["html_strip"]
)

# @registry.register_document
@calculations_index.document
class CalculationDocument(Document):
    """Article elasticsearch document"""
    
    id = fields.IntegerField(attr='id')
    title = fields.TextField(
        analyzer=html_strip,
        fields={'raw': fields.KeywordField()}
    )
    body = fields.TextField(
        analyzer=html_strip,
        fields={'raw': fields.KeywordField()}
    )
    author = fields.IntegerField(attr='author_id')
    created = fields.DateField()
    modified = fields.DateField()
    pub_date = fields.DateField()

    class Django:
        model = calculations_models.Calculation

    