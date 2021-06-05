from flask import request, make_response, jsonify

from foodSystem import app, db
from foodSystem.models import User, Auth, Restaurant, Food, Menu, Order, OrderItem,Logins
from foodSystem.middleware import is_authenticated, is_restaurant, only_user


@app.route('/api/restaurant/food/add', methods=['POST'])
@is_authenticated
@is_restaurant
def add_food():
    data = request.get_json()
    food = Food(name=data.get('name'),price=data.get('price'),menu_id=request.user.restaurant.menu.id)
    db.session.add(food)
    db.session.commit()

    response = {
        "message":"item add successfully"
    }

    return make_response(jsonify(response))


@app.route('/api/resturant/order/list')
@is_authenticated
@is_restaurant
def get_orders():
    orders = []
    for order in Order.query.filter_by(user_id=request.user.id).all():
        orders.append(order.to_json())
    
    response = {
        "message":"orders ",
        "data" : orders
    }
    return make_response(jsonify(response))


@app.route('/api/resturant/order/<order_id>/update', methods=["PUT"])
@is_authenticated
@is_restaurant
def update_order_status(order_id):
    order = Order.query.filter_by( 
                            id=order_id,
                            restaurant_id=request.user.restaurant.id).first()
    if not order:
        response = {
            'status': 'fail',
            'message': 'Sorry this order not exists'
        }
        return make_response(jsonify(response)), 404

    order.status = 1
    db.session.add(order)
    db.session.commit()

    response = {
        'status': 'success',
        'data': order.to_json()
    }
    return make_response(jsonify(response))
    

@app.route('/api/restaurant/<restaurant_id>/menu')
@is_authenticated
def get_menu(restaurant_id):
    
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    if not restaurant:
        response = {
            'status': 'fail',
            'message': 'Sorry this restaurant not exists'
        }
        return make_response(jsonify(response)), 404
    
    response = {
        'status': 'success',
        'data': restaurant.menu.to_json()
    }
    return make_response(jsonify(response))


@app.route('/api/restaurant/list')
@is_authenticated
def all_restaurants():
    restaurants = [ item.to_json() for item in Restaurant.query.all()]
    response = {
        'status': 'success',
        'data': restaurants
    }
    return make_response(jsonify(response))
    

@app.route('/api/resturant/<restaurant_id>/order', methods=['POST'])
@is_authenticated
@only_user
def book_order(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    if not restaurant:
        response = {
            'status': 'fail',
            'message': 'Sorry this restaurant not exists'
        }
        return make_response(jsonify(response)), 404
    
    post_data = request.get_json()
    order = Order(
                restaurant_id=restaurant_id,
                user_id=request.user.id,
                address=post_data.get('address'))

    db.session.add(order)
    db.session.commit()
    for item in post_data.get('items'):
        food = Food.query.filter_by(name=item.get('name')).first()
        if food:
            order_item = OrderItem( 
                            order_id=order.id,
                            food_id=food.id,
                            quantity=item.get('quantity'))
            order_item.total_price = food.price * int(item.get('quantity'))
            db.session.add(order_item)
            db.session.commit()
            order.total_price += order_item.total_price

    response = {
            'status': 'success',
            'data': order.to_json()
        }
    return make_response(jsonify(response))


@app.route('/api/user/order/list')
@is_authenticated
@only_user
def user_oders():
    orders = [item.to_json() for item in Order.query.filter_by(user_id=request.user.id)]
    response = {
            'status': 'success',
            'data': orders
        }
    return make_response(jsonify(response))
