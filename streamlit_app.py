import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime
import os
from typing import Optional, List, Dict, Any

# Database connection configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'postgres'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'crud_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'db_123')
}

class DatabaseManager:
    def __init__(self):
        self.config = DB_CONFIG
        
    def get_connection(self):
        """Create and return database connection"""
        try:
            conn = psycopg2.connect(**self.config)
            return conn
        except Exception as e:
            st.error(f"Error connecting to database: {str(e)}")
            return None
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict[Any, Any]]]:
        """Execute query and return results"""
        conn = self.get_connection()
        if not conn:
            return None
            
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if query.strip().upper().startswith('SELECT'):
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                else:
                    conn.commit()
                    return []
        except Exception as e:
            st.error(f"Database error: {str(e)}")
            conn.rollback()
            return None
        finally:
            conn.close()

# Initialize database manager
db = DatabaseManager()

def main():
    st.set_page_config(page_title="CRUD Application", page_icon="🗃️", layout="wide")
    
    st.title("🗃️ PostgreSQL CRUD Application")
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose Operation", ["View Data", "Add Records", "Update Records", "Delete Records", "Database Info"])
    
    if page == "View Data":
        view_data_page()
    elif page == "Add Records":
        add_records_page()
    elif page == "Update Records":
        update_records_page()
    elif page == "Delete Records":
        delete_records_page()
    elif page == "Database Info":
        database_info_page()

def view_data_page():
    st.header("📊 View Data")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        table_choice = st.selectbox("Select Table", ["users", "products"])
        
        if st.button("Refresh Data", type="primary"):
            st.rerun()
    
    with col2:
        if table_choice == "users":
            display_users_table()
        else:
            display_products_table()

def display_users_table():
    st.subheader("👥 Users Table")
    
    query = "SELECT * FROM users ORDER BY id"
    results = db.execute_query(query)
    
    if results:
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)
        st.info(f"Total users: {len(results)}")
    else:
        st.warning("No users found or error retrieving data.")

def display_products_table():
    st.subheader("📦 Products Table")
    
    query = "SELECT * FROM products ORDER BY id"
    results = db.execute_query(query)
    
    if results:
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)
        st.info(f"Total products: {len(results)}")
    else:
        st.warning("No products found or error retrieving data.")

def add_records_page():
    st.header("➕ Add New Records")
    
    tab1, tab2 = st.tabs(["Add User", "Add Product"])
    
    with tab1:
        add_user_form()
    
    with tab2:
        add_product_form()

def add_user_form():
    st.subheader("Add New User")
    
    with st.form("add_user_form"):
        name = st.text_input("Name*", placeholder="Enter user name")
        email = st.text_input("Email*", placeholder="Enter email address")
        
        submitted = st.form_submit_button("Add User", type="primary")
        
        if submitted:
            if name and email:
                query = "INSERT INTO users (name, email) VALUES (%s, %s)"
                result = db.execute_query(query, (name, email))
                
                if result is not None:
                    st.success("✅ User added successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to add user. Email might already exist.")
            else:
                st.error("Please fill in all required fields.")

def add_product_form():
    st.subheader("Add New Product")
    
    with st.form("add_product_form"):
        name = st.text_input("Product Name*", placeholder="Enter product name")
        description = st.text_area("Description", placeholder="Enter product description")
        price = st.number_input("Price", min_value=0.0, step=0.01, format="%.2f")
        stock = st.number_input("Stock Quantity", min_value=0, step=1)
        
        submitted = st.form_submit_button("Add Product", type="primary")
        
        if submitted:
            if name:
                query = "INSERT INTO products (name, description, price, stock_quantity) VALUES (%s, %s, %s, %s)"
                result = db.execute_query(query, (name, description, price, stock))
                
                if result is not None:
                    st.success("✅ Product added successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to add product.")
            else:
                st.error("Please enter a product name.")

def update_records_page():
    st.header("✏️ Update Records")
    
    tab1, tab2 = st.tabs(["Update User", "Update Product"])
    
    with tab1:
        update_user_form()
    
    with tab2:
        update_product_form()

def update_user_form():
    st.subheader("Update User")
    
    # Get all users for selection
    users_query = "SELECT id, name, email FROM users ORDER BY name"
    users = db.execute_query(users_query)
    
    if users:
        user_options = {f"{user['name']} ({user['email']})": user['id'] for user in users}
        selected_user = st.selectbox("Select User to Update", options=list(user_options.keys()))
        
        if selected_user:
            user_id = user_options[selected_user]
            
            # Get current user data
            current_user_query = "SELECT * FROM users WHERE id = %s"
            current_user = db.execute_query(current_user_query, (user_id,))
            
            if current_user:
                user_data = current_user[0]
                
                with st.form("update_user_form"):
                    name = st.text_input("Name", value=user_data['name'])
                    email = st.text_input("Email", value=user_data['email'])
                    
                    submitted = st.form_submit_button("Update User", type="primary")
                    
                    if submitted:
                        if name and email:
                            update_query = "UPDATE users SET name = %s, email = %s WHERE id = %s"
                            result = db.execute_query(update_query, (name, email, user_id))
                            
                            if result is not None:
                                st.success("✅ User updated successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to update user.")
                        else:
                            st.error("Please fill in all fields.")
    else:
        st.warning("No users available to update.")

def update_product_form():
    st.subheader("Update Product")
    
    # Get all products for selection
    products_query = "SELECT id, name, price FROM products ORDER BY name"
    products = db.execute_query(products_query)
    
    if products:
        product_options = {f"{product['name']} (${product['price']})": product['id'] for product in products}
        selected_product = st.selectbox("Select Product to Update", options=list(product_options.keys()))
        
        if selected_product:
            product_id = product_options[selected_product]
            
            # Get current product data
            current_product_query = "SELECT * FROM products WHERE id = %s"
            current_product = db.execute_query(current_product_query, (product_id,))
            
            if current_product:
                product_data = current_product[0]
                
                with st.form("update_product_form"):
                    name = st.text_input("Product Name", value=product_data['name'])
                    description = st.text_area("Description", value=product_data['description'] or "")
                    price = st.number_input("Price", value=float(product_data['price'] or 0), min_value=0.0, step=0.01)
                    stock = st.number_input("Stock Quantity", value=product_data['stock_quantity'] or 0, min_value=0, step=1)
                    
                    submitted = st.form_submit_button("Update Product", type="primary")
                    
                    if submitted:
                        if name:
                            update_query = "UPDATE products SET name = %s, description = %s, price = %s, stock_quantity = %s WHERE id = %s"
                            result = db.execute_query(update_query, (name, description, price, stock, product_id))
                            
                            if result is not None:
                                st.success("✅ Product updated successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to update product.")
                        else:
                            st.error("Please enter a product name.")
    else:
        st.warning("No products available to update.")

def delete_records_page():
    st.header("🗑️ Delete Records")
    st.warning("⚠️ Deletion is permanent and cannot be undone!")
    
    tab1, tab2 = st.tabs(["Delete User", "Delete Product"])
    
    with tab1:
        delete_user_form()
    
    with tab2:
        delete_product_form()

def delete_user_form():
    st.subheader("Delete User")
    
    users_query = "SELECT id, name, email FROM users ORDER BY name"
    users = db.execute_query(users_query)
    
    if users:
        user_options = {f"{user['name']} ({user['email']})": user['id'] for user in users}
        selected_user = st.selectbox("Select User to Delete", options=list(user_options.keys()))
        
        if selected_user:
            user_id = user_options[selected_user]
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🗑️ Delete User", type="secondary"):
                    delete_query = "DELETE FROM users WHERE id = %s"
                    result = db.execute_query(delete_query, (user_id,))
                    
                    if result is not None:
                        st.success("✅ User deleted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete user.")
    else:
        st.info("No users available to delete.")

def delete_product_form():
    st.subheader("Delete Product")
    
    products_query = "SELECT id, name, price FROM products ORDER BY name"
    products = db.execute_query(products_query)
    
    if products:
        product_options = {f"{product['name']} (${product['price']})": product['id'] for product in products}
        selected_product = st.selectbox("Select Product to Delete", options=list(product_options.keys()))
        
        if selected_product:
            product_id = product_options[selected_product]
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🗑️ Delete Product", type="secondary"):
                    delete_query = "DELETE FROM products WHERE id = %s"
                    result = db.execute_query(delete_query, (product_id,))
                    
                    if result is not None:
                        st.success("✅ Product deleted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete product.")
    else:
        st.info("No products available to delete.")

def database_info_page():
    st.header("💾 Database Information")
    
    # Connection status
    st.subheader("Connection Status")
    conn = db.get_connection()
    if conn:
        st.success("✅ Connected to PostgreSQL database")
        conn.close()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Host:** {DB_CONFIG['host']}")
            st.info(f"**Port:** {DB_CONFIG['port']}")
            st.info(f"**Database:** {DB_CONFIG['database']}")
        
        with col2:
            st.info(f"**User:** {DB_CONFIG['user']}")
            st.info(f"**Connected at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Table statistics
        st.subheader("📊 Table Statistics")
        
        # Users statistics
        users_count_query = "SELECT COUNT(*) as count FROM users"
        users_count = db.execute_query(users_count_query)
        
        # Products statistics  
        products_count_query = "SELECT COUNT(*) as count FROM products"
        products_count = db.execute_query(products_count_query)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if users_count:
                st.metric("👥 Total Users", users_count[0]['count'])
            
        with col2:
            if products_count:
                st.metric("📦 Total Products", products_count[0]['count'])
                
        # Recent activity
        st.subheader("🕐 Recent Activity")
        recent_users = db.execute_query("SELECT name, email, created_at FROM users ORDER BY created_at DESC LIMIT 5")
        recent_products = db.execute_query("SELECT name, price, created_at FROM products ORDER BY created_at DESC LIMIT 5")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Recent Users:**")
            if recent_users:
                for user in recent_users:
                    st.write(f"• {user['name']} - {user['created_at'].strftime('%Y-%m-%d %H:%M')}")
            else:
                st.write("No recent users")
        
        with col2:
            st.write("**Recent Products:**")
            if recent_products:
                for product in recent_products:
                    st.write(f"• {product['name']} - ${product['price']} - {product['created_at'].strftime('%Y-%m-%d %H:%M')}")
            else:
                st.write("No recent products")
                
    else:
        st.error("❌ Failed to connect to database")

if __name__ == "__main__":
    main()