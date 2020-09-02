from flask import Flask

from the_hero.hero import HeroDatabase

app = Flask(__name__)


@app.route('/')
def show_events():
    # Display existing Database content
    html = "<h1>Existing Feats</h1>"
    html += "<table> <tr> <th>When I saved the world</th><th>How I saved the world</th><th>Who I thank for being so awesome</th></tr>"
    heroDB = HeroDatabase()
    heroDB.connect()
    all_results = heroDB.inspect()
    for i in all_results:
        html += "<tr>"
        html += "<td>" + str(i[1]) + "</td>"
        html += "<td>" + i[2] + "</td>"
        html += "<td>" + i[3] + "</td>"  # TODO: This needs to be parsed as a list
        html += "</tr>"
        html += str("\n")
    heroDB.close()
    return html


@app.route('add')
def add_event():
    x = 1


if __name__ == '__main__':
    app.run()
