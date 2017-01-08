var HTML_STRINGS = {

    /**
     * @return {string}
     */
    PIECE: function (id, epoch_date, epoch_time, time_period, duration, tag, comment) {

        //defaults
        tag = tag === undefined ? "" : tag;
        comment = comment === undefined ? "" : comment;
        epoch_date = epoch_date === undefined ? "" : epoch_date;
        epoch_time = epoch_time === undefined ? "00:00" : epoch_time;
        var duration_days = duration === undefined ? 0 : duration.days;
        var duration_seconds = duration === undefined ? 0 : duration.seconds;
        var time_period_days = time_period === undefined ? 0 : time_period.days;
        var time_period_seconds = time_period === undefined ? 0 : time_period.seconds;

        var time_period_display = '',
            duration_display = '',
            time_period_switch = 'checked',
            duration_switch = 'checked';
        if (duration_days == 0 && duration_seconds == 0){
            duration_display = 'display:none';
            duration_switch = '';
        }
        if (time_period_days == 0 && time_period_seconds == 0){
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
            '<span><i class="small material-icons activator right waves-effect">comment</i></span>' +
            '<div class="card-content row">' +
            '<div class="col l6 m6 s6 waves-effect waves-yellow  time-period-div">' +
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
            '<div class="col l6 m6 s6 waves-effect waves-yellow duration-div">' +
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
            '<div class="col l8 m8 s8 waves-effect waves-yellow epoch-div">' +
            '<div class="card-title">Epoch</div>' +
            '<div class="row">' +
            '<label class="col l6 m6 s6 ">' +
            'Epoch Date' +
            '<input class="epoch-date" type="date" value="' + epoch_date + '">' +
            '</label>' +
            '<div class="col l1 m1 s1"></div>' +
            '<label class="col l6 m6 s6 ">' +
            'Epoch Time' +
            '<input class="epoch-time" type="time" value="' + epoch_time + '">' +
            '</label>' +
            '</div>' +
            '</div>' +
            '<div class="col l3 m3 s3 waves-effect waves-yellow tag-div">' +
            '<div class="card-title">About</div>' +
            '<label>' +
            'Tag' +
            '<input type="text" class="card-title tag validate" value="' + tag + '"/>' +
            '</label>' +
            '</div>' +
            '</div>' +
            '<div class="card-reveal">' +
            '<span class="card-title grey-text text-darken-4">' +
            '<i class="material-icons right waves-effect">close</i></span>' +
            '<div class="card-title">Comment</div>' +
            '<div class="input-field">' +
            '<textarea class="comment materialize-textarea">' + comment + '</textarea>' +
            '</div>' +
            'Help' +
            '<ul>' +
            '<li>An Event has Duration, A Task Do Not<li>' +
            '<li>Both can repeat<li>' +
            '<li>For those which repeat, Epoch Date is it\'s First Date<li>' +
            '</ul>' +
            '</div>' +
            '</div>' +
            '</td>' +
            '</tr>'
    }
};
