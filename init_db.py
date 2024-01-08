from app import create_app
from app.extensions import db
from app.models.Run import Run
from app.models.Post import Post

def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        
if __name__ == '__main__':
    main()