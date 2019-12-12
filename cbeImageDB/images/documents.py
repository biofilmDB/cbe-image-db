# code from github example
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.documents import model_field_class_to_field_class
from django_elasticsearch_dsl.exceptions import ModelFieldNotMappedError
from elasticsearch_dsl import analyzer, token_filter, DocType, Text
from django.conf import settings
from django_elasticsearch_dsl.registries import registry
from .models import Image, Experiment

#index = Index(settings.ES_INDEX)
#index.settings(**settings.ES_INDEX_SETTINGS)


synonym_tokenfilter = token_filter(
    'synonym_tokenfilter',
    'synonym',
    synonyms=[
        'reactjs, react',  # <-- important
    ],
)

text_analyzer = analyzer(
    'text_analyzer',
    tokenizer='standard',
    filter=[
        # The ORDER is important here.
        'standard',
        'lowercase',
        'stop',
        synonym_tokenfilter,
        # Note! 'snowball' comes after 'synonym_tokenfilter'
        'snowball',
    ],
    char_filter=['html_strip']
)


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
        char_filter=["html_strip"]
)


@registry.register_document
class ExperimentDocument(Document):
    ugh = Text(
        required=True, 
        analyzer=text_analyzer
    )
    
    class Index:
        # Name of the Elasticsearch index
        name = 'experiment_names'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Experiment  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name',
        ]


   

@registry.register_document
class ImageDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'images'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Image  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'brief_description',
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True
        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False
        # Paginate the django queryset used to populate the index with the specified size
        # (by default there is no pagination)
        # queryset_pagination = 5000



from elasticsearch_dsl import (
    DocType,
    Text,
    Index,
    analyzer,
    Keyword,
    token_filter,
)
from django.conf import settings


#index = Index(settings.ES_INDEX)
#index.settings(**settings.ES_INDEX_SETTINGS)


synonym_tokenfilter = token_filter(
    'synonym_tokenfilter',
    'synonym',
    synonyms=[
        'reactjs, react',  # <-- important
    ],
)

text_analyzer = analyzer(
    'text_analyzer',
    tokenizer='standard',
    filter=[
        # The ORDER is important here.
        'standard',
        'lowercase',
        'stop',
        synonym_tokenfilter,
        # Note! 'snowball' comes after 'synonym_tokenfilter'
        'snowball',
    ],
    char_filter=['html_strip']
)

class BlogItemDoc(DocType):
    title = Text(
        required=True, 
        analyzer=text_analyzer
    )
    text = Text(analyzer=text_analyzer)

#index.doc_type(BlogItemDoc)