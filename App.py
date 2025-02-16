from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)  #__name__ is a built-in variable, it is assigned the name of the current running file.

# Flask uses __name__ to determine the location of the application (or module) so it can:
# Find resources like templates or static files.
# Handle relative paths for configurations.

# app is the variable that holds the Flask application instance.
# You use it to define routes, configurations, and other behaviors of your application.

# @app.route("/")
# def hello_world():
#     return "<p>Hello World!!</p>"
# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # Example SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
# Link SQLAlchemy to Flask
db.init_app(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(200), nullable=False)

@app.route("/", methods=["GET", "POST"])
def get_tasks():
    if request.method == "POST":
        task = request.form.get("task_name")
        desc = request.form.get("desc")
        if task == "" or desc == "":
            print("Enter data")
        else:
            task_value = Task(task_name=task, desc=desc)
            db.session.add(task_value)
            db.session.commit()
    tasks = db.session.query(Task).all()
    # data = [{"id":task.id, "task_name": task.task_name, "description": task.desc} for task in tasks]
    # return jsonify(data)
    return render_template('appUI.html', tasks = tasks)

@app.route("/delete/<int:id>")
def delete_task(id):
    task = db.session.query(Task).filter_by(id = id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>" , methods=["GET", "POST"])
def update_task(id):
    if request.method == "POST":
        task_name = request.form.get("task_name")
        desc = request.form.get("desc")
        task = db.session.query(Task).filter_by(id = id).first()
        task.task_name = task_name
        task.desc = desc
        db.session.add(task)
        db.session.commit()
        return redirect("/")
    task = db.session.query(Task).filter_by(id=id).first()
    return render_template('update.html', task=task)

# @app.route("/addTask", methods=["GET", "POST"])
# def add_task():
#     if request.method == "POST":
#         task = request.form.get("task")
#         desc = request.form.get("desc")
#         print(f"value of task {task}",file=sys.stdout)
#         if len(task) == 0:  # Check if the task is empty
#             return task, 400
#         task_value = Task(task_name = task, desc = desc)
#         db.session.add(task_value)
#         db.session.commit()
#         return "<p>Task added successfully!</p>"
#     return '''
#     <form method="POST" action="/addTask">
#     <label for="task">New Task:</label><br>
#     <input type="text" id="task" name="task" required><br><br>
#     <label for="task">Description:</label><br>
#     <input type="text" id="desc" name="desc" required><br><br>
#     <button type="submit">Add Task</button>
#     </form>
#     '''
if __name__ == '__main__':
    app.run(debug=True)