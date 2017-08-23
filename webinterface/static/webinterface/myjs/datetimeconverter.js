/**
 * Order of shortForms and longForms must be same
 * Dependencies :
 *      moment.js
 * */
var DatetimeConverter = {
    shortForms: ['d', 'm', 'y', 'h', 't', 's', 'u'],
    longForms: ['day', 'month', 'year', 'hour', 'minute', 'second', 'microsecond'],
    getShortForm: function (longForm) {
        var index = this.longForms.indexOf(longForm);
        return this.shortForms[index];
    },
    getLongForm: function (shortForm) {
        var index = this.shortForms.indexOf(shortForm);
        return this.longForms[index];
    },
    parse: function (datetimeStr) {
        try {
            if (datetimeStr === '') {
                return null;
            }
            var ans = {microsecond: 0, second: 0, minute: 0, hour: 0, day: 0, month: 0, year: 0};
            var spilt = datetimeStr.split(' ');
            for (var i = 0; i < spilt.length; ++i) {
                var unit = spilt[i];
                ans[this.getLongForm(unit.charAt(0))] = Number(unit.substr(1));
            }
            return ans;
        } catch (e) {
            return false;
        }
    },
    format: function (datetimeObj) {
        if (datetimeObj === null) {
            return '';
        }
        var ans = '';
        for (var i = 0; i < this.longForms.length; ++i) {
            ans += this.shortForms[i] + datetimeObj[this.longForms[i]] + ' ';
        }
        return ans;
    },
    formatNow: function () {
        var now = moment();
        return this.getShortForm('day') + now.date() + ' '
            + this.getShortForm('month') + (now.month() + 1) + ' '
            + this.getShortForm('year') + now.year() + ' '
            + this.getShortForm('hour') + now.hour() + ' '
            + this.getShortForm('minute') + now.minute() + ' '
            + this.getShortForm('second') + now.second() + ' '
            + this.getShortForm('microsecond') + (now.millisecond() * 1000)
    }
};