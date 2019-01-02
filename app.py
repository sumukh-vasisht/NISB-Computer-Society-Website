from flask import Flask, request, render_template
app = Flask(__name__)

#CONFIGURING FIREBASE


import pyrebase

config = {
    "apiKey": "AIzaSyCNqP7QA-spg2B-WblSnbJ9kcVLntvSq_Q",
    "authDomain": "nisb-ieee.firebaseapp.com",
    "databaseURL": "https://nisb-ieee.firebaseio.com",
    "projectId": "nisb-ieee",
    "storageBucket": "nisb-ieee.appspot.com",
    "messagingSenderId": "496074877089",
    "serviceAccount": "creds.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()



@app.route("/")
def index():
    #SLIDER IMAGES
    slides = [
        "slide1.jpg",
        "slide2.jpg"
    ]
    #ACTIVITIES DATA
    activities = [
        {
            "heading":"FOCUS GROUPS",
            "imgUrl":"../static/images/activities/focusGroups.jpg",
            "text":"The people with common technical interest form groups to focus and learn on particular technology and develop real life application projects. We have been conducting various focus groups on Microcontrollers like AVR Atmega, Deep Learning, Web development & Python programming.",
            "direction":"left"
        },
        {
            "heading":"WIE WEEKLY MEETINGS",
            "imgUrl":"../static/images/activities/wieWeek.jpg",
            "text":"Women in Engineering affinity group under NISB conducts weekly meetups where women are mostly focused to learn a new technical concepts and to implement simple projects.",
            "direction":"right"
        },
        {
            "heading":"TECHNICAL BLOG",
            "imgUrl":"../static/images/activities/blog.png",
            "text":"NISB has its one technical blog site which provides platform for students to showcase their writing skills and to learn from it. We also have a youtube channel to which helps students to keep learning new things.",
            "direction":"left"
        },
        {
            "heading":"INDUSTRIAL VISITS",
            "imgUrl":"../static/images/activities/cisco.jpg",
            "text":"As a part of technical tour to make students get an exposure about working of things in Industries every semester we conduct Industrial visits. Our recent visits include ISRO space centre, IISC Banglore, NOKIA, Cisco, Infosys.",
            "direction":"right"
        },
        {
            "heading":"SOCIAL INITIATIVES",
            "imgUrl":"../static/images/activities/wieSI.jpg",
            "text":"Every year we visit Old age ashram's, Divya Deepa with a theme and to make children and aged people familiar with basic use of technology and its benefits for individuals.",
            "direction":"left"
        }
    ]
    return render_template("index.html", slides=slides , activities = activities)


#ADMIN PANEL (PASSWORD PROTECT LATER)
@app.route("/Admin")
def admin():

    #GETTING EVENTS
    events = db.child("events").get()
    upcomingEventsList = []
    pastEventsList = []
    
    for event in events.each():
        eventObj = {
            "title": event.val()["title"],
            "date": event.val()["date"],
            "id":event.key()
        }
        if(event.val()["type"]=="upcoming"):
            upcomingEventsList.append(eventObj)
        else:
            pastEventsList.append(eventObj)

    upcomingEventsList.reverse()
    pastEventsList.reverse()
    return render_template("admin.html", upcomingEventsList=upcomingEventsList , pastEventsList=pastEventsList, uploadedMessage = "")

@app.route("/Admin/<eventId>/Delete")
def deleteEvent(eventId):

    #DELETING SELECTED EVENT
    imgName = db.child("events/"+eventId).get().val()["imgName"]
    storage.delete("events/"+imgName)
    db.child("events/"+eventId).remove()
    return render_template("showMessage.html", message = "Deleted")

@app.route("/Admin/<eventId>/changeType")
def changeToPast(eventId):

    if(db.child("events/"+eventId+"/type").get().val()=="upcoming"):
        db.child("events/"+eventId+"/type").set("past")
        message = "Event Set to Past"
    else: 
        db.child("events/"+eventId+"/type").set("upcoming")
        message = "Event Set to Upcoming"
    return render_template("showMessage.html", message = message)




@app.route('/Admin', methods=['POST'])
def event_form_post():

    #UPLOADING IMAGE
    coverImage = request.files["coverImage"]
    storage.child("events/"+coverImage.filename).put(coverImage)
    
    #SAVING DATA
    db.child("events/").push({
        "title": request.form['title'],
        "organisedBy": request.form['organisedBy'],
        "date": request.form['date'],
        "time": request.form['time'],
        "venue": request.form['venue'],
        "imgName":coverImage.filename,
        "imgURL": storage.child("events/"+coverImage.filename).get_url(token="none"),
        "type":"upcoming"
    })

    return render_template("showMessage.html" , message = "Event Uploaded")



@app.route("/About")
def about():

    members = db.child("members").get().val()
    for member in members:
        url = member["imgURL"]
        member["imgURL"] = storage.child(url).get_url(token="none")

    aboutRow = [
        {
            "imgURL":"../static/images/about/logo.png",
            "heading":"NIE IEEE Student Branch",
            "text":"NISB is the IEEE student branch of National Institute of Engineering. It is one of the largest and most active student branches of Karnataka.Having been active for a decade, we have been honoured and humbled with numerous awards and accolades over time, including 'The Best Student Chapter' of Region 10­ Bangalore. We organize and host a wide range of technical workshops and events. We have our odd sem fest ADROIT and even sem fest ANKURA. Electronika , IPL are few our signature events."
        },
        {
            "imgURL":"../static/images/about/IEEE.gif",
            "heading":"Institute of Electrical and Electronics Engineers",
            "text":"The Institute of Electrical and Electronics Engineers is a professional association.It was formed in 1963 from the amalgamation of the American Institute of Electrical Engineers and the Institute of Radio Engineers. Today, it is the world's largest association of technical professionals with more than 400,000 members in chapters around the world. Its objectives are the educational and technical advancement of electrical and electronic engineering, telecommunications, computer engineering and allied disciplines. The core purpose of IEEE is to foster technological innovation and excellence for the benefit of humanity.The Institute of Electrical and Electronics Engineers sponsors more than 1,600 annual conferences and meetings worldwide. IEEE is also highly involved in the technical program development of numerous events including trade events, training workshops, job fairs, and other programs."
        },
        {
            "imgURL":"../static/images/about/r10.jpg",
            "heading":"Region 10",
            "text":"The IEEE Region 10, also sometimes referred as the Asia Pacific Region, comprises of 57 Sections, 6 Councils, 17 Sub­sections, 515 Chapters, 60 Affinity Groups and 958 Student Branches. It covers a geographical area stretching from South Korea and Japan in the north­east to New Zealand in the south, and Pakistan in the west. With a membership of 107,154, it is one of the largest regions in IEEE. In order to fulfill IEEE’s mission of advancing the theory and practice of electrical, electronics, communications and computer engineering, as well as computer science and related areas, Region 10 activities are directed to developing and maintaining regional entities for the best interests and benefits of the IEEE members in the region. TENCON is a premier international technical conference of IEEE Region 10."
        },
        {
            "imgURL":"../static/images/about/blr-min.png",
            "heading":"IEEE Bangalore Section",
            "text":"IEEE Banglaore section is one of the most prestigious sections in India known for conducting a wide range of events and workshops. IEEE Bangalore Section is recognised as an Outstanding Section for Membership Recruitment and Retention Performance – 2016. It has 14 Society Chapters and two affinity groups.The Chapters carry out focused activities in the respective area by way of conducting technical talks under DLT, Seminars, Tutorials, workshops etc. Apart from the Chapters two affinity groups viz. the Graduate of the Last Decade (GOLD) and Women In Engineering (WIE) also carry out related activities. IEEE Bangalore and IEEE Princeton and Central New Jersey Sections had signed a MoU as sister sections.There are about 53 Student Branches in Karnataka in the various graduate and post­graduate engineering colleges and these units conduct technical talks, TechFests etc. A dedicated Student Paper contest, Technical Colloquium and Student Leadership Workshop are some of the major events conducted under Student activities of the Section."
        }
    ]
    return render_template("about.html", members=members, aboutRow=aboutRow)

@app.route("/Events")
def events():
    events = db.child("events/").get()
    pastEventsList = []
    upcomingEventsList = []
    for event in events.each():
        eventObj = {
            "title": event.val()["title"],
            "organisedBy": event.val()["organisedBy"],
            "date": event.val()["date"],
            "time": event.val()["time"],
            "venue": event.val()["venue"],
            "imgURL": event.val()["imgURL"]
        }
        if(event.val()["type"]=="upcoming"):
            upcomingEventsList.append(eventObj)
        else:
            pastEventsList.append(eventObj)

    pastEventsList.reverse()
    upcomingEventsList.reverse()
    return render_template("events.html" , pastEventsList=pastEventsList, upcomingEventsList=upcomingEventsList)

if __name__=="__main__":
    app.run(debug=True)