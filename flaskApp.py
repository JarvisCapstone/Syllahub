from app import create_app, db

app = create_app()

#print("db in flaskapp.py=", db)

def view_routes():
    for name, func in app.view_functions.items():
        print(name)
        print(func)
        print()