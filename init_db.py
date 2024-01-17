from app import create_app


def main() -> None:
    app = create_app(role="master")
    db = app.extensions["sqlalchemy"]
    with app.app_context():
        db.create_all()
    print("Initialized the database successfully.")
    
if __name__ == '__main__':
    main()