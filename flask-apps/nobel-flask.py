#!/usr/bin/env python

from flask import Flask, json, render_template, request, send_file
import os

#create instance of Flask app
app = Flask(__name__)

#decorator
@app.route("/")
def nobel_index():

    return render_template('nobel_index.html')

@app.route("/all")
def all_data():
    json_url = os.path.join(app.static_folder,"","nobel.json")
    data_json = json.load(open(json_url))

    return render_template('index.html',data=data_json)

@app.route("/add")
def form():
    form_url = os.path.join("templates","form.html")
    return send_file(form_url)

@app.route("/<year>", methods=['GET', 'POST'])
def year(year):
    json_url = os.path.join(app.static_folder,"","nobel.json")
    data_json = json.load(open(json_url))

    if request.method == 'GET':
        data = data_json['prizes']
        year = request.view_args['year']
        output_data = [x for x in data if x['year']==year]
        return render_template('year.html',html_page_text=output_data)    

    elif request.method == 'POST':
        year = request.form['year']
        category = request.form['category']
        id = request.form['id']
        fname = request.form['fname']
        sname = request.form['sname']
        m_text = request.form['m_text']
        share_no = request.form['share_no']
        prize_yr= {"year":year,
                    "category":category,
                    "laureates":
                        [{"id":id,
                        "firstname":fname,
                        "surname":sname,
                        "motivation":m_text,
                        "share":share_no
                        }]
                    }
        
        with open(json_url,"r+") as file:
            data_json = json.load(file)
            data_json["prizes"].append(prize_yr)
            json.dump(data_json, file, indent=1)
        
        #Adding text
        text_success = "Data successfully added: " + str(prize_yr)
        return render_template('index.html', html_page_text=text_success)


if __name__ == "__main__":
    app.run(debug=True)


