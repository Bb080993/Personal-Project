from app.config.mysqlconnection import connectToMySQL

from flask import flash

class Character:
    DB = "final_project"
    def __init__(self, data):
        self.id= data['id']
        self.name = data['name']
        self.description = data['description']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.book_id=['book_id'] 
        self.book_in=None

    @classmethod
    def add_character(cls, data):
        query=  """
                INSERT INTO characters (name, description, book_id)
                VALUES (%(name)s, %(description)s, %(book_id)s)
                """
        results=connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @staticmethod
    def validate_character(data):
        is_valid=True

        if len(data["name"])<1:
            flash("Name must be at least 1 characters.",'character')
            is_valid=False
        if len(data["description"])<3:
            flash("Description must be at least 3 characters.", 'character')
            is_valid=False

        return is_valid