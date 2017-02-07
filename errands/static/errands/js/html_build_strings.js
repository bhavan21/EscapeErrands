var HTML_STRINGS = {
    TOUCH: {
        /**
         * @return {string}
         */
        PIECE: function (id, epoch_date, epoch_time, end_date, end_time, time_period, duration, tag, comment) {
            //defaults
            tag = tag === undefined ? "" : tag;
            comment = comment === undefined ? "" : comment;
            epoch_date = epoch_date === undefined ? "" : epoch_date;
            epoch_time = epoch_time === undefined ? "00:00" : epoch_time;
            end_date = end_date === undefined ? "" : end_date;
            end_time = end_time === undefined ? "" : end_time;
            var duration_days = duration === undefined ? 0 : duration.days;
            var duration_seconds = duration === undefined ? 0 : duration.seconds;
            var time_period_days = time_period === undefined ? 0 : time_period.days;
            var time_period_seconds = time_period === undefined ? 0 : time_period.seconds;

            var time_period_display = '',
                duration_display = '',
                time_period_switch = 'checked',
                duration_switch = 'checked';
            if (duration_days == 0 && duration_seconds == 0) {
                duration_display = 'display:none';
                duration_switch = '';
            }
            if (time_period_days == 0 && time_period_seconds == 0) {
                time_period_display = 'display:none';
                time_period_switch = '';
            }
            return '<tr id="' + id + '">' +
                '<td class="center-align remove-td">' +
                '<a class="remove-btn waves-effect waves-light btn-floating red z-depth-3">' +
                '<i class="material-icons">remove</i>' +
                '</a>' +
                '</td>' +
                '<td>' +
                '<div class="card waves-effect waves-yellow hoverable" style="width:100%">' +
                '<span style="position:absolute;bottom:0;right:0;margin:10px"><i class="material-icons activator">comment</i></span>' +
                '<div class="card-content row">' +
                '<div class="col l6 m6 s12 waves-effect waves-yellow  time-period-div">' +
                '<div class="card-title">Time Period</div>' +
                '<div class="row">' +
                '<div class="col l4 m4 s4 switch">' +
                '<label>' +
                'Once' +
                '<input class="option-select" type="checkbox" ' + time_period_switch + '>' +
                '<span class="lever"></span>' +
                'Repeat' +
                '</label>' +
                '</div>' +
                '<div class="col l8 m8 s8 time-period-select row" style="' + time_period_display + '">' +
                '<label class="col l6 m6 s6">' +
                'Days' +
                '<input class="days validate" type="number" value="' + time_period_days + '">' +
                '</label>' +
                '<label class="col l6 m6 s6">' +
                'Seconds' +
                '<input class="seconds validate" type="number" value="' + time_period_seconds + '">' +
                '</label>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '<div class="col l6 m6 s12 waves-effect waves-yellow duration-div">' +
                '<div class="card-title">Duration</div>' +
                '<div class="row">' +
                '<div class="col l4 m4 s4 switch">' +
                '<label>' +
                'Task' +
                '<input class="option-select" type="checkbox" ' + duration_switch + '>' +
                '<span class="lever"></span>' +
                'Event' +
                '</label>' +
                '</div>' +
                '<div class="col l8 m8 s8 duration-select" style="' + duration_display + '">' +
                '<label class="col l6 m6 s6">' +
                'Days' +
                '<input class="days validate" type="number" value="' + duration_days + '">' +
                '</label>' +
                '<label class="col l6 m6 s6">' +
                'Seconds' +
                '<input class="seconds validate" type="number" value="' + duration_seconds + '">' +
                '</label>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '<div class="card-content row">' +
                '<div class="col l8 m8 s12 waves-effect waves-yellow epoch-div">' +
                '<div class="card-title">Epoch</div>' +
                '<div class="row">' +
                '<label class="col l6 m6 s12 ">' +
                'Epoch Date' +
                '<input class="epoch-date" type="date" value="' + epoch_date + '">' +
                '</label>' +
                '<div class="col l1 m1 s1"></div>' +
                '<label class="col l6 m6 s12 ">' +
                'Epoch Time' +
                '<input class="epoch-time" type="time" value="' + epoch_time + '">' +
                '</label>' +
                '</div>' +
                '</div>' +
                '<div class="col l4 m4 s12 waves-effect waves-yellow tag-div">' +
                '<div class="card-title">About</div>' +
                '<label>' +
                'Tag' +
                '<input type="text" class="card-title tag validate" value="' + tag + '"/>' +
                '</label>' +
                '</div>' +
                '</div>' +
                '<div class="card-content row">' +
                '<div class="col l8 m8 s12 waves-effect waves-yellow end-div" style="' + time_period_display + '">' +
                '<div class="card-title">End</div>' +
                '<div class="row">' +
                '<label class="col l6 m6 s12 ">' +
                'End Date' +
                '<input class="end-date" type="date" value="' + end_date + '">' +
                '</label>' +
                '<label class="col l6 m6 s12 ">' +
                'End Time' +
                '<input class="end-time" type="time" value="' + end_time + '">' +
                '</label>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '<div class="card-reveal">' +
                '<span style="position:absolute;bottom:0;right:0;margin:10px" class="card-title">' +
                '<i class="material-icons waves-effect">close</i></span>' +
                '<div class="card-title">Comment</div>' +
                '<div class="input-field">' +
                '<textarea class="comment materialize-textarea">' + comment + '</textarea>' +
                '</div>' +
                '<div class="grey-text">' +
                '<span class="flow-text">Help</span>' +
                '<ul>' +
                '<li>An Event has duration, A Task does not<li>' +
                '<li>Both can repeat<li>' +
                '<li>For those which repeat, their first date is Epoch DateTime and they cannot appear after End DateTime<li>' +
                '<li>Using these thumb rules, construct your errand in an intuitional manner<li>' +
                '</ul>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</td>' +
                '</tr>'

        }
    },
    ALL: {
        /**
         * @return {string}
         */
        PIECE: function (id) {
            //defaults
            id = id === undefined ? "" : id;
            return '<tr id="' + id + '"><td>' + id + '</td></tr>'
        }
    }
};