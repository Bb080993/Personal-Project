from app.config.mysqlconnection import connectToMySQL

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

    @classmethod
    def create_summary(cls, data):
        query=  """
                INSERT INTO books (title, author, summary, user_id)
                VALUES (%(title)s, %(author)s, %(summary)s, %(user_id)s)
                """
        results=connectToMySQL(cls.DB).query_db(query, data)
        return results
    
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