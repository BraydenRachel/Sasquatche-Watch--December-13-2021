from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app.models.user import User

class Recipe:
    db_name = 'sasquatches'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.location = db_data['location']
        self.what_happened = db_data['what_happened']
        self.date_of_sighting = db_data['date_of_sighting']
        self.number = db_data['number']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.first_name = None
    
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO sasquatches (location, what_happened, date_of_sighting, number, user_id) VALUES (%(location)s,%(what_happened)s,%(date_of_sighting)s,%(number)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sasquatches;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_sasquatches = []
        for row in results:
            print(row['date_of_sighting'])
            all_sasquatches.append( cls(row) )
        return all_sasquatches
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM sasquatches WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE sasquatches SET location=%(location)s, what_happened=%(what_happened)s, date_of_sighting=%(date_of_sighting)s, number=%(number)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM sasquatches WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_one_recipe_join_users(cls):
        query = "SELECT * FROM sasquatches LEFT JOIN users ON sasquatches.user_id = users.id ;"
        results = connectToMySQL('sasquatches').query_db(query)
        print(results)
        sasquatches = []
        for row in results:
            a_sas = cls(row)
            a_sas.first_name = row['first_name']
            sasquatches.append( a_sas )
        return sasquatches


    @staticmethod
    def validate_sasquatches(sasquatches):
        is_valid = True
        if len(sasquatches['location']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","sasquatches")
        if len(sasquatches['what_happened']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters","sasquatches")
        if sasquatches['date_of_sighting'] == "":
            is_valid = False
            flash("Please enter a date","sasquatches")
        if sasquatches['number'] == "":
            is_valid = False
            flash("Please enter a number","sasquatches")
        return is_valid
