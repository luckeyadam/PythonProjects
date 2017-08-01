from flask import Flask
from flask import render_template

"""
The most basic flask application ever
=====================================
- /add/<number>/<number> adds two numbers
- /<name> says hello name
- defines routes for views by using app.route and switches views by calling render_template
- uses render_template / jinja to generate html docs from the /templates directory()defualt
  by passing variables to render_template
"""

app = Flask(__name__)

# set route for view for calls to / to return hello and a name if provided
@app.route('/')
@app.route('/<name>')
def index(name="Application"):
    context = {'name':name}
    return render_template("index.html", **context)

# set route to add numbers of different types together
@app.route('/add/<int:num1>/<int:num2>')
@app.route('/add/<float:num1>/<float:num2>')
@app.route('/add/<int:num1>/<float:num2>')
@app.route('/add/<float:num1>/<int:num2>')
def add(num1, num2):
    #return the add.html template from the templates directory
    context = {'num1':num1, 'num2':num2}
    return render_template("add.html", **context)

#run the app
app.run(debug=True, port=8000, host='0.0.0.0')
