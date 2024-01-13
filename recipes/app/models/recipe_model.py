from app.config.mysqlconnection import connectToMySQL
from app.models import user_model
from flask import flash

class Recipe:
    DB = "recipes"
    def __init__(self, data):
        self.id= data['id']
        self.name=data["name"]
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.less_than_30= data["less_than_30"]
        self.user_id= data["user_id"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.created_by= None

    @classmethod
    def get_all_recipes_with_user(cls):
        query="""
                SELECT * FROM recipes
                LEFT JOIN users ON users.id=recipes.user_id
            """
        results=connectToMySQL(cls.DB).query_db(query)
        all_recipes=[]
        for row in results:
            one_recipe=cls(row)
            one_recipe_user_info={
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            user=user_model.User(one_recipe_user_info)
            one_recipe.created_by=user
            print(one_recipe.__dict__)
            all_recipes.append(one_recipe)
        print("ALL recipes with user", all_recipes)
        return all_recipes
    
    @classmethod
    def one_recipe_with_user(cls,data):
        query="""
                SELECT * FROM recipes
                LEFT JOIN users ON users.id=recipes.user_id
                WHERE recipes.id=%(id)s
            """
        results=connectToMySQL(cls.DB).query_db(query, data)
        one_recipe_with_user=cls(results[0])
        for row in results:
            one_recipe_user_info={
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            user=user_model.User(one_recipe_user_info)
            one_recipe_with_user.created_by=user
        print("!ONE RECIPE WITH USER!",one_recipe_with_user)
        return one_recipe_with_user
        
    @classmethod
    def create_recipe(cls, data):
        query=  """
                INSERT INTO recipes (name, description, instructions, date_cooked, less_than_30, user_id)
                VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(less_than_30)s, %(user_id)s)
                """
        results=connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete_a_recipe(cls, id):
        query=  """
                DELETE FROM recipes
                WHERE id=%(id)s
                """
        results=connectToMySQL(cls.DB).query_db(query, id)
        print("DELETE", results)
        return results
    @classmethod
    def update_recipe(cls, data):
        query=  """
                UPDATE recipes
                SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked=%(date_cooked)s, less_than_30=%(less_than_30)s
                WHERE id=%(id)s
                """
        results=connectToMySQL(cls.DB).query_db(query, data)
        return results
    @staticmethod
    def validate_new_recipe(data):
        is_valid=True

        if len(data["name"])<3:
            flash("Name must be at least 3 characters.",'recipe')
            is_valid=False
        if len(data["description"])<3:
            flash("Description must be at least 3 characters.", 'recipe')
            is_valid=False
        if len(data["instructions"])<3:
            flash("Instructions must be at least 3 characters.", 'recipe')
            is_valid=False
        if not data["date_cooked"]:
            flash("Date cooked required", 'recipe')
            is_valid=False
        if "less_than_30" not in data:
            flash("Does your recipe take less than 30 minutes?", 'recipe')
            is_valid=False
        return is_valid
    