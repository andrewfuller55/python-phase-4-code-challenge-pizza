#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
# from werkzeug.exceptions import 
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


# @app.route('/restaurants')
# def restaurants():

#     restaurants = []
#     for restaurant in Restaurant.query.all():
#         restaurant_dict = restaurant.to_dict()
#         restaurants.append(restaurant_dict)

#     response = make_response(
#         restaurants,
#         200
#     )

#     return response

class Restaurants(Resource):

    def get(self):
        restaurants = [restaurant.to_dict(rules=('-restaurant_pizzas',)) for restaurant in Restaurant.query.all()]
        return make_response(jsonify(restaurants), 200)

api.add_resource(Restaurants, '/restaurants')


# @app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
# def restaurant_by_id(id):
#     restaurant = Restaurant.query.filter(Restaurant.id == id).first()

#     if restaurant == None:
#         response_body = {
#             "error": "Restaurant not found"
#         }
#         response = make_response(response_body, 404)

#         return response

#     else:
#         if request.method == 'GET':
#             restaurant_dict = restaurant.to_dict()

#             response = make_response(
#                 restaurant_dict,
#                 200
#             )

#             return response

#         elif request.method == 'DELETE':
#             db.session.delete(restaurant)
#             db.session.commit()

#             return make_response('', 204)

class RestaurantByID(Resource):

    def get(self, id):

        restaurant = Restaurant.query.filter_by(id=id).first()
        
        if restaurant:
            return restaurant.to_dict(), 200
        else:
            return make_response({"error": "Restaurant not found"}, 404)
    
    def delete(self, id):

        restaurant = Restaurant.query.filter_by(id=id).first()
        
        if not restaurant:
            return make_response({"error": "Restaurant not found"}, 404)
        
        db.session.delete(restaurant)
        db.session.commit()

        return {}, 204


api.add_resource(RestaurantByID, '/restaurants/<int:id>')




# @app.route('/pizzas')
# def pizzas():

#     pizzas = []
#     for pizza in Pizza.query.all():
#         pizza_dict = pizza.to_dict()
#         pizzas.append(pizza_dict)

#     response = make_response(
#         pizzas,
#         200
#     )

#     return response


class Pizzas(Resource):

    def get(self):
        pizzas = [pizza.to_dict(rules=('-restaurant_pizzas',)) for pizza in Pizza.query.all()]
        return make_response(jsonify(pizzas), 200)

api.add_resource(Pizzas, '/pizzas')


class RestaurantPizzas(Resource):

    def post(self):


        try:
            data = request.get_json()

            new_obj = RestaurantPizza(
                price=data['price'],
                pizza_id=data['pizza_id'],
                restaurant_id=data['restaurant_id'],
            )

            db.session.add(new_obj)
            db.session.commit()

            return make_response(new_obj.to_dict(), 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
    


    # @app.errorhandler(BadRequest)
    # def handle_not_found(e):

    #     response = make_response({
    #         "errors": ["validation errors"]
    #     })

    #     return response

    # app.register_error_handler(400, handle_not_found)

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
