package org.yashasvi.calender4j.core.classes;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NonNull;
import lombok.ToString;
import org.yashasvi.calender4j.core.exceptions.InvalidDateException;
import org.yashasvi.calender4j.core.exceptions.InvalidTimeException;

import java.util.Calendar;

@Getter
@ToString
@EqualsAndHashCode
public class DateTime {
    private Date date;
    private Time time;

    public static DateTime now() {
        Calendar currentTime = Calendar.getInstance();
        DateTime dateTime = new DateTime();
        dateTime.date = Date.now();
        dateTime.time = Time.now();
        return dateTime;
    }

    public static DateTime of(final int year,
                              final int month,
                              final int day,
                              final int hour,
                              final int minute,
                              final int second,
                              final int microsecond) throws InvalidDateException, InvalidTimeException {
        DateTime dateTime = new DateTime();
        dateTime.date = Date.of(year, month, day);
        dateTime.time = Time.of(hour, minute, second, microsecond);
        return dateTime;
    }

    public DateTime(@NonNull final DateTime b) {
        this(b.date, b.time);
    }

    public DateTime(@NonNull final Date date, @NonNull final Time time) {
        this.date = new Date(date);
        this.time = new Time(time);
    }

    public DateTime(@NonNull final Date date) {
        this.date = new Date(date);
        this.time = Time.now();
    }

    public DateTime(@NonNull final Time time) {
        this.date = Date.now();
        this.time = new Time(time);
    }

    public boolean isGreaterThan(DateTime B) {
        if (this.date.isGreaterThan(B.date))
            return true;
        else if (this.date.isEqualTo(B.date))
            return this.time.isGreaterThan(B.time);
        return false;
    }

    public boolean isEqualTo(DateTime B) {
        return this.date.isEqualTo(B.date) && this.time.isEqualTo(B.time);
    }

    public boolean isLessThan(DateTime B) {
        return B.isGreaterThan(this);
    }

    public boolean isGreaterThanOrEqualTo(DateTime B) {
        return this.isGreaterThan(B) || this.isEqualTo(B);
    }

    public boolean isLessThanOrEqualTo(DateTime B) {
        return this.isLessThan(B) || this.isEqualTo(B);
    }

    public Duration minus(DateTime B) {
        return Duration.of(this.date.minus(B.date), this.time.minus(B.time));
    }

    public void addDaysSeconds(long days, long seconds) throws IllegalAccessException {
        long daysChanged = this.time.addSeconds(seconds);
        this.date.addDays(days + daysChanged);
    }

    public void addDuration(Duration duration) throws IllegalAccessException {
        // todo : make the / 1000 go away
        this.addDaysSeconds(duration.getDays(), duration.getMicroseconds() / 1000);
    }

    private DateTime() {
    }

    private boolean isValid() {
        return this.date.isValid() && this.time.isValid();
    }

}
