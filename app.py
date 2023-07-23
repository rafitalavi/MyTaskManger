from flask import Flask , render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
class TaskManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    complete = db.Column(db.Boolean)

@app.route('/')
def home():
    task_list = TaskManager.query.all()

    
    return render_template('base.html',task_list = task_list)
@app.route('/add', methods=['post'])
def add():
    title = request.form.get('title')
    new_task = TaskManager(title=title , complete =False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home")) 

@app.route("/update/<int:task_id>")
def update(task_id):
    task =TaskManager.query.filter_by(id=task_id).first()
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    task =TaskManager.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))

with app.app_context():
    db.create_all()


    #new_task = TaskManager(title = 'task 1', complete = False)
    #db.session.add(new_task)
    #db.session.commit()


