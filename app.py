from flask import Flask , render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
my_db = SQLAlchemy(app)


@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('index.html' , todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():
    todo_get = request.form.get('todoInput')
    new_todo = Todo(text=todo_get, complete=False)
    my_db.session.add(new_todo)
    my_db.session.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo_to_update = Todo.query.filter_by(id= todo_id).first()
    todo_to_update.complete = not todo_to_update.complete
    my_db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo_to_delete = Todo.query.filter_by(id= todo_id).first()
    my_db.session.delete(todo_to_delete)
    my_db.session.commit()
    return redirect(url_for('index'))

class Todo(my_db.Model):
    id = my_db.Column(my_db.Integer, primary_key=True)
    text = my_db.Column(my_db.String(100))
    complete = my_db.Column(my_db.Boolean)

    def __str__(self):
        return self.text

if __name__ == '__main__':
    with app.app_context():  
        my_db.create_all() 
        app.run(debug=True)
   