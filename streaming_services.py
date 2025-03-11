import json
import uuid

class User:
    def __init__(self, username, password):
        self.user_id = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.subscribed_plan = None

class SubscriptionPlan:
    def __init__(self, name, price, features):
        self.name = name
        self.price = price
        self.features = features

class Content:
    def __init__(self, title, genre, rating):
        self.title = title
        self.genre = genre
        self.rating = rating

class StreamingService:
    def __init__(self):
        self.users = {}
        self.plans = []
        self.contents = []
        self.load_data()

    def load_data(self):
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.users = {k: User(**v) for k, v in data.get('users', {}).items()}
                self.plans = [SubscriptionPlan(**plan) for plan in data.get('plans', [])]
                self.contents = [Content(**content) for content in data.get('contents', [])]
        except FileNotFoundError:
            print("No data file found. Starting fresh.")

    def save_data(self):
        data = {
            'users': {user_id: user.__dict__ for user_id, user in self.users.items()},
            'plans': [plan.__dict__ for plan in self.plans],
            'contents': [content.__dict__ for content in self.contents]
        }
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def register_user(self, username, password):
        if username in self.users:
            return "Username already exists."
        user = User(username, password)
        self.users[username] = user
        self.save_data()
        return "User registered successfully."

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return user
        return None

    def add_subscription_plan(self, name, price, features):
        plan = SubscriptionPlan(name, price, features)
        self.plans.append(plan)
        self.save_data()

    def add_content(self, title, genre, rating):
        content = Content(title, genre, rating)
        self.contents.append(content)
        self.save_data()

    def display_content(self):
        return [f"{content.title} ({content.genre}) - Rating: {content.rating}" for content in self.contents]

    def subscribe_user(self, username, plan_name):
        user = self.users.get(username)
        plan = next((plan for plan in self.plans if plan.name == plan_name), None)
        if user and plan:
            user.subscribed_plan = plan
            self.save_data()
            return "Subscription successful."
        return "Invalid user or plan."

    def list_plans(self):
        return [f"{plan.name}: ${plan.price} - Features: {', '.join(plan.features)}" for plan in self.plans]

def main():
    service = StreamingService()
    
    while True:
        print("\n--- Streaming Service ---")
        print("1. Register User")
        print("2. Login")
        print("3. Add Subscription Plan")
        print("4. Add Content")
        print("5. Display Content")
        print("6. Subscribe User")
        print("7. List Plans")
        print("8. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(service.register_user(username, password))
        
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = service.authenticate_user(username, password)
            if user:
                print(f"Welcome {user.username}")
            else:
                print("Invalid credentials.")
        
        elif choice == '3':
            name = input("Enter plan name: ")
            price = float(input("Enter plan price: "))
            features = input("Enter plan features (comma separated): ").split(',')
            service.add_subscription_plan(name, price, [feature.strip() for feature in features])
            print("Subscription plan added successfully.")
        
        elif choice == '4':
            title = input("Enter content title: ")
            genre = input("Enter content genre: ")
            rating = float(input("Enter content rating: "))
            service.add_content(title, genre, rating)
            print("Content added successfully.")
        
        elif choice == '5':
            contents = service.display_content()
            print("\nAvailable Contents:")
            for content in contents:
                print(content)
        
        elif choice == '6':
            username = input("Enter username: ")
            plan_name = input("Enter plan name: ")
            print(service.subscribe_user(username, plan_name))
        
        elif choice == '7':
            plans = service.list_plans()
            print("\nAvailable Subscription Plans:")
            for plan in plans:
                print(plan)
        
        elif choice == '8':
            print("Exiting the service...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()