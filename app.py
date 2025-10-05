from flask import Flask, render_template, request, redirect, url_for
from models import db, Contact
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create DB file
with app.app_context():
    if not os.path.exists("contacts.db"):
        db.create_all()

@app.route('/')
def index():
    query = request.args.get('q')
    if query:
        contacts = Contact.query.filter(
            (Contact.name.ilike(f'%{query}%')) |
            (Contact.email.ilike(f'%{query}%'))
        ).all()
    else:
        contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)


@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        new_contact = Contact(name=name, email=email, phone=phone)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.email = request.form['email']
        contact.phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', contact=contact)

@app.route('/delete/<int:id>')
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)