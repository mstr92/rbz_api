from flask_restplus import fields
from helpers.restplus import api

movie = api.model('Movies', {
    'neg_entity': fields.List(fields.String(description='List of negative entities')),
    'pos_entity': fields.List(fields.String(description='List of positive entities')),
    'neg_movie': fields.List(fields.String(description='List of negative movies')),
    'pos_movie': fields.List(fields.String(description='List of positive movies')),
    'neg_actor': fields.List(fields.String(description='List of negative actors')),
    'pos_actor': fields.List(fields.String(description='List of positive actors')),
    'neg_genre': fields.List(fields.String(description='List of negative genres')),
    'pos_genre': fields.List(fields.String(description='List of positive genres')),
    'neg_keyword': fields.List(fields.String(description='List of negative keywords')),
    'pos_keyword': fields.List(fields.String(description='List of positive keywords')),
    'neg_year_from': fields.List(fields.Integer(pattern='^[0-9]{4}', description='List of negative years from')),
    'pos_year_from': fields.List(fields.Integer(description='List of positive years from')),
    'neg_year_to': fields.List(fields.Integer(description='List of negative years to')),
    'pos_year_to': fields.List(fields.Integer(description='List of positive years to')),
    'length': fields.Integer(description='Total number of results'),
    # 'approach': fields.Integer(description='Total number of results'),
})



