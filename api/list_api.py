from flask import Blueprint, request, jsonify,render_template
import datetime
from models.list import List, Item
from app import db
from utils import auth

api = Blueprint('list_api',__name__)

@api.route('/lists')
@auth.token_required
def get_lists(current_user, token):
    lists_data = []

    for user_list in current_user.lists:
        items_data = []
        for item in user_list.items:
            item_data = {
                "item": item.data,
                "item id": item.id
            }
            items_data.append(item_data)
        
        lists_data.append({
            "list id": user_list.id,
            "list name": user_list.name,
            "items": items_data
        })

    metadata = {"total_lists": len(current_user.lists)}
    
    return jsonify({
        "data": lists_data,
        "metadata": metadata
    })
    
    
@api.route('/lists', methods=['POST'])
@auth.token_required
def addlist(current_user, token):
    list_name = request.form.get('listname')

    items = request.form.getlist('item')

    if not list_name or not items:
        return jsonify({'error': 'bad request: list name or items missing'}), 400

    new_list = List(name=list_name, user_id=current_user.id)
    db.session.add(new_list)
    db.session.commit()

    for item_data in items:
        item = Item(data=item_data, list_id=new_list.id)
        db.session.add(item)

    db.session.commit()

    return jsonify({
        'data': {
            'list_id': new_list.id,
            'list_name': new_list.name,
            'items': [item.data for item in new_list.items]
        }
    }), 201
    
    
@api.route('/lists/<int:list_id>')
@auth.token_required
def get_note(current_user, token, list_id):
    user_list = List.query.get(list_id)
    if user_list:
        items_data = []
        for item in user_list.items:
            item_data = {
                "item": item.data,
                "item id": item.id
            }
            items_data.append(item_data)
        
        list_data = {
            "list id": user_list.id,
            "list name": user_list.name,
            "items": items_data
        }
        
        return jsonify({'data': list_data}), 201
    return jsonify({'message':'couldnt find the list'}), 404


@api.route('/lists/<int:list_id>', methods=['DELETE'])
@auth.token_required
def delete_list(current_user, token, list_id):
    list = List.query.get(list_id)
    if list:
        if list.user_id==current_user.id:
            db.session.delete(list)
            db.session.commit()
    return jsonify({
        'message':' listdeleted!'
    })
    
@api.route('/lists/<int:list_id>/<int:item_id>', methods=['DELETE'])
@auth.token_required
def delete_item(current_user, token, list_id, item_id):
    item = Item.query.get(item_id)
    list = List.query.get(list_id)
    if item and list and item.list_id==list_id :
        if list.user_id==current_user.id:
            db.session.delete(item)
            db.session.commit()
    return jsonify({
        'message':'item deleted!'
    })
    
@api.route('/lists/<int:list_id>', methods=['PUT'])
@auth.token_required
def edit_list_name(current_user, token, list_id):
    list = List.query.get(list_id)
    if not list:
        return jsonify({'error':'resource not found'})
    list.name=request.form.get('listname')
    db.session.commit()
    if list:
        items_data = []
        for item in list.items:
            item_data = {
                "item": item.data,
                "item id": item.id
            }
            items_data.append(item_data)
        
        list_data = {
            "list id": list.id,
            "list name": list.name,
            "items": items_data
        }
        
        return jsonify({'data': list_data}), 201
    return jsonify({'message':'couldnt find the list'}), 404