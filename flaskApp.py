from app import create_app

app = create_app()

for name, func in app.view_functions.items():
    print(name)
    print(func)
    print()