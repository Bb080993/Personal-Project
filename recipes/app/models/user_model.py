
from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
DB = "recipes"

class User:
    DB = "recipes"
    def __init__(self, data):
        self.id= data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password= data["password"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes=[]
        #self.anything that is a many relationship to connect to=[]
        #self.if this is the many that needs to be equal eventually to one= None
    #Insert into database
    @classmethod
    def insert_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"    
        return connectToMySQL(cls.DB).query_db(query, data)
    #Validation
    @staticmethod
    def validate_user(form_data):
        
        is_valid=True
        if len(form_data['first_name'])<2:
            flash("First Name Required", 'register')
            is_valid=False
        if len(form_data['last_name'])<2:
            flash("Last Name Required", 'register')
            is_valid=False
        if len(form_data['email'])<1:
            flash("Email Required", 'register')
            is_valid=False
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid Email", 'register')
            is_valid=False
        if form_data["password"] != form_data["confirm_password"]:
            flash("Passwords do not match!", 'register')
            is_valid=False
        query="""SELECT * FROM users WHERE email=%(email)s"""
        response=connectToMySQL(DB).query_db(query, form_data)
        print(response)
        if len(response)>0:
            flash("User already exists", 'register')
            is_valid= False
        
        return is_valid
    @classmethod
    def find_user_by_email(cls, email):
        query="""SELECT * FROM users WHERE email=%(email)s"""
        response=connectToMySQL(cls.DB).query_db(query, email)
        print(response)

        if len(response)<1:
            return False
        return cls(response[0])
    #Get user by id
    @classmethod
    def get_user_by_id(cls, id):
        query= """SELECT * FROM users WHERE id=%(id)s """
        results= connectToMySQL(cls.DB).query_db(query, id)[0]
        print("!!!!!!!!!!!", results)
        return results
