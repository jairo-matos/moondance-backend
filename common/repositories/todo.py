from rococo.repositories.postgresql import PostgreSQLRepository
from common.models.todo import Todo


class TodoRepository(PostgreSQLRepository):
    
    def __init__(self, adapter, message_adapter, queue_name, user_id):
        super().__init__(adapter, Todo, message_adapter, queue_name, user_id)