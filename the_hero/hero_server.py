from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

# TODO This can't be seen in the docker execution
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
    # TODO Split time into YYYY:MM:DD HH:mm:SS dropdowns and all the associated code with that
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

    if 'delete' in request.form:
        print("DELETE")
        if select is not None:
            hero_db = HeroDatabase()
            hero_db.connect()
            hero_db.remove_person_from_database(str(select))
            hero_db.close()
            return show_events()
    if 'modify' in request.form:
        new_name = form.new_name.data
        hero_db.connect()
        hero_db.rename_person_in_database(str(select), new_name)
        hero_db.close()
        return show_events()
    return render_template('formpeople.html', title='People', form=form)


if __name__ == '__main__':
    app.run()
