from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from the_hero.hero import HeroDatabase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'filesystem'


@app.route('/')
def show_events():
    # Display existing Database content
    hero_db = HeroDatabase()
    hero_db.connect()
    all_results = hero_db.inspect()
    hero_db.close()
    return render_template('existingevents.html', title='Existing Events', rows=all_results)


class EventRegisterForm(FlaskForm):
    time = StringField("Time", validators=[DataRequired()])
    how = StringField("How", validators=[DataRequired()])
    who = StringField("Who", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/add', methods=['GET', 'POST'])
def add_event():
    form = EventRegisterForm()
    if form.validate_on_submit():
        # add to database
        hero_db = HeroDatabase()
        hero_db.connect()
        the_time = form.time.data
        the_how = form.how.data
        the_who = form.who.data
        hero_db.new_save(the_time, the_how, the_who)
        hero_db.close()
        return show_events()
    return render_template('formadd.html', title='Add Event', form=form)


if __name__ == '__main__':
    app.run()
