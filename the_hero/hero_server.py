from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from the_hero.hero import HeroDatabase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'filesystem'


@app.route('/')
def show_events():
    hero_db = HeroDatabase()
    hero_db.connect()
    all_results = hero_db.inspect()
    people = hero_db.get_all_people_from_people()
    hero_db.close()
    return render_template('existingevents.html', title='Existing Events', rows=all_results, people=people)


class EventRegisterForm(FlaskForm):
    time = StringField("Time", validators=[DataRequired()])
    how = StringField("How", validators=[DataRequired()])
    who = StringField("Who", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/add', methods=['GET', 'POST'])
def add_event():
    form = EventRegisterForm()
    if form.validate_on_submit():
        # add event to database
        hero_db = HeroDatabase()
        hero_db.connect()
        the_time = form.time.data
        the_how = form.how.data
        the_who = form.who.data
        hero_db.new_save(the_time, the_how, the_who)
        hero_db.close()
        return show_events()
    return render_template('formadd.html', title='Add Event', form=form)


class PersonModifyForm(FlaskForm):
    people = SelectField("People", validators=[DataRequired()])
    new_name = StringField("New Name")
    delete = SubmitField("Delete")
    modify = SubmitField("Modify")


@app.route('/people', methods=['GET', 'POST'])
def modify_people():
    form = PersonModifyForm()
    # Update the people that can be selected
    hero_db = HeroDatabase()
    hero_db.connect()
    people = hero_db.get_all_people_from_people()
    hero_db.close()
    choices = []
    for p in people:
        choices.append(tuple((p[0], p[0])))
    form.people.choices = choices

    select = request.form.get('people')
    print(str(select))

    if 'delete' in request.form:
        print("DELETE")
    if 'modify' in request.form:
        print("MODIFY")
    # if request.form['Modify']:
    #     print("MODIFY")

    return render_template('formpeople.html', title='People', form=form)


if __name__ == '__main__':
    app.run()
