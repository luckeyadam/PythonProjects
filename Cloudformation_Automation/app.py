import json
import boto3
from aws_operations import region_tasks, ami_tasks, subnet_tasks, vpc_tasks
from cloudformation_operations import top_level_json_former
from ec2_operations import webapp_former
from security_group_operations import sg_operations

"""
Flask site that builds AWS cloudformation templates
========================
"""
from flask import (Flask, render_template, redirect,
                   url_for, request, make_response, flash)

app = Flask(__name__)

# set a key for flash messages that are assigned to users
# TODO build out error handling and unit tests for application
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
                 "subnets": subnet_tasks.get_subnets(), "vpcs": vpc_tasks.get_vpc()}
    )


@app.route('/save', methods=['POST'])
def save():
    """
    Saves selections to a cookie so you dont have to re enter selections every time
    and then displays the output of the cloudformation in a flash message
    :return:
    """
    # TODO split this stuff out for better separation of concerns and error handling
    # but for quick testbed, this should work
    flash("Generated Template:")
    response = make_response(redirect(url_for('builder')))  # redirect back to index
    data = get_saved_data()  # attempt to get the cookie if its stored
    data.update(dict(request.form.items()))  # update the cookie with whats on the form
    data['jsontextarea'] = ""  # clear this out so cookie doesnt save sensitive data
    print(data)
    response.set_cookie('userdata', json.dumps(data))  # set the cookie

    # create security group if it doesnt exist
    sg = sg_operations.create_sg(vpc_tasks.return_vpc_id(data['vpcs']), "test security group from flask builder",
                                 data['installationinput'])

    template = create_cloudformation_template(data, sg)

    flash(template)

    client = boto3.client('cloudformation')
    formation_val_resp = client.validate_template(
        TemplateBody=template,
    )

    # if formation is valid, submit to create stack
    if formation_val_resp['ResponseMetadata']['HTTPStatusCode'] == 200:
        flash("template is valid building stack......")
        stack_response = client.create_stack(
            StackName=data['installationinput'] + "STACK",
            TemplateBody=template,
            TimeoutInMinutes=10,
            ResourceTypes=[
                'AWS::EC2::*',
            ],
            Tags=[
                {
                    'Key': 'Name',
                    'Value': data['installationinput'] + "STACK"
                },
            ]
        )
        flash(stack_response)
    else:
        flash("Cloudformation template may be corrupt, or there was a problem")

    return response


def create_cloudformation_template(data, sg):
    """
    build the cloudformation template
    :param data:
    :return:
    """
    # build top level json
    top_level_json = top_level_json_former.get_formation_telmplate()

    # build webapp json
    result = webapp_former.build_webapp("t2.micro", data['installationinput'], "wa01", top_level_json, sg,
                                        subnet_tasks.return_subnet_id(data['subnets']),
                                        ami_tasks.return_image_id(data['amis']))

    return json.dumps(result)


app.run(debug=True, host='0.0.0.0', port=8000)
