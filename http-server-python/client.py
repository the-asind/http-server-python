import sys, requests, base64

BASE_URL = 'http://localhost:5000'

def delete_user(user_id, username, password):
    auth_str = base64.b64encode(f"{username}:{password}".encode()).decode()
    headers = {'Authorization': f"Basic {auth_str}"}
    r = requests.delete(f"{BASE_URL}/user/{user_id}", headers=headers)
    return r.json()

def create_user(username, password, role='user'):
    data = {'username': username, 'password': password, 'role': role}
    r = requests.post(f"{BASE_URL}/user", json=data)
    return r.json()

def update_user(user_id, username, password, new_data):
    auth_str = base64.b64encode(f"{username}:{password}".encode()).decode()
    headers = {'Authorization': f"Basic {auth_str}"}
    r = requests.put(f"{BASE_URL}/user/{user_id}", json=new_data, headers=headers)
    return r.json()

def get_user(user_id):
    r = requests.get(f"{BASE_URL}/user/{user_id}")
    return r.json()

def get_all_users():
    r = requests.get(f"{BASE_URL}/users")
    return r.json()

def show_menu():
    print("\nHTTP Server Client")
    print("1. Create user")
    print("2. Get user by ID")
    print("3. Get all users")
    print("4. Delete user")
    print("5. Exit")
    return input("Choose option (1-5): ")

def interactive_mode():
    while True:
        choice = show_menu()
        
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role (admin/user): ")
            print(create_user(username, password, role))
            
        elif choice == '2':
            user_id = int(input("Enter user ID: "))
            print(get_user(user_id))
            
        elif choice == '3':
            print(get_all_users())
            
        elif choice == '4':
            user_id = int(input("Enter user ID to delete: "))
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            print(delete_user(user_id, username, password))
            
        elif choice == '5':
            print("Goodbye!")
            break
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    interactive_mode()
