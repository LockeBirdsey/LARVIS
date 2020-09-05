from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

# This can be seen from Docker
from hero_database import HeroDatabase

# This can be seen from Pycharm
# from the_hero.hero_database import HeroDatabase

# Web server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'filesystem'

hero_db = HeroDatabase()


# Builds the main page which displays all existing events and the list of people
@app.route('/')
def show_events():
    hero_db.connect()
    all_results = hero_db.inspect_all()
    people = hero_db.get_all_people()
    hero_db.close()
    return render_template('existingevents.html', title='Existing Events', rows=all_results, people=people)


# Generates a form where a new event can be registered
class EventRegisterForm(FlaskForm):
    # Programmatically generate selectable years, days etc..
    year_choices = [tuple((i, i)) for i in range(1900, 2021)]
    month_choices = [tuple((i, i)) for i in range(1, 13)]
    day_choices = [tuple((i, i)) for i in range(1, 32)]
    hour_choices = [tuple((i, i)) for i in range(0, 24)]
    minute_choices = [tuple((i, i)) for i in range(0, 60)]
    second_choices = [tuple((i, i)) for i in range(0, 60)]

    # Build the form fields
    time_year = SelectField("Year", choices=year_choices, validators=[DataRequired()])
    time_month = SelectField("Month", choices=month_choices, validators=[DataRequired()])
    time_day = SelectField("Day", choices=day_choices, validators=[DataRequired()])
    time_hour = SelectField("Hour", choices=hour_choices, validators=[DataRequired()])
    time_minute = SelectField("Minute", choices=minute_choices, validators=[DataRequired()])
    time_second = SelectField("Second", choices=second_choices, validators=[DataRequired()])

    # Build the remaining form fields
    how = StringField("How", validators=[DataRequired()])
    who = StringField("Who", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Generates a string that conforms the Postgres TIMESTAMP type
def build_timestamp(y, mo, d, h, mi, s):
    return str(y) + "-" + str(mo) + "-" + str(d) + " " + str(h) + ":" + str(mi) + ":" + str(s)


# Builds the page where new events can be added
@app.route('/add', methods=['GET', 'POST'])
def add_event():
    form = EventRegisterForm()
    if form.validate_on_submit():
        # Add event to database
        hero_db.connect()

        # Get all the time data
        year = request.form.get('time_year')
        month = request.form.get('time_month')
        day = request.form.get('time_day')
        hour = request.form.get('time_hour')
        minute = request.form.get('time_minute')
        second = request.form.get('time_second')
        the_when = build_timestamp(year, month, day, hour, minute, second)

        # Get the remaining event data
        the_how = form.how.data
        the_who = form.who.data

        # Create the database records
        hero_db.new_save(the_when, the_how, the_who)
        hero_db.close()
        return show_events()
    return render_template('formadd.html', title='Add Event', form=form)


# Generates a form where a person can be renamed or deleted
class PersonModifyForm(FlaskForm):
    people = SelectField("People", validators=[DataRequired()])
    new_name = StringField("New Name")
    delete = SubmitField("Delete")
    modify = SubmitField("Rename")


# Builds the page where people can be modified
@app.route('/people', methods=['GET', 'POST'])
def modify_people():
    form = PersonModifyForm()
    # Update the people that can be selected
    hero_db.connect()
    people = hero_db.get_all_people()
    hero_db.close()
    # Populate the list of people with their ids
    choices = [tuple((p[1], p[0])) for p in people]
    form.people.choices = choices

    # Get the ID of the selected person
    selected_person_id = request.form.get('people')
    if 'delete' in request.form:
        hero_db.connect()
        hero_db.remove_person_with_id(str(selected_person_id))
        hero_db.close()
        return show_events()
    if 'modify' in request.form:
        new_name = form.new_name.data
        hero_db.connect()
        if len(new_name) is 0:
            flash('Cannot rename someone to an empty string')
        else:
            hero_db.rename_person(str(selected_person_id), new_name)
            hero_db.close()
            return show_events()
    return render_template('formpeople.html', title='People', form=form)


if __name__ == '__main__':
    app.run()
