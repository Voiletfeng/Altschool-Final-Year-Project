from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
from flask_jwt_extended import jwt_required
import requests
from flask import request
from ..model.linkmodel import LinkSpace
import json
from ..utils import db

link_namespace = Namespace('link', description="link creation namespace")
link_model = link_namespace.model('LinkShorten', {
    'id': fields.Integer(decription='link identifier', required=True),
    'link': fields.String(description="url to shorten", required=True),
    'name': fields.String(description="name alias", required=True)
})
link_march = link_namespace.model('LinkMac', {
    'id': fields.Integer(decription='link identifier', required=True),
    'link': fields.String(description="url to shorten", required=True)
})


@link_namespace.route('/create_link')
class createShortenLink(Resource):
    @link_namespace.expect(link_model)
    @jwt_required()
    def post(self):
        '''
            Create shorten link
        '''
        data = request.get_json()
        key = 'ed6b9642e21672c4626234620c1b3c72'
        url = data['url']
        name = data['name']
        
        api_url = 'http://cutt.ly/api/api.php?key={}&short={}&name={}&userDomain={}'
        
        response = requests.get(api_url.format(key, url, name, '0'))
        response_json = json.loads(response.content.decode('utf-8'))
        short_link = response_json['url']['shortLink']
        s_link = short_link
        set_link = LinkSpace(link=s_link)
        set_link.save()
        
        return response.json(), HTTPStatus.CREATED
        
@link_namespace.route('all_links')
class getAallLinks(Resource):
    @link_namespace.marshal_with(link_march)
    @jwt_required()
    def get(self):
        '''
            Get All Links
        '''
        links = LinkSpace.query.all()
        return links, HTTPStatus.OK