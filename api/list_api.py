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