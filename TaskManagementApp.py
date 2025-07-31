import mysql.connector
from mysql.connector import Error
from datetime import datetime

#CREATE A TABLE AND DATABASE IF THEY DO NOT EXIST
#CREATE A TABLE WITH TASKID, TITLE, DESCRIPTION, DUEDATE, PRIORITYLEVEL
def create_database_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',  # Replace with your MySQL username
            password='admin'   # Replace with your MySQL password
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS TaskManagerDB")
            cursor.execute("USE TaskManagerDB")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
  TaskID int NOT NULL AUTO_INCREMENT,
  Title varchar(255) NOT NULL,
  Description varchar(500) DEFAULT NULL,
  DueDate date NOT NULL,
  PriorityLevel enum('Low','Medium','High') DEFAULT 'Low',
  Status enum('Pending','In Progress','Completed') DEFAULT 'Pending',
  CreationTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (TaskID),
  UNIQUE KEY TaskID_UNIQUE (TaskID)
)
            """)
            print("Database and table created successfully")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

class TaskManager:
    def __init__(self):
        self.connection = create_database_connection()

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host='127.0.0.1',
                user='root',      # Replace with your MySQL username
                password='admin',      # Replace with your MySQL password
                database='TaskManagerDB'
            )
            return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None


    #Create a task with title, description, duedate, prioritylevel, status
    def create_task(self, title, description=None, duedate='2001-01-01', prioritylevel='Low', status='Pending'):
        if not self.connection:
            print("Database connection failed")
            return False
        
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO tasks (title, description, duedate, prioritylevel, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (title, description, duedate, prioritylevel, status))
            self.connection.commit()
            print("Task created successfully")
            return True
        except Error as e:
            print(f"Error creating task: {e}")
            return False
    
    #List down the tasks
    def read_tasks(self):
        if not self.connection:
            print("Database connection failed")
            return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM tasks ORDER BY CreationTimestamp DESC"
            cursor.execute(query)
            tasks = cursor.fetchall()
            return tasks
                
        except Error as e:
            print(f"Error reading tasks: {e}")
            return None
    
    #Update a task by task_id, only update the fields that were provided, if no fields are provided, return False
    def update_task(self, task_id, title=None, description=None, due_date=None, status=None):
        if not self.connection:
            print("Database connection failed")
            return False
        
        try:
            cursor = self.connection.cursor()
            
            # First get the current task data
            current_task = self.read_tasks(task_id)
            if not current_task:
                print("Task not found")
                return False
            
            # Update only the fields that were provided
            update_fields = []
            update_values = []
            
            if title is not None:
                update_fields.append("title = %s")
                update_values.append(title)
            if description is not None:
                update_fields.append("description = %s")
                update_values.append(description)
            if due_date is not None:
                update_fields.append("due_date = %s")
                update_values.append(due_date)
            if status is not None:
                update_fields.append("status = %s")
                update_values.append(status)
            
            if not update_fields:
                print("No fields to update")
                return False
            
            update_values.append(task_id)
            query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE Taskid = %s"
            cursor.execute(query, update_values)
            self.connection.commit()
            print("Task updated successfully")
            return True
        except Error as e:
            print(f"Error updating task: {e}")
            return False
        
    #Mark a specific task as complete
    def mark_task_complete(self, task_id):
        if not self.connection:
            print("Database connection failed")
            return False
        
        try:
            cursor = self.connection.cursor()
            query = "UPDATE tasks SET status = 'Completed' WHERE TaskID = %s"
            cursor.execute(query, (task_id,))
            self.connection.commit()
            if cursor.rowcount > 0:
                print("Task marked as complete successfully")
                return True
            else:
                print("Task not found or already completed")
                return False
        except Error as e:
            print(f"Error marking task as complete: {e}")
            return False
    
    #Delete a specific task
    def delete_task(self, task_id):
        if not self.connection:
            print("Database connection failed")
            return False
        
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM tasks WHERE Taskid = %s"
            cursor.execute(query, (task_id,))
            self.connection.commit()
            if cursor.rowcount > 0:
                print("Task deleted successfully")
                return True
            else:
                print("Task not found")
                return False
        except Error as e:
            print(f"Error deleting task: {e}")
            return False
    
    #Ends the database connection
    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

# Display menu for task management options
def display_menu():
    print("\nTask Manager Menu:")
    print("1. Create a new task")
    print("2. View all tasks")
    print("3. Update a Task")
    print("4. Mark a task as complete")
    print("5. Delete a task")
    print("6. Exit")

# Display, menu for sort options for tasks
def sort_menu():
    print("\nSort Options:")
    print("1. Sort by Default (Creation Timestamp)")
    print("2. Sort by Priority Level")
    print("3. Sort by Due Date")
    print("4. Sort by Status")
    print("5. Sort by Title")

def main():
    # Initialize the database connection
    manager = TaskManager()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            # Create task
            title = input("Enter task title: ")
            description = input("Enter task description (optional): ")
            due_date = input("Enter due date (YYYY-MM-DD, optional): ")
            prioritylevel = input("Enter priority level (Low/Medium/High, default Low): ")
            if prioritylevel not in ['Low', 'Medium', 'High']:
                    prioritylevel = 'Low'
            status = input("Enter status (Pending/In Progress/Completed, default Pending): ")
            if status not in ['Pending', 'In Progress', 'Completed']:
                status = 'Pending'

            if not due_date:
                due_date = None

            manager.create_task(title, description or None, due_date, prioritylevel, status)

        elif choice == '2':
            sortToggle = input("Sort tasks? (yes/no): ").strip().lower()
            if sortToggle == 'yes':
                # Display sort options

                sort_menu()
                sort_choice = input("Enter your choice (1-5): ")
                if sort_choice == '1':
                    # Default sorting by creation timestamp
                    tasks = manager.read_tasks()
                elif sort_choice == '2':
                    # Sort by priority level
                    tasks = manager.read_tasks()
                    tasks.sort(key=lambda x: x['PriorityLevel'])
                elif sort_choice == '3':
                    # Sort by due date
                    tasks = manager.read_tasks()
                    tasks.sort(key=lambda x: x['DueDate'])
                elif sort_choice == '4':
                    # Sort by status
                    tasks = manager.read_tasks()
                    tasks.sort(key=lambda x: x['Status'])
                elif sort_choice == '5':
                    # Sort by title
                    tasks = manager.read_tasks()
                    tasks.sort(key=lambda x: x['Title'])
                else:
                    print("Invalid choice")
                    continue
            elif sortToggle == 'no':
                # Default sorting by creation timestamp
                tasks = manager.read_tasks()
            else:
                print("Invalid input, please enter 'yes' or 'no'")
                continue
            # Display tasks
            if tasks:
                print("\nAll Tasks:")
                for task in tasks:
                    print(f"\nTask ID: {task['TaskID']}")
                    print(f"Title: {task['Title']}")
                    print(f"Description: {task['Description']}")
                    print(f"Due Date: {task['DueDate']}")
                    print(f"Priority Level: {task['PriorityLevel']}")
                    print(f"Status: {task['Status']}")
                    print(f"Created At: {task['CreationTimestamp']}")
            else:
                print("No tasks found")
        
       
        
        elif choice == '3':
            # Update task
            task_id = input("Enter task ID to update: ")
            try:
                task_id = int(task_id)
                # Check if task exists
                task = manager.read_tasks(task_id)
                if not task:
                    print("Task not found")
                    continue
                
                print("\nLeave field blank to keep current value")
                title = input(f"New title (current: {task['Title']}): ")
                description = input(f"New description (current: {task['Description']}): ")
                due_date = input(f"New due date (YYYY-MM-DD, current: {task['DueDate']}): ")
                prioritylevel = input(f"New priority level (Low/Medium/High, current: {task['PriorityLevel']}): ")
                if prioritylevel not in ['Low', 'Medium', 'High']:
                    prioritylevel = 'Low'
                status = input(f"New status (Pending/In Progress/Completed, current: {task['Status']}): ")
                if status not in ['Pending', 'In Progress', 'Completed']:
                    status = 'Pending'

                # Convert empty strings to None
                title = title if title else None
                description = description if description else None
                due_date = due_date if due_date else None
                status = status if status else None
                
                manager.update_task(task_id, title, description, due_date, status)
            except ValueError:
                print("Invalid task ID")

        elif choice == '4':
            # Mark task as complete
            task_id = input("Enter task ID to mark as Complete: ")
            try:
                task_id = int(task_id)
                # Check if task exists
                task = manager.read_tasks(task_id)
                if not task:
                    print("Task not found")
                    continue
                manager.mark_task_complete(task_id)
            except ValueError:
                print("Invalid task ID")
        
        elif choice == '5':
            # Delete task
            task_id = input("Enter task ID to delete: ")
            try:
                task_id = int(task_id)
                manager.delete_task(task_id)
            except ValueError:
                print("Invalid task ID")
        
        elif choice == '6':
            # Exit
            manager.close_connection()
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    # First, create the database and table if they don't exist
    connection = create_database_connection()
    if connection and connection.is_connected():
        connection.close()
    
    # Then run the main application
    main()