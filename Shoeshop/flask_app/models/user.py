from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



db= 'ecommerce'
class User:
    def __init__(self,data):
        self.id = data['id']
        self.password = data['password']
        self.email = data['email']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.address = data['address']
        self.zipcode = data['zipcode']
        self.city = data['city']
        self.state = data['state']
        self.country = data['country']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.phone = data['phone']
        self.admin = data['admin']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (firstName, lastName, email, password, address, zipcode, city, state, country, phone) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s, %(address)s, %(zipcode)s, %(city)s, %(state)s, %(country)s, %(phone)s);"
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])  




















    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, user)
        print(results)
        if len(results) >=1:
            flash("Account already exists with this email", 'register')
            is_valid = False
        if (bool(re.search(r'\d', user['firstName']))) == True:
            flash("First name must only contain letters", 'register')
            is_valid = False
        if len(user['firstName']) < 1:
            flash("First name may not be left blank", 'register')
            is_valid = False
        if len(user['firstName']) < 2:
            flash("First name must be at least 2 characters", 'register')
            is_valid = False
        if (bool(re.search(r'\d', user['lastName']))) == True:
            flash("Last name must only contain letters", 'register')
            is_valid = False
        if len(user['lastName']) < 1:
            flash("Last name may not be left blank", 'register')
            is_valid = False
        if len(user['lastName']) < 2:
            flash("Last name must be at least 2 characters", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['email']) < 1:
            flash("Email may not be left blank", 'register')
            is_valid = False
        if len(user['password']) < 1:
            flash("Password must be at least 1 characters", 'register')
            is_valid = False
        if len(user['password']) < 1:
            flash("Password may not be left blank", 'register')
            is_valid = False
        if user['password'] != user['confirmPassword']:
            flash("Passwords do not match!", 'register')
            is_valid = False
        return is_valid
        



class Product:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.description = data['description']
        self.image = data['image']
        self.stock = data['stock']
        self.category_id = data['category_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO products (name, price, description, image, stock, category_id) VALUES (%(name)s, %(price)s, %(description)s, %(image)s, %(stock)s, %(category_id)s);"
        return connectToMySQL(db).query_db(query, data)