function element(tags, attributes, contents, closings) {
    var $element = "";// returning string
    var iter;
    for (iter = 0; iter < tags.length; ++iter) {

        $element += "<" + tags[iter];

        for (var key in attributes[iter]) {
            if (attributes[iter].hasOwnProperty(key)) {
                //# adding an attribute to the tags[i]#
                $element += ( " " + key + "=\'" + attributes[iter][key] + "\'");
            }
        }

        $element += ">";
        $element += contents[iter];
    }

    for (iter = tags.length - 1; iter > -1; --iter) {
        if (closings[iter]) {
            $element += "</" + tags[iter] + ">"
        }
    }

    return $element;
}

function cast_to_days_hours(days_seconds) {
    var days, seconds, hours;
    seconds = parseInt(days_seconds.seconds % 86400);
    hours = parseInt(seconds / 3600);
    days = parseInt(days_seconds.days + days_seconds.seconds / 86400);
    return {
        hours : hours,
        days   : days
    }
}

function cast_to_hours_minutes(days_seconds) {
    var hours, minutes, seconds;
    seconds = parseInt(days_seconds.seconds % 3600);
    hours = parseInt(days_seconds.days * 24 + days_seconds.seconds / 3600);
    minutes = parseInt(seconds / 60);
    return {
        hours : hours,
        minutes   : minutes
    }
}