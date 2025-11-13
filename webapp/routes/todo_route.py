from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_required
from datetime import datetime
from webapp import app
from webapp.forms.todo_form import TaskForm

todo_list = [
    {'id': 1, 'task': 'Belajar Flask', 'done': False, 'created_at': 'Fri, 5 Apr 2019, 10:00', 'completed_at': None},
    {'id': 2, 'task': 'Integrasi Bootstrap', 'done': True, 'created_at': 'Fri, 12 Nov 2019, 10:30', 'completed_at': 'Sat, 13 Nov 2019, 11:30'},
]
next_id = 3

@app.route('/')
@login_required
def index():
    recent_todos_first = todo_list[::-1]
    form = TaskForm()
    return render_template('main_templates/index.html', todos=recent_todos_first, form=form)

@app.route('/api/todos', methods=['GET'])
@login_required
def get_todos():
    return jsonify(todo_list), 200

@app.route('/add', methods=['POST'])
@login_required
def add_todo():
    form = TaskForm()
    global next_id
    task_name = form.taskName.data
    if form.validate_on_submit():
        now = datetime.now()
        formatted_date = now.strftime("%a, %d %b %Y, %H:%M")
        
        new_todo = {
            'id': next_id, 
            'task': task_name, 
            'done': False,
            'created_at': formatted_date
        }
        todo_list.append(new_todo)
        next_id += 1
        
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>', methods=['POST'])
@login_required
def complete_todo(todo_id):
    for todo in todo_list:
        if todo['id'] == todo_id:
            new_status = not todo['done']
            todo['done'] = new_status
            
            if new_status:
                now = datetime.now()
                formatted_date = now.strftime("%a, %d %b %Y, %H:%M")
                todo['completed_at'] = formatted_date
            else:
                todo['completed_at'] = None
            break
            
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
@login_required
def delete_todo(todo_id):
    global todo_list
    todo_list = [todo for todo in todo_list if todo['id'] != todo_id]
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['POST'])
@login_required
def edit_todo(todo_id):
    form = TaskForm()
    task_name = form.taskName.data
    
    if form.validate_on_submit():
        for todo in todo_list:
            if todo['id'] == todo_id:
                todo['task'] = task_name
                break                
    return redirect(url_for('index'))