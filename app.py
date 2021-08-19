
from flask import Flask, render_template, request, send_file
from analyzeSlang import *
import time

app = Flask(__name__)

analyzedData = None
template = None
socialMediaRender = None
error = None


@app.route("/")
def home():
    return render_template("home.html")

# @app.route('/getCSV')
# def getCSV():
#     time.sleep(3)
#     global error
#     if analyzedData.getUserExists():
#         analyzedData.falseUserExists()
#         return send_file('messages.csv', mimetype='text/csv', download_name="messages.csv", as_attachment=True)
#     print("error")
#     error = "inputerror"
#     return socialMediaRender


@app.route("/facebook", methods = ["GET", "POST"])  # http://127.0.0.1:5000/
def facebook():
    return socialMedia("socialPlatform.html", "facebook")


@app.route("/discord", methods=["GET", "POST"])
def discord():
    return socialMedia("socialPlatform.html", "discord")

@app.route("/reddit")
def reddit():
    return render_template('socialPlatform.html', False)


@app.route("/instagram", methods = ["GET", "POST"])
def instagram():
    return socialMedia("socialPlatform.html", "instagram")


def socialMedia(nameHTML, socialPlatform):
    global analyzedData
    global template
    global socialMediaRender
    global names

    if request.method == "POST" and (request.form.get('fname')):  #When form is submitted (When user press Download button)
        # try:              
            senderName = request.form.get('fname')
            analyzedData.createCSV(senderName)
            return send_file('messages.csv', mimetype='text/csv', download_name="messages.csv", as_attachment=True)

        # except NameError:
        #     return render_template(nameHTML, template = None)

    elif request.method == "POST":
        #try:
            if socialPlatform == "instagram" or socialPlatform == "facebook":
                print("request form", request.form)
                analyzedData = AnalyzeSlang("facebook")
                names = analyzedData.getParticipantNames()
                print("does user exist", analyzedData.getUserExists())
                socialMediaRender = render_template(nameHTML, template = analyzedData.getTemplateSetup(), socialPlatform = socialPlatform, showDownload = True, error = error, names=names)
                return socialMediaRender

            if socialPlatform == "discord":
                analyzedData = AnalyzeSlang("discord")
                names = analyzedData.getParticipantNames()
                socialMediaRender = render_template(nameHTML, template = analyzedData.getTemplateSetup(), socialPlatform = socialPlatform, showDownload = True, error = error, names=names)
                return socialMediaRender

        #except:
            #return render_template(nameHTML, template = None)

    return render_template(nameHTML, template = None, socialPlatform = socialPlatform, showDownload = False)


if __name__ == "__main__":
    app.run(debug = True)