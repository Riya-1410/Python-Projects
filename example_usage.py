#!/usr/bin/env python3
"""
Example usage of the CRUD module
================================

This script demonstrates how to use the reusable CRUD module
in different scenarios and applications.
"""

import os
from dotenv import load_dotenv
from CRUD.app.crud import CRUDManager, DatabaseConfig, create_crud_manager_from_env

# Load environment variables
load_dotenv()

def example_basic_usage():
    """Basic CRUD operations example"""
    print("=== Basic CRUD Operations Example ===")
    
    # Initialize CRUD manager from environment
    crud = create_crud_manager_from_env()
    
    try:
        # Create a new user
        print("\n1. Creating a new user...")
        new_user = crud.create_item('users', {
            'name': 'Jane Doe',
            'email': 'jane@example.com'
        })
        print(f"Created user: {new_user}")
        
        # Read the user
        print("\n2. Reading the user...")
        user = crud.get_item('users', new_user['id'])
        print(f"Retrieved user: {user}")
        
        # Update the user
        print("\n3. Updating the user...")
        updated_user = crud.update_item('users', new_user['id'], {
            'name': 'Jane Smith'
        })
        print(f"Updated user: {updated_user}")
        
        # List all users
        print("\n4. Listing all users...")
        all_users = crud.get_items('users')
        print(f"All users ({len(all_users)}):")
        for user in all_users:
            print(f"  - {user['name']} ({user['email']})")
        
        # Delete the user
        print("\n5. Deleting the user...")
        deleted = crud.delete_item('users', new_user['id'])
        print(f"User deleted: {deleted}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        crud.close()

def example_advanced_queries():
    """Advanced querying example"""
    print("\n=== Advanced Querying Example ===")
    
    crud = create_crud_manager_from_env()
    
    try:
        # Get users with conditions
        print("\n1. Finding users with specific conditions...")
        conditions = {'name': 'Alice Johnson'}
        users = crud.get_items('users', conditions=conditions)
        print(f"Users named 'Alice Johnson': {users}")
        
        # Get users with pagination
        print("\n2. Getting users with pagination...")
        paginated_users = crud.get_items('users', limit=2, offset=0, order_by='name')
        print(f"First 2 users (ordered by name): {paginated_users}")
        
        # Raw SQL query example
        print("\n3. Using raw SQL query...")
        result = crud.execute_query(
            "SELECT name, email FROM users WHERE created_at > %s",
            ('2024-01-01',)
        )
        print(f"Recent users: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        crud.close()

def example_product_management():
    """Product management example"""
    print("\n=== Product Management Example ===")
    
    crud = create_crud_manager_from_env()
    
    try:
        # Create a new product
        print("\n1. Creating a new product...")
        new_product = crud.create_item('products', {
            'name': 'Wireless Headphones',
            'description': 'Noise-cancelling wireless headphones',
            'price': 199.99,
            'stock_quantity': 25
        })
        print(f"Created product: {new_product}")
        
        # Update stock quantity
        print("\n2. Updating stock quantity...")
        updated_product = crud.update_item('products', new_product['id'], {
            'stock_quantity': 20
        })
        print(f"Updated product: {updated_product}")
        
        # Get all products
        print("\n3. Listing all products...")
        products = crud.get_items('products', order_by='name')
        print("All products:")
        for product in products:
            print(f"  - {product['name']}: ${product['price']} (Stock: {product['stock_quantity']})")
        
        # Find products by price range (using raw SQL)
        print("\n4. Finding products in price range...")
        expensive_products = crud.execute_query(
            "SELECT * FROM products WHERE price > %s ORDER BY price DESC",
            (50.0,)
        )
        print("Products over $50:")
        for product in expensive_products:
            print(f"  - {product['name']}: ${product['price']}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        crud.close()

def example_with_custom_config():
    """Example using custom database configuration"""
    print("\n=== Custom Configuration Example ===")
    
    # Custom configuration (useful for multiple databases)
    config = DatabaseConfig(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 5432)),
        database=os.getenv('DB_NAME', 'testdb'),
        username=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password'),
        min_connections=2,
        max_connections=10
    )
    
    crud = CRUDManager(config)
    
    try:
        # Use the CRUD manager with custom configuration
        users = crud.get_items('users', limit=1)
        print(f"Sample user with custom config: {users[0] if users else 'No users found'}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        crud.close()

def example_table_creation():
    """Example of creating tables dynamically"""
    print("\n=== Dynamic Table Creation Example ===")
    
    crud = create_crud_manager_from_env()
    
    try:
        # Define a new table schema
        blog_posts_schema = {
            'id': 'SERIAL PRIMARY KEY',
            'title': 'VARCHAR(200) NOT NULL',
            'content': 'TEXT',
            'author_id': 'INTEGER REFERENCES users(id)',
            'published': 'BOOLEAN DEFAULT FALSE',
            'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        }
        
        # Create the table
        print("Creating blog_posts table...")
        crud.create_table('blog_posts', blog_posts_schema)
        
        # Insert a sample blog post
        print("Inserting sample blog post...")
        blog_post = crud.create_item('blog_posts', {
            'title': 'Welcome to My Blog',
            'content': 'This is my first blog post using the CRUD module!',
            'author_id': 1,
            'published': True
        })
        print(f"Created blog post: {blog_post}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        crud.close()

if __name__ == "__main__":
    print("CRUD Module Usage Examples")
    print("=" * 50)
    
    # Run all examples
    example_basic_usage()
    example_advanced_queries()
    example_product_management()
    example_with_custom_config()
    example_table_creation()
    
    print("\n" + "=" * 50)
    print("All examples completed!")