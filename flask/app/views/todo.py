from flask_restx import Namespace, Resource
from flask import request
from app.helpers.response import get_success_response, get_failure_response, parse_request_body, validate_required_fields
from app.helpers.decorators import login_required
from common.app_config import config
from common.services import TodoService
from common.models import Todo
from common.app_logger import logger

# Create the todo blueprint
todo_api = Namespace('todos', description="Todo-related APIs")


@todo_api.route('/')
class TodoList(Resource):
    
    @login_required()
    def get(self, person):
        """Get all todos for the current user"""
        todo_service = TodoService(config)
        todos = todo_service.get_todos_by_person_id(person.entity_id)
        
        # Convert todos to dictionaries
        todos_data = [todo.as_dict() for todo in todos]
        
        return get_success_response(todos=todos_data)
    
    @todo_api.expect(
        {'type': 'object', 'properties': {
            'title': {'type': 'string'}
        }}
    )
    @login_required()
    def post(self, person):
        """Create a new todo"""
        parsed_body = parse_request_body(request, ['title'])
        validate_required_fields(parsed_body)
        
        todo_service = TodoService(config)

        logger.info(f"------person: {person}")
        
        # Create new todo
        todo = Todo(
            person_id=person.entity_id,
            title=parsed_body['title'].strip(),
            completed=False
        )
        
        # Save todo
        saved_todo = todo_service.save_todo(todo)
        
        return get_success_response(
            message="Todo created successfully.",
            todo=saved_todo.as_dict()
        )


@todo_api.route('/<string:todo_id>')
class TodoItem(Resource):
    
    @todo_api.expect(
        {'type': 'object', 'properties': {
            'title': {'type': 'string'},
            'completed': {'type': 'boolean'}
        }}
    )
    @login_required()
    def put(self, todo_id, person):
        """Update a todo"""
        todo_service = TodoService(config)
        todo = todo_service.get_todo_by_id(todo_id)
        
        if not todo or todo.person_id != person.entity_id:
            return get_failure_response(message="Todo not found", status_code=404)
        
        parsed_body = parse_request_body(request, ['title', 'completed'])
        
        # Update fields if provided
        if 'title' in parsed_body:
            todo.title = parsed_body['title'].strip()
        if 'completed' in parsed_body:
            todo.completed = parsed_body['completed']
        
        # Save updated todo
        updated_todo = todo_service.save_todo(todo)
        
        return get_success_response(
            message="Todo updated successfully.",
            todo=updated_todo.as_dict()
        )
    
    @login_required()
    def delete(self, todo_id, person):
        """Delete a todo"""
        todo_service = TodoService(config)
        todo = todo_service.get_todo_by_id(todo_id)
        
        if not todo or todo.person_id != person.entity_id:
            return get_failure_response(message="Todo not found", status_code=404)
        
        todo_service.delete_todo(todo)
        
        return get_success_response(message="Todo deleted successfully.")


@todo_api.route('/toggle/<string:todo_id>')
class TodoToggle(Resource):
    
    @login_required()
    def patch(self, todo_id, person):
        """Toggle completion status of a todo"""
        todo_service = TodoService(config)
        todo = todo_service.get_todo_by_id(todo_id)
        
        if not todo or todo.person_id != person.entity_id:
            return get_failure_response(message="Todo not found", status_code=404)
        
        # Toggle completion
        todo.completed = not todo.completed
        updated_todo = todo_service.save_todo(todo)
        
        return get_success_response(
            message="Todo updated successfully.",
            todo=updated_todo.as_dict()
        )


@todo_api.route('/bulk-actions')
class TodoBulkActions(Resource):
    
    @todo_api.expect(
        {'type': 'object', 'properties': {
            'action': {'type': 'string', 'enum': ['toggle-all', 'clear-completed']},
            'completed': {'type': 'boolean'}
        }}
    )
    @login_required()
    def post(self, person):
        """Perform bulk actions on todos"""
        parsed_body = parse_request_body(request, ['action'])
        validate_required_fields(parsed_body)
        
        todo_service = TodoService(config)
        action = parsed_body['action']
        
        if action == 'toggle-all':
            completed = parsed_body.get('completed', True)
            updated_todos = todo_service.mark_all_todos_completed(person.entity_id, completed)
            return get_success_response(
                message=f"All todos marked as {'completed' if completed else 'active'}.",
                todos=[todo.as_dict() for todo in updated_todos]
            )
        
        elif action == 'clear-completed':
            deleted_count = todo_service.delete_completed_todos(person.entity_id)
            return get_success_response(
                message=f"Deleted {deleted_count} completed todos.",
                deleted_count=deleted_count
            )
        
        else:
            return get_failure_response(message="Invalid action", status_code=400)