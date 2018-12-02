from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField

import shelve
import User

app = Flask(__name__)

class RequiredIf(object):

    def __init__(self, *args, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                validators.Optional()(field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data:
                    validators.DataRequired().__call__(form, field)
                else:
                    validators.Optional().__call__(form, field)

class RegisterUser(Form):
    firstname = StringField('Firstname', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastname = StringField('Lastname', [validators.Length(min=1, max=150), validators.DataRequired()])
    membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    remarks = TextAreaField('Remarks', [RequiredIf(membership='P')])


@app.route('/')
def home():
    return render_template('HelloWorld.html')

@app.route('/newUser', methods=['GET', 'POST'])
def newUser():
    form = RegisterUser(request.form)
    if request.method == 'POST' and form.validate():

        userList = {}
        db = shelve.open('storage.db', 'c')

        try:
            userList = db['Users']
        except:
            print("fail in open db")

        #userid = len(userList) + 1
        user = User.User(form.firstname.data, form.lastname.data, form.membership.data, form.gender.data, form.remarks.data)

        userList[user.get_userID()] = user
        db['Users'] = userList

        db.close()

        return redirect(url_for('contact'))

    return render_template('NewUser.html', form=form)

@app.route('/details')
def details():
    userList = {}
    db = shelve.open('storage.db', 'r')
    userList = db['Users']
    db.close()

    list = []
    for key in userList:
        user = userList.get(key)
        #print("here: ", user.get_userID())
        #print("here:", user.get_firstname())
        list.append(user)
    return render_template('ShowUser.html', users=list, count=len(list))


@app.route('/update/<string:id>/', methods=['GET', 'POST'])
def update_user(id):
    form = RegisterUser(request.form)
    if request.method == 'POST' and form.validate():
        userList = {}
        db = shelve.open('storage.db', 'w')
        userList = db['Users']
        id = int(id)
        user = userList.get(id)
        user.set_firstname(form.firstname.data)
        user.set_lastname(form.lastname.data)
        user.set_membership(form.membership.data)
        user.set_gender(form.gender.data)
        user.set_remarks(form.remarks.data)
        db['Users'] = userList
        db.close()

        return redirect(url_for('details'))
    else:
        userList = {}
        db = shelve.open('storage.db', 'r')
        userList = db['Users']
        db.close()

        user = userList.get(int(id))
        form.firstname.data = user.get_firstname()
        form.lastname.data = user.get_lastname()
        form.membership.data = user.get_membership()
        form.gender.data = user.get_gender()
        form.remarks.data = user.get_remarks()
        return render_template('UpdateUser.html', form=form)


@app.route('/delete_user/<string:id>', methods=['POST'])
def delete_user(id):
    userList = {}
    db = shelve.open('storage.db', 'w')
    userList = db['Users']
    id = int(id)
    userList.pop(id)
    db['Users'] = userList
    db.close()

    return redirect(url_for('details'))

@app.route('/contact')
def contact():
    return render_template('Contact.html')


if __name__ == '__main__':
    app.run()
