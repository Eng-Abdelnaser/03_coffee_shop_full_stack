import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth
from werkzeug.exceptions import abort , HTTPException


app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

def check_recipe_value(recipe):
    if not isinstance(recipe,list) or not isinstance(recipe,dict):
        return False
    if isinstance(recipe,list):
        for item in recipe :
            if  not isinstance(item['name'] , str) :
                return False
            if  not isinstance(item['color'] , str) :
                return False
            if  not isinstance(item['parts'] ,(str,int,float)) :
                return False
        return True    
    else:
        if ( not isinstance(recipe['name'] , str) ):
            return False
        if ( not isinstance(recipe['color'] , str) ):
            return False
        if  (not isinstance(recipe['parts'] ,(str,int,float))) :
            return False
        return True    

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',methods=['GET'])
def get_short_drinks_detail():
    drinks=Drink.query.all()
    return jsonify({
        "success": True,
        "drinks":[drink.short() for drink in drinks]
        })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail',methods=['GET'])
@requires_auth('get:drinks-detail')
def get_long_drinks_detail():
    drinks=Drink.query.all()
    return jsonify({
        "success": True,
        "drinks":[drink.long() for drink in drinks]
        } )

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',methods=['POST'])
@requires_auth('post:drinks')
def add_drink():
    body =request.get_json() 
    title=body.get('title')
    recipe=body.get('recipe')
    if (recipe is None or title is None) :
        abort(400)

    if check_recipe_value(recipe) :
        abort(422)
        
    drink=Drink(title , str(recipe)) 
    drink.insert()
    return jsonify({
        "success": True,
        "drinks":drink.long()
        })

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>',methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(id):
    body =request.get_json() 
    title=body.get('title')
    recipe=body.get('recipe')
    drink=Drink.query.filter(Drink.id==id).one_or_none()
    if drink is None:
        abort(400)
    if check_recipe_value(recipe) :
        abort(422)
    
    drink.title=title
    drink.recipe=recipe
    drink.update()
    return jsonify({
        "success": True,
        "drinks":drink.long()
        })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>',methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    body =request.get_json() 
    drink=Drink.query.filter(Drink.id==id).one_or_none()
    if drink is None:
        abort(404)
    drink.delete()
    return jsonify({
        "success": True,
        "delete":id
        })


## Error Handling
'''
Example error handling for unprocessable entity
'''

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def handling_not_found_error(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(HTTPException)
def error_handling_exception(error):
    return jsonify({
                    "success": False, 
                    "error": error.code,
                    "message": error.name
                    }), error.code

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def handling_Authexception(error):
    return jsonify({
                    "success": False, 
                    "error": error.status_code,
                    "message": error.error
                    }), error.status_code
