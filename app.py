import os
from flask import Flask , render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#database creation and connection

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.root_path, "form.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db= SQLAlchemy(app)

class form(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    college = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno } - { self.name }"

with app.app_context():
    #this will create database file using the models above only if it does not exist already
    db.create_all()


#routes

#home page

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        college = request.form['college']
        info = form(name=name, email=email, phone=phone, college=college)
        db.session.add(info)
        db.session.commit()

    form_data = form.query.all()
    return render_template('index.html',form_data=form_data)


#view data block route

@app.route('/#viewData')
def viewData():
    form_data = form.query.all()
    return render_template('index.html',form_data=form_data)

#update data route

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        college = request.form['college']
        info = form.query.filter_by(sno=sno).first()
        info.name = name
        info.email = email
        info.phone = phone
        info.college = college
        db.session.add(info)
        db.session.commit()
        return redirect('/')

    form_data = form.query.filter_by(sno=sno).first()
    return render_template('update.html', form_data=form_data)





#delete data route

@app.route('/delete/<int:sno>')
def delete(sno):
    info = form.query.filter_by(sno=sno).first()
    db.session.delete(info)
    db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)