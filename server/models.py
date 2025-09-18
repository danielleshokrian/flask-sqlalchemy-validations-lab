from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validators 
    @validates('name')
    def validate_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Author must have a name.")
        
        existing = Author.query.filter_by(name=value).first()
        if existing and existing.id != self.id:
            raise ValueError("Author name must be unique.")
        
        return value
    
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise ValueError("Phone number must be exactly 10 digits.")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validators
    @validates('content')
    def validate_content(self, key, value):
        if not value or len(value) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if not value or len(value) > 250:
            raise ValueError("Summary must be at most 250 characters long.")
        return value
    
    @validates('category')
    def validate_category(self, key, value):
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'.")
        return value
    
    @validates('title')
    def validate_title(self, key, value):
        if not value or not any(phrase in value for phrase in ["Wont Believe", "Won't Believe","Secret", "Top", "Guess"]):
            raise ValueError("Title must be present and contain at least one of the following phrases: 'Wont Believe', 'Secret', 'Top', 'Guess'.")
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
