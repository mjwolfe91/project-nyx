from flask import Flask, render_template, send_from_directory, request, redirect, flash
import secrets
import pickle
import pandas as pd
import sqlalchemy as sa
from time import sleep

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

# Note the server address here. Just mysql! It's the service name in our compose file.
con = sa.create_engine("mysql://root@projectnyx1234@172.116.176.142:3306", echo=True)

sleep(15)
con.connect()

# Make the schema if it doesn't exist
schemas = sa.inspect(con).get_schema_names()
print(schemas)
if 'user' not in schemas:
    con.execute(sa.schema.CreateSchema('user'))


with open("./recommendations.pkl", "rb") as f:
    clf = pickle.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    index = "index.html"
    #todo get inputs from Stroud
    pred = "Enter your TBD inputs below."
    if request.method == "GET":
        return render_template(index, pred=pred)
    else:
        print(list(request.form.keys()))
        try:
            # Get the things from the form, make them floats (they start as strings)
            colnames = ["userId", "rec_exp.movieId", "rec_exp.rating"]
            responses = [request.form.get(item) for item in colnames]
            inputs = [[float(item) for item in responses]]

            # Write the submission to SQL!
            pd.DataFrame(columns=colnames, data=inputs).to_sql('submissions', con, schema='user', if_exists='append', index=False)
            #todo update once inputs are ready
            pred = f"We think your flower is a {clf.predict(inputs)[0]}!"
        except Exception as e:
            print(e)
            flash("Invalid inputs! Try again.", "warn")
            redirect(index)

    return render_template(index, pred=pred)


@app.route("/js/<path:path>")
def send_js(path):
    return send_from_directory("static/js", path)


@app.route("/css/<path:path>")
def send_css(path):
    return send_from_directory("static/css", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
