from flask_restx import Namespace, Resource
from flask import request
from app.helpers.response import get_success_response, parse_request_body, validate_required_fields
from app.helpers.decorators import login_required
from common.app_config import config
from common.services import PersonService

# Create the person blueprint
person_api = Namespace('person', description="Person-related APIs")


@person_api.route('/me')
class Me(Resource):
    
    @login_required()
    def get(self, person):
        return get_success_response(person=person.as_dict())
    
    @person_api.expect(
        {'type': 'object', 'properties': {
            'first_name': {'type': 'string'},
            'last_name': {'type': 'string'}
        }}
    )
    @login_required()
    def put(self, person):
        parsed_body = parse_request_body(request, ['first_name', 'last_name'])
        validate_required_fields(parsed_body)
        
        person_service = PersonService(config)
        
        # Update person fields
        person.first_name = parsed_body['first_name']
        person.last_name = parsed_body['last_name']
        
        # Save updated person
        updated_person = person_service.save_person(person)
        
        return get_success_response(
            message="Profile updated successfully.",
            person=updated_person.as_dict()
        )
