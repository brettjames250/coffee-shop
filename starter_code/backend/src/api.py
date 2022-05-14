import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
db_drop_and_create_all()

# ROUTES
@app.route("/", methods=["GET"])
def test_initilisation():
    return jsonify({
        "success": True,
        "drinks": "yeah"
    })
    
'''
implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=["GET"])
def get_drinks():
    drinks = Drink.query.all()
    formatted_drinks = []
    
    for drink in drinks:
        formatted_drinks.append(drink.short())
    
    return jsonify({
        "success": True,
        "drinks": formatted_drinks
    })


'''
implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail", methods=["GET"])
def get_drinks_detail():
    drinks = Drink.query.all()
    formatted_drinks = []
    
    for drink in drinks:
        formatted_drinks.append(drink.long())
    
    return jsonify({
        "success": True,
        "drinks": formatted_drinks
    })


'''
implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=["POST"])
def add_new_drink():
    request_data = request.get_json()
    
    drink = Drink(
        title=request_data.get("title"),
        recipe=request_data.get("recipe")
    )
    
    drink.insert()
    
    return jsonify({
        "success": True,
        "drinks": drink.long()
    })
    
    


'''
implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:id>", methods=["PATCH"])
def update_drink(drink_id):
    drink = Drink.query.get(drink_id)
    
    if drink is None:
        abort(404)
        
    request_data = request.get_json()
    
    if request_data.get("title") is not None:
        drink.title = request_data.get("title")
    
    if request_data.get("recipe") is not None:
        drink.recipe = request_data.get("recipe")
    
    drink.update()
    
    return jsonify({
        "success": True,
        "drinks": drink
    })
    
    
        

'''
implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:id>", methods=["DELETE"])
def delete_drink(drink_id):
    drink = Drink.query.get(drink_id)
    
    if drink is None:
        abort(404)
        
    drink.delete()
    
    return jsonify({
        "success": True,
        "delete": drink.id
    })
    


'''
implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422
    
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404
    
@app.errorhandler(401)
def unauthorised(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorised"
    }), 401
    
    
@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403
    
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
    }), 500



if __name__ == "__main__":
    app.debug = True
    app.run()
