from app import create_app


def main() -> None:
    app = create_app()
    db = app.extension["sqlalchemy"]
    with app.app_context():
        db.create_all()
        
if __name__ == '__main__':
    main()