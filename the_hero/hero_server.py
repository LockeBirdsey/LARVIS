from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

# This can be seen from Docker
from hero import HeroDatabase

# This can be seen from Pycharm
# from the_hero.hero import HeroDatabase

# Web server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'filesystem'


@app.route('/')
def show_events():
    hero_db = HeroDatabase()
    hero_db.connect()
    all_results = hero_db.inspect_all()
    people = hero_db.get_all_people_from_people()
    hero_db.close()
    return render_template('existingevents.html', title='Existing Events', rows=all_results, people=people)


class EventRegisterForm(FlaskForm):
    # Programmatically generate selectable years, days etc..
    year_choices = []
    for i in range(1900, 2021):
        print(i)
        year_choices.append(tuple((i, i)))
    month_choices = []
    for i in range(1, 13):
        print(i)
        month_choices.append(tuple((i, i)))
    day_choices = []
    for i in range(1, 32):
        print(i)
        day_choices.append(tuple((i, i)))
    hour_choices = []
    for i in range(1, 25):
        print(i)
        hour_choices.append(tuple((i, i)))
    minute_choices = []
    for i in range(0, 60):
        print(i)
        minute_choices.append(tuple((i, i)))
    second_choices = []
    for i in range(0, 60):
        print(i)
        second_choices.append(tuple((i, i)))
    time_year = SelectField("Year", choices=year_choices, validators=[DataRequired()])
    time_month = SelectField("Month", choices=month_choices, validators=[DataRequired()])
    time_day = SelectField("Day", choices=day_choices, validators=[DataRequired()])
    time_hour = SelectField("Hour", choices=hour_choices, validators=[DataRequired()])
    time_minute = SelectField("Minute", choices=minute_choices, validators=[DataRequired()])
    time_second = SelectField("Second", choices=second_choices, validators=[DataRequired()])

    # Old time input method
    # time = StringField("Time", validators=[DataRequired()])
    how = StringField("How", validators=[DataRequired()])
    who = StringField("Who", validators=[DataRequired()])
    submit = SubmitField("Submit")


def build_timestamp(y, mo, d, h, mi, s):
    return str(y) + "-" + str(mo) + "-" + str(d) + " " + str(h) + ":" + str(mi) + ":" + str(s)


@app.route('/add', methods=['GET', 'POST'])
def add_event():
    form = EventRegisterForm()
    if form.validate_on_submit():
        # add event to database
        hero_db = HeroDatabase()
        hero_db.connect()

        # get all the time data
        year = request.form.get('time_year')
        month = request.form.get('time_month')
        day = request.form.get('time_day')
        hour = request.form.get('time_hour')
        minute = request.form.get('time_minute')
        second = request.form.get('time_second')
        the_when = build_timestamp(year, month, day, hour, minute, second)
        # get the remaining event data
        the_how = form.how.data
        the_who = form.who.data
        # create the database records
        hero_db.new_save(the_when, the_how, the_who)
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
