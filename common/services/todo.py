from common.repositories.factory import RepositoryFactory, RepoType
from common.models.todo import Todo


class TodoService:

    def __init__(self, config):
        self.config = config
        self.repository_factory = RepositoryFactory(config)
        self.todo_repo = self.repository_factory.get_repository(RepoType.TODO)

    def save_todo(self, todo: Todo):
        """Save or update a todo item"""
        todo = self.todo_repo.save(todo)
        return todo

    def get_todos_by_person_id(self, person_id: str):
        """Get all todos for a specific person"""
        todos = self.todo_repo.get_many({"person_id": person_id})
        return todos

    def get_todo_by_id(self, todo_id: str):
        """Get a specific todo by ID"""
        todo = self.todo_repo.get_one({"entity_id": todo_id})
        return todo

    def delete_todo(self, todo: Todo):
        """Delete a todo item"""
        self.todo_repo.delete(todo)

    def delete_todo_by_id(self, todo_id: str):
        """Delete a todo by ID"""
        todo = self.get_todo_by_id(todo_id)
        if todo:
            self.delete_todo(todo)
            return True
        return False

    def get_completed_todos_by_person_id(self, person_id: str):
        """Get all completed todos for a specific person"""
        todos = self.todo_repo.get_many({"person_id": person_id, "completed": True})
        return todos

    def get_active_todos_by_person_id(self, person_id: str):
        """Get all active (not completed) todos for a specific person"""
        todos = self.todo_repo.get_many({"person_id": person_id, "completed": False})
        return todos

    def toggle_todo_completion(self, todo_id: str):
        """Toggle the completion status of a todo"""
        todo = self.get_todo_by_id(todo_id)
        if todo:
            todo.completed = not todo.completed
            return self.save_todo(todo)
        return None

    def mark_all_todos_completed(self, person_id: str, completed: bool = True):
        """Mark all todos as completed or not completed for a person"""
        todos = self.get_todos_by_person_id(person_id)
        updated_todos = []
        for todo in todos:
            todo.completed = completed
            updated_todo = self.save_todo(todo)
            updated_todos.append(updated_todo)
        return updated_todos

    def delete_completed_todos(self, person_id: str):
        """Delete all completed todos for a person"""
        completed_todos = self.get_completed_todos_by_person_id(person_id)
        for todo in completed_todos:
            self.delete_todo(todo)
        return len(completed_todos)