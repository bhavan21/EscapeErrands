var HTML_STRINGS = {

    /**
     * @return {string}
     */
    PIECE: function (id) {
        return '<tr id="'+ id +'">' +
        '<td class="center-align remove-td">' +
        '<a class="remove-btn waves-effect waves-light btn-floating red z-depth-3">' +
        '<i class="material-icons">remove</i>' +
        '</a>' +
        '</td>' +
        '<td>' +
        '<div class="card waves-effect waves-yellow hoverable" style="width:100%">' +
        '<span><i class="small material-icons activator right waves-effect">comment</i></span>' +
        '<div class="card-content row">' +
        '<div class="col l6 waves-effect waves-yellow  time-period-div">' +
        '<div class="card-title">Time Period</div>' +
        '<div class="row">' +
        '<div class="col l4 switch">' +
        '<label>' +
        'Once' +
        '<input class="option-select" type="checkbox">' +
        '<span class="lever"></span>' +
        'Repeat' +
        '</label>' +
        '</div>' +
        '<div class="time-period-select" style="display:none">' +
        '<label class="col l4">' +
        'Days' +
        '<input class="days validate" type="number" value="0">' +
        '</label>' +
        '<label class="col l4">' +
        'Seconds' +
        '<input class="seconds validate" type="number" value="0">' +
        '</label>' +
        '</div>' +
        '</div>' +
        '</div>' +
        '<div class="col l6 waves-effect waves-yellow duration-div">' +
        '<div class="card-title">Duration</div>' +
        '<div class="row">' +
        '<div class="col l4 switch">' +
        '<label>' +
        'Task' +
        '<input class="option-select" type="checkbox">' +
        '<span class="lever"></span>' +
        'Event' +
        '</label>' +
        '</div>' +
        '<div class="duration-select" style="display:none">' +
        '<label class="col l4">' +
        'Days' +
        '<input class="days validate" type="number" value="0">' +
        '</label>' +
        '<label class="col l4">' +
        'Seconds' +
        '<input class="seconds validate" type="number" value="0">' +
        '</label>' +
        '</div>' +
        '</div>' +
        '</div>' +
        '</div>' +
        '<div class="card-content row">' +
        '<div class="col l8 waves-effect waves-yellow epoch-div">' +
        '<div class="card-title">Epoch</div>' +
        '<div class="row">' +
        '<label class="col l6">' +
        'Epoch Date' +
        '<input class="epoch-date" type="date">' +
        '</label>' +
        '<div class="col l1"></div>' +
        '<label class="col l6">' +
        'Epoch Time' +
        '<input class="epoch-time" type="time">' +
        '</label>' +
        '</div>' +
        '</div>' +
        '<div class="col l3 waves-effect waves-yellow tag-div">' +
        '<div class="card-title">Misc</div>' +
        '<label>' +
        'Tag' +
        '<input type="text" class="card-title tag validate"/>' +
        '</label>' +
        '</div>' +
        '</div>' +
        '<div class="card-reveal">' +
        '<span class="card-title grey-text text-darken-4">' +
        '<i class="material-icons right waves-effect">close</i></span>' +
        '<div class="card-title">Misc</div>' +
        '<div class="input-field">' +
        '<textarea placeholder="Comment" class="comment materialize-textarea"></textarea>' +
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
