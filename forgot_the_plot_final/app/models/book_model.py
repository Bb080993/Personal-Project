from app.config.mysqlconnection import connectToMySQL
from app.models import user_model

from flask import flash

class Book:
    DB = "final_project"
    def __init__(self, data):
        self.id= data['id']
        self.title = data['title']
        self.author = data['author']
        self.summary= data['summary']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id=['user_id'] 
        self.created_by=None
        self.characters=[]

    @classmethod
    def create_summary(cls, data):
        query=  """
                INSERT INTO books (title, author, summary, user_id)
                VALUES (%(title)s, %(author)s, %(summary)s, %(user_id)s)
                """
        results=connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def books_by_user(cls, data):
        query=  """
                SELECT * FROM books WHERE user_id=%(id)s
                """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def one_book_with_user(cls, data):
        query=  """
                SELECT * FROM books
                 LEFT JOIN users ON users.id=books.user_id
                WHERE books.id=%(id)s
                """
        results=connectToMySQL(cls.DB).query_db(query, data)
        one_book_with_user=cls(results[0])
        for row in results:
            one_book_user_info={
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "username": row["username"],
                "createdAt":row["users.createdAt"],
                "updatedAt": row["users.updatedAt"]

            }
            user=user_model.User(one_book_user_info)
            one_book_with_user.created_by=user
        print("!ONE Book WITH USER!",one_book_with_user)
        return one_book_with_user
    
    @staticmethod
    def validate_new_summary(data):
        is_valid=True

        if len(data["title"])<3:
            flash("Title must be at least 3 characters.",'book')
            is_valid=False
        if len(data["author"])<3:
            flash("Author must be at least 3 characters.", 'book')
            is_valid=False
        if len(data["summary"])<10:
            flash("Summary must be at least 10 characters.", 'book')
            is_valid=False
        
        return is_valid