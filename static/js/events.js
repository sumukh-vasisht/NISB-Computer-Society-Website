var pastEventsDiv = document.querySelector("#past");
var upEventsDiv = document.querySelector("#upcoming");
var todayEventsDiv = document.querySelector("#todayEvents");

db.ref("events").orderByChild("timeStamp").on("value", function(snapshot) {
    this.data = [];

    snapshot.forEach(function(child) {
        this.data.push(child.val());
    }.bind(this));

    var now = new Date();
    var todayDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    var todayEvents = "";
    var pastEvents = "";
    var upEvents = "";
    Object.keys(this.data).forEach(function(k){
        if (this.data[k]["name"] !== "dummy" && this.data[k]["organiser"] === "Computer Society") {
            var date = this.data[k]["date"].split("-");
            var eventDate = new Date(date[2], date[1]-1, date[0]);

            if ((todayDate - eventDate) === 0) {
                var event = `
                <div class="eventCard">
                    <div class="eventImg" style="background-image: url(` +  this.data[k]["imgUrl"]+ `)"></div>
                    <div class="eventDesp">
                        <p class="eventTitle">`  + this.data[k]["name"]  + ` </p>
                        <p class="eventOrganiserWrap">Organised by: <b class="eventOrganiser">` + this.data[k]["organiser"] + `</b></p>
                        <p class="eventVenue">Venue: <b>` +this.data[k]["venue"]  +  `</b></p>
                        <p class="eventTime">Date: <b>` + this.data[k]["date"] + `</b> &nbsp&nbsp Time: <b> ` + this.data[k]["time"] +  `</b></p>
                    </div>
                    <button class="regBtn"><a target="_blank" href="` + this.data[k]["regUrl"] + `">` + this.data[k]["btnValue"] + `</a></button>
                </div>
                    `;
                todayEvents = event + todayEvents;
            } else if ((todayDate - eventDate) < 0) {
                var event = `
                <div class="eventCard">
                    <div class="eventImg" style="background-image: url(` +  this.data[k]["imgUrl"]+ `)"></div>
                    <div class="eventDesp">
                        <p class="eventTitle">`  + this.data[k]["name"] + ` </p>
                        <p class="eventOrganiserWrap">Organised by: <b class="eventOrganiser">` + this.data[k]["organiser"] + `</b></p>
                        <p class="eventVenue">Venue: <b>` +this.data[k]["venue"]  +  `</b></p>
                        <p class="eventTime">Date: <b>` + this.data[k]["date"] + `</b> &nbsp&nbsp Time: <b> ` + this.data[k]["time"] +  `</b></p>
                    </div>
                    <button class="regBtn"><a target="_blank" href="` + this.data[k]["regUrl"] + `">` + this.data[k]["btnValue"] + `</a></button>
                </div>
                    `;
                upEvents += event;
            } else if ((todayDate - eventDate) > 0) {
                            var event = `
                <div class="eventCard" style="height: 21rem;">
                    <div class="eventImg" style="background-image: url(` +  this.data[k]["imgUrl"]+ `)"></div>
                    <div class="eventDesp">
                        <p class="eventTitle">`  + this.data[k]["name"] + ` </p>
                        <p class="eventOrganiserWrap">Organised by: <b class="eventOrganiser">` + this.data[k]["organiser"] + `</b></p>
                        <p class="eventVenue">Venue: <b>` +this.data[k]["venue"]  +  `</b></p>
                        <p class="eventTime">Date: <b>` + this.data[k]["date"] + `</b> &nbsp&nbsp Time: <b> ` + this.data[k]["time"] +  `</b></p>
                    </div>
                </div>
                    `;
                pastEvents = event + pastEvents;
            }
        }
    });
    todayEventsDiv.innerHTML = todayEvents;
    upEventsDiv.innerHTML = upEvents;
    pastEventsDiv.innerHTML = pastEvents;

    if (todayEvents === "") {
        todayEventsDiv.parentNode.style.display = "none";
    } else {
        todayEventsDiv.parentNode.style.display = "block";
        document.querySelector("#todayLoad").style.display = "none";
    }
    if (upEvents === "") {
        document.querySelector("#upLoad").style.display = "block";
        document.querySelector("#upLoad").innerHTML = "Brainstorming now, we will update soon.";
    } else {
        document.querySelector("#upLoad").style.display = "none";
    }
    if (pastEvents === "") {
        document.querySelector("#pastLoad").style.display = "block";
        document.querySelector("#pastLoad").innerHTML = "Error fetching information.";
    } else {
        document.querySelector("#pastLoad").style.display = "none";
    }
});