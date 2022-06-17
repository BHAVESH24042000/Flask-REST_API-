import sqlite3
from db import db

# models are for internal representation for an entity( just used by coder, not for client or API or someone else)
class ItemModel(db.Model):

    __tablename__ = 'items' # for SQLALchemy to define table name and columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self): #used to return dictionary object
        return { 'name':self.name, 'price' : self.price}   


     
    @classmethod  
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #this is SQLAlchemy implementation comes from db.Model
    
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()
        #query = "SELECT * FROM items WHERE name=?"
        #result = cursor.execute(query, (name,))
        #row = result.fetchone()
        #connection.close()
        #if row:
        #    return {'item': {'name': row[0], 'price': row[1]}}   
        #else:
        #    return None    

    
    def save_to_db(self):  # for saving and updating data through SQLALchemy
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):  # for deleting data through SQLALchemy
        db.session.delete(self)
        db.session.commit()

    #@classmethod
    #def insert(cls, item):
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()
        #query = "INSERT INTO items VALUES(?, ?)"
        #cursor.execute(query, (item['name'], item['price']))
        #connection.commit()
        #connection.close()        


    #@classmethod
    #def update(cls, item):
       # connection = sqlite3.connect('data.db')
       # cursor = connection.cursor()
       # query = "UPDATE items SET price=? WHERE name=?"
       # cursor.execute(query, (item['price'], item['name']))
        #connection.commit()
        #connection.close()    

#A class method is a method that is bound to a class rather than its object. It doesn't require creation of a class instance, much like staticmethod.
#The difference between a static method and a class method is:
#Static method knows nothing about the class and just deals with the parameters
#Class method works with the class since its parameter is always the class itself (cls).
#The class method can be called both by the class and its object.