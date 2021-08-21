
from flask import Flask, render_template, request, send_file, flash
from analyzeSlang import *
import time

app = Flask(__name__)

analyzedData = None
template = None
socialMediaRender = None
error = None
currentSocialPlatform = None


@app.route("/")
def home():
    return render_template("home.html")

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
    global currentSocialPlatform
    

    if request.method == "POST" and (request.form.get('fname')):  #When form is submitted (When user press Download button)            
            senderName = request.form.get('fname')
            analyzedData.createCSV(senderName)
            return send_file('messages.csv', mimetype='text/csv', download_name="messages.csv", as_attachment=True)

    elif request.method == "POST":
        # try:
        if socialPlatform == "facebook":
            currentSocialPlatform = "facebook"
            analyzedData = AnalyzeSlang(currentSocialPlatform)
            names = analyzedData.getParticipantNames()
            socialMediaRender = render_template(nameHTML, template = analyzedData.getTemplateSetup(), socialPlatform = socialPlatform, showDownload = True, error = error, names=names)
            return socialMediaRender
        
        if socialPlatform == "instagram":
            currentSocialPlatform = "instagram"
            analyzedData = AnalyzeSlang(currentSocialPlatform)
            names = analyzedData.getParticipantNames()
            socialMediaRender = render_template(nameHTML, template = analyzedData.getTemplateSetup(), socialPlatform = socialPlatform, showDownload = True, error = error, names=names)
            return socialMediaRender

        if socialPlatform == "discord":
            currentSocialPlatform = "discord"
            analyzedData = AnalyzeSlang(currentSocialPlatform)
            names = analyzedData.getParticipantNames()
            socialMediaRender = render_template(nameHTML, template = analyzedData.getTemplateSetup(), socialPlatform = socialPlatform, showDownload = True, error = error, names=names)
            return socialMediaRender

        # except:
        #     return render_template(nameHTML, template = None, socialPlatform = socialPlatform, error=True)

    elif socialMediaRender and currentSocialPlatform == socialPlatform:
        return socialMediaRender

    return render_template(nameHTML, template = None, socialPlatform = socialPlatform)


if __name__ == "__main__":
    app.run(debug=True)