"""xReusable CRUD Module for PostgreSQL"""
import os
import logging
from typing import Any, Dict, List, Optional, Union
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Database configuration dataclass"""
    host: str
    port: int
    database: str
    username: str
    password: str
    min_connections: int = 1
    max_connections: int = 20

class CRUDManager:
   
    def __init__(self, config: DatabaseConfig):
       
        self.config = config
        self.pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize the connection pool"""
        try:
            self.pool = ThreadedConnectionPool(
                minconn=self.config.min_connections,
                maxconn=self.config.max_connections,
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password,
                cursor_factory=RealDictCursor
            )
            logger.info("Database connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize connection pool: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = self.pool.getconn()
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database operation failed: {e}")
            raise
        finally:
            if conn:
                self.pool.putconn(conn)
    
    def execute_query(self, query: str, params: Optional[tuple] = None, fetch: bool = True) -> Optional[List[Dict]]:

        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                
                if fetch:
                    return [dict(row) for row in cursor.fetchall()]
                else:
                    conn.commit()
                    return None
    
    def create_item(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:

        if not data:
            raise ValueError("Data cannot be empty")
        
        columns = list(data.keys())
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join(columns)
        
        query = f"""
            INSERT INTO {table} ({columns_str})
            VALUES ({placeholders})
            RETURNING *
        """
        
        result = self.execute_query(query, tuple(data.values()))
        return result[0] if result else None
    
    def get_item(self, table: str, item_id: Any, id_column: str = 'id') -> Optional[Dict[str, Any]]:
       
        query = f"SELECT * FROM {table} WHERE {id_column} = %s"
        result = self.execute_query(query, (item_id,))
        return result[0] if result else None
    
    def get_items(self, table: str, conditions: Optional[Dict[str, Any]] = None, 
                  limit: Optional[int] = None, offset: Optional[int] = None,
                  order_by: Optional[str] = None) -> List[Dict[str, Any]]:
       
        query = f"SELECT * FROM {table}"
        params = []
        
        if conditions:
            where_clauses = []
            for key, value in conditions.items():
                where_clauses.append(f"{key} = %s")
                params.append(value)
            query += f" WHERE {' AND '.join(where_clauses)}"
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit:
            query += f" LIMIT {limit}"
        
        if offset:
            query += f" OFFSET {offset}"
        
        return self.execute_query(query, tuple(params) if params else None)
    
    def update_item(self, table: str, item_id: Any, data: Dict[str, Any], 
                    id_column: str = 'id') -> Optional[Dict[str, Any]]:
       
        if not data:
            raise ValueError("Update data cannot be empty")
        
        set_clauses = []
        params = []
        
        for key, value in data.items():
            set_clauses.append(f"{key} = %s")
            params.append(value)
        
        params.append(item_id)
        
        query = f"""
            UPDATE {table}
            SET {', '.join(set_clauses)}
            WHERE {id_column} = %s
            RETURNING *
        """
        
        result = self.execute_query(query, tuple(params))
        return result[0] if result else None
    
    def delete_item(self, table: str, item_id: Any, id_column: str = 'id') -> bool:
        
        query = f"DELETE FROM {table} WHERE {id_column} = %s"
        
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (item_id,))
                conn.commit()
                return cursor.rowcount > 0
    
    def create_table(self, table_name: str, schema: Dict[str, str]):
        
        columns = []
        for column_name, column_type in schema.items():
            columns.append(f"{column_name} {column_type}")
        
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.execute_query(query, fetch=False)
        logger.info(f"Table '{table_name}' created successfully")
    
    def close(self):
        """Close all connections in the pool"""
        if self.pool:
            self.pool.closeall()
            logger.info("Database connection pool closed")

# Utility functions for easy initialization
def create_crud_manager_from_env() -> CRUDManager:
    
    config = DatabaseConfig(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 5432)),
        database=os.getenv('DB_NAME', 'testdb'),
        username=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password'),
        min_connections=int(os.getenv('DB_MIN_CONNECTIONS', 1)),
        max_connections=int(os.getenv('DB_MAX_CONNECTIONS', 20))
    )
    
    return CRUDManager(config)

# Example usage (for testing purposes)
if __name__ == "__main__":
    # Example of how to use the CRUD manager
    crud = create_crud_manager_from_env()
    
    # Create a sample table
    user_schema = {
        'id': 'SERIAL PRIMARY KEY',
        'name': 'VARCHAR(100) NOT NULL',
        'email': 'VARCHAR(100) UNIQUE NOT NULL',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    }
    
    try:
        crud.create_table('users', user_schema)
        
        # Create a user
        new_user = crud.create_item('users', {
            'name': 'John Doe',
            'email': 'john@example.com'
        })
        print(f"Created user: {new_user}")
        
        # Get the user
        user = crud.get_item('users', new_user['id'])
        print(f"Retrieved user: {user}")
        
        # Update the user
        updated_user = crud.update_item('users', new_user['id'], {
            'name': 'John Smith'
        })
        print(f"Updated user: {updated_user}")
        
        # Get all users
        all_users = crud.get_items('users')
        print(f"All users: {all_users}")
        
        # Delete the user
        deleted = crud.delete_item('users', new_user['id'])
        print(f"User deleted: {deleted}")
        
    except Exception as e:
        logger.error(f"Error in example: {e}")
    finally:
        crud.close()