from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db = 'recipes_db'
    def __init__ (self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def getByEmail(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return False
        user = cls(result[0]) 
        return user
        
    @staticmethod
    def registrationValidation(user): #Make sure to test all validations
        email = {
            'email' : user['email']
        }
        user_O = User.getByEmail(email) #User object
        is_valid = True
        if not user['first_name'].isalpha():
            flash("Invalid First Name", 'registration')
            is_valid = False
        if not len(user['first_name']) > 2:
            flash("First name must have at least two letters.", 'registration')
            is_valid = False
        if not user['last_name'].isalpha():
            flash("Invalid Last Name", 'registration')
            is_valid = False
        if not len(user['last_name']) > 2:
            flash("Last name must have at least two letters.", 'registration')
            is_valid = False    
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email Address.", 'registration')
            is_valid = False
        if user_O:
            flash("This email is taken.", 'registration')
            is_valid = False
        if not len(user['password']) > 7:
            flash("Password is too short. Must be at least 8 characters.", 'registration')
            is_valid = False
        if not user['password'] == user['confirm_password']:
            flash("Passwords do not match.", 'registration')
            is_valid = False
        return is_valid

    @staticmethod
    def loginValidation(user):
        email_data = {  
            'email' : user['email']
        }
        is_valid = True
        user_O = User.getByEmail(email_data)
        if not user_O:
            flash("Invalid email/password.", 'login')
            is_valid = False
        elif not bcrypt.check_password_hash(user_O.password, user['password']):
            flash("Invalid email/password.", 'login')
            is_valid = False
        return is_valid