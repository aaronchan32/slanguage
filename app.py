
from flask import Flask, render_template, request, send_file
from analyzeSlang import *

app = Flask(__name__)

analyzedData = None
template = None
socialMediaRender = None


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/facebook", methods = ["GET", "POST"])  # http://127.0.0.1:5000/
def facebook():
    return socialMedia("socialPlatform.html", "facebook")


@app.route('/getCSV')
def getCSV():
    if analyzedData.userExist:
        return send_file('messages.csv', mimetype='text/csv', download_name="messages.csv", as_attachment=True)
         


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

    if request.method == "GET" and ('fname' in request.args):  
        # try:
            print("Request.args:", request.args)
            senderName = request.args['fname']
            print("Sender Name:", senderName)
            analyzedData.createCSV(senderName)
            
            return render_template(nameHTML, template = analyzedData.getTemplateSetup(), socialPlatform = socialPlatform, showDownload = True)

        # except NameError:
        #     return render_template(nameHTML, template = None)

    elif request.method == "POST" and (not ('fname' in request.args)):
        #try:
            if socialPlatform == "instagram" or socialPlatform == "facebook":
                analyzedData = AnalyzeSlang("facebook")
                socialMediaRender = render_template(nameHTML, template = analyzedData.getTemplateSetup(), socialPlatform = socialPlatform, showDownload = True)
                return socialMediaRender

            if socialPlatform == "discord":
                analyzedData = AnalyzeSlang("discord")
                socialMediaRender = render_template(nameHTML, template = analyzedData.getTemplateSetup(), socialPlatform = socialPlatform, showDownload = True)
                return socialMediaRender

        #except:
            #return render_template(nameHTML, template = None)

    return render_template(nameHTML, template = None, socialPlatform = socialPlatform, showDownload = False)


if __name__ == "__main__":
    app.run(debug = True)