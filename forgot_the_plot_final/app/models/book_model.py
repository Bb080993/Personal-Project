from app.config.mysqlconnection import connectToMySQL
from app.models import user_model
from app.models import character_model

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

# create a book summary
    @classmethod
    def create_summary(cls, data):
        query=  """
                INSERT INTO books (title, author, summary, user_id)
                VALUES (%(title)s, %(author)s, %(summary)s, %(user_id)s)
                """
        results=connectToMySQL(cls.DB).query_db(query, data)
        return results
    
#   get all the books from one user
    @classmethod
    def books_by_user(cls, data):
        query=  """
                SELECT * FROM books WHERE user_id=%(id)s
                ORDER BY books.id DESC 
                """
        return connectToMySQL(cls.DB).query_db(query, data)

#get one single book with its user    
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
        # print("!ONE Book WITH USER!",one_book_with_user)
        return one_book_with_user

#edit info for a book   
    @classmethod
    def edit_one_book(cls, data):
        query=  """
                UPDATE books
                SET title=%(title)s, author=%(author)s, summary=%(summary)s
                WHERE id=%(id)s
                """
        results=connectToMySQL(cls.DB).query_db(query, data)
        return results

#delete one book    
    @classmethod
    def delete(cls, data):
        query=  """
                DELETE FROM books
                WHERE id=%(id)s
                """
        return connectToMySQL(cls.DB).query_db(query, data)

#get all books in the db with its user info    
    @classmethod
    def get_all_books_with_user(cls):
        query="""
                SELECT * FROM books
                LEFT JOIN users ON users.id=books.user_id
                ORDER BY books.id DESC 
                LIMIT 10
                
            """
        results=connectToMySQL(cls.DB).query_db(query)
        all_books=[]
        for row in results:
            one_book=cls(row)
            one_book_user_info={
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "username":row["username"],
                "password":row["password"],
                "createdAt":row["users.createdAt"],
                "updatedAt": row["users.updatedAt"]
            }
            user=user_model.User(one_book_user_info)
            one_book.created_by=user
            # print(one_book.__dict__)
            all_books.append(one_book)
        # print("ALL books with user", all_books)
        return all_books
    
#get all characters for one book
    @classmethod
    def get_all_characters_from_book(cls, data):
        
        query="""SELECT * FROM books
        LEFT JOIN characters ON characters.book_id=books.id
        WHERE books.id=%(id)s;"""
        results=connectToMySQL(cls.DB).query_db(query, data)
        # print("BOOK CHARACTERS", results)
        book=cls(results[0])
        # print("!!!!!!!", book)
        for row in results:
            character_data= {"id":row ["characters.id"],
                "name" :row ["name"],
                "description": row ["description"],
                "createdAt": row ["characters.createdAt"],
                "updatedAt" :row ["characters.updatedAt"],
                "book_id":row ["book_id"] }
            book.characters.append(character_model.Character(character_data))
        # print("Characters", book.characters)
        return book.characters

#search by title containing
    @classmethod
    def search_by_title(cls, data):
        print("DATA", data)
        query=  """
                SELECT * FROM books
                WHERE title LIKE %(title)s
                """
        results=connectToMySQL(cls.DB).query_db(query, data)
        print("SEARCH RESULTS", results)
        return results
        

 #validate book in form   
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