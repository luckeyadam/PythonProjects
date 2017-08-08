import json
from aws_operations import region_tasks, ami_tasks, subnet_tasks
from cloudformation_operations import top_level_json_former
from ec2_operations import webapp_former

"""
Flask site that builds AWS cloudformation templates
========================
"""
from flask import (Flask, render_template, redirect,
                   url_for, request, make_response, flash)

app = Flask(__name__)

# set a secret key for flash messages that are assigned to users
app.secret_key = 'asdflkj!23559086!fnasdfj&defln3'


def get_saved_data():
    try:
        data = json.loads(request.cookies.get('userdata'))  # get the userdata cookie if it exists

    except TypeError:
        data = {}
    return data


@app.route('/')
def builder():
    """
    route for requests to /
    builds options by using the aws boto3 sdk and pulling aws data
    :return:
    """
    return render_template(
        'builder.html',
        saves=get_saved_data(),
        options={"regions": region_tasks.get_regions(), "amis": ami_tasks.get_amis(),
                 "subnets": subnet_tasks.get_subnets()}
    )


@app.route('/save', methods=['POST'])
def save():
    """
    Saves selections to a cookie so you dont have to re enter selections every time
    and then displays the output of the cloudformation in a flash message
    :return:
    """
    flash("Generated Template!")
    response = make_response(redirect(url_for('builder')))  # redirect back to index
    data = get_saved_data()  # attempt to get the cookie if its stored
    data.update(dict(request.form.items()))  # update the cookie with whats on the form
    data['jsontextarea'] = ""  # clear this out so cookie doesnt save sensitive data
    response.set_cookie('userdata', json.dumps(data))  # set the cookie
    flash(create_cloudformation_template(data))
    return response


def create_cloudformation_template(data):
    """
    build the cloudformation template
    :param data:
    :return:
    """
    # build top level json
    top_level_json = top_level_json_former.get_formation_telmplate()

    # build webapp json
    result = webapp_former.build_webapp("t2.micro", data['installationinput'], "wa01", top_level_json, data['regions'],
                                        subnet_tasks.return_subnet_id(data['subnets']),
                                        ami_tasks.return_image_id(data['amis']))

    return json.dumps(result)


app.run(debug=True, host='0.0.0.0', port=8000)
