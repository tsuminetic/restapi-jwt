from flask import Blueprint, request, jsonify,render_template
import datetime
from models.note import Note
from app import db
from utils import auth

api=Blueprint('note_api', __name__)

@api.route('/')
def home():
    return render_template('login.html')
    


@api.route('/notes')
@auth.token_required
def allnotes(current_user, token):
    data =[]
    for note in current_user.notes:
        data.append(dict(id=note.id, data=note.data, completed=note.completed))
    return jsonify({"data":data,
                    "metadata":{"total":len(current_user.notes)}
                    })

@api.route('/notes/<int:note_id>')
@auth.token_required
def get_note(current_user, token, note_id):
    note = Note.query.get(note_id)
    if note:
        return jsonify({
            'data':dict(id=note.id, data=note.data, completed=note.completed)
        })

@api.route('/notes/<int:note_id>', methods=['DELETE'])
@auth.token_required
def delete_note(current_user, token, note_id):
    note = Note.query.get(note_id)
    if note:
        if note.user_id==current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({
        'message':'deleted!'
    })

@api.route('/notes/<int:note_id>', methods=['PUT'])
@auth.token_required
def notecompleted(current_user, token, note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error':'resource not found'})
    note.completed=request.json['completed']
    db.session.commit()
    print(request.json['completed'])
    return jsonify({
            'data':dict(id=note.id, data=note.data, completed=note.completed)
        })

@api.route('/notes', methods=['POST'])
@auth.token_required
def addnote(current_user, token):
    note=request.form['note']
    due_date_str = request.form.get('duedate')

    if len(note) < 1:
        return jsonify({
                'error':'bad request note empty'
            })
    else:
        try:
            due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError as e:
            return jsonify({
                'error':'bad request due date error'
            })
        note = Note(data=note, due_date=due_date, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()

    return jsonify({
        'data':dict(id=note.id, data=note.data, completed=note.completed)
    }), 201

