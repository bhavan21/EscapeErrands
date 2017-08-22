package org.yashasvi.calender4j.core.classes;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NonNull;
import lombok.ToString;
import org.yashasvi.calender4j.core.exceptions.InvalidTimeException;

import java.util.Calendar;

// measures a day
// day starts from 00:00:00.0 ends at 23:59:59.999999
@Getter
@ToString
@EqualsAndHashCode
public class Time {
    // 0 - 23
    private int hour;
    // 0 - 59
    private int minute;
    // 0 - 59
    private int second;
    // 0 - 999999
    private int microsecond;

    public static Time now() {
        Calendar currentTime = Calendar.getInstance();
        Time time = new Time();
        time.hour = currentTime.get(Calendar.HOUR_OF_DAY);// 24hr format
        time.minute = currentTime.get(Calendar.MINUTE);
        time.second = currentTime.get(Calendar.SECOND);
        time.microsecond = currentTime.get(Calendar.MILLISECOND) * 1000;
        return time;
    }

    public static Time of(final int hour, final int minute, final int second, final int microsecond) throws InvalidTimeException {
        Time time = new Time();
        time.hour = hour;
        time.minute = minute;
        time.second = second;
        time.microsecond = microsecond;
        if (!time.isValid()) throw new InvalidTimeException();
        return time;
    }

    public Time(@NonNull final Time b) {
        this.hour = b.hour;
        this.minute = b.minute;
        this.second = b.second;
        this.microsecond = b.microsecond;
    }

    private Time() {
    }

    // 00:00:00.0 - 23:59:59.999999 are valid
    boolean isValid() {
        if (this.hour < 0 || this.hour > 23) return false;
        if (this.minute < 0 || this.minute > 59) return false;
        if (this.second < 0 || this.second > 59) return false;
        if (this.microsecond < 0 || this.microsecond > 999999) return false;
        return true;
    }

    public boolean isGreaterThan(@NonNull final Time B) {
        if (this.hour > B.hour) return true;
        else if (this.hour < B.hour) return false;
        if (this.minute > B.minute) return true;
        else if (this.minute < B.minute) return false;
        if (this.second > B.second) return true;
        else if (this.second < B.second) return false;
        if (this.microsecond > B.microsecond) return true;
        else if (this.microsecond < B.microsecond) return false;
        return false;
    }

    public boolean isEqualTo(@NonNull final Time B) {
        return this.second == B.second && this.minute == B.minute && this.hour == B.hour && this.microsecond == B.microsecond;
    }

    public boolean isLessThan(@NonNull final Time B) {
        return B.isGreaterThan(this);
    }

    public boolean isGreaterThanOrEqualTo(Time B) {
        return this.isGreaterThan(B) || this.isEqualTo(B);
    }

    public boolean isLessThanOrEqualTo(Time B) {
        return this.isLessThan(B) || this.isEqualTo(B);
    }

    // return A - B in microseconds with sign
    public long minus(@NonNull final Time B) {
        return (long) (this.hour - B.hour) * Constants.MICROSECONDS_IN_HOUR
                + (long) (this.minute - B.minute) * Constants.MICROSECONDS_IN_MINUTE
                + (long) (this.second - B.second) * Constants.MICROSECONDS_IN_SECOND
                + (long) (this.microsecond - B.microsecond);
    }

    // adds seconds to this time day circularly
    // returns # day changes occurred, NOT # overflows
    private long add(final long seconds) {
        if (seconds < 0)
            return 0;

        long dayChanges = seconds / Constants.SECONDS_IN_DAY;
        int _day = (int) (seconds % Constants.SECONDS_IN_DAY);

        // _day belongs to [0,86399] therefore no extra days
        int hours = _day / Constants.SECONDS_IN_HOUR;
        int _hour = _day % Constants.SECONDS_IN_HOUR;

        int minutes = _hour / Constants.SECONDS_IN_MINUTE;
        int _minute = _hour % Constants.SECONDS_IN_MINUTE;

        int $seconds = _minute % Constants.SECONDS_IN_MINUTE;

        int prevSec = this.second;
        int prevMin = this.minute;
        int prevHour = this.hour;

        this.second = (prevSec + $seconds) % Constants.SECONDS_IN_MINUTE;
        int extraMinute = (prevSec + $seconds) / Constants.SECONDS_IN_MINUTE;

        this.minute = (prevMin + minutes + extraMinute) % Constants.MINUTES_IN_HOUR;
        int extraHour = (prevMin + minutes + extraMinute) / Constants.MINUTES_IN_HOUR;

        this.hour = (prevHour + hours + extraHour) % Constants.HOURS_IN_DAY;

        // due to day change
        if (this.hour < prevHour)
            dayChanges++;
        else if (prevHour == this.hour && this.minute < prevMin)
            dayChanges++;
        else if (prevHour == this.hour && prevMin == this.minute && this.second < prevSec)
            dayChanges++;

        return dayChanges;
    }

    // subtracts seconds to this time day circularly
    // returns # day changes occurred, NOT # overflows
    private long subtract(final long seconds) {
        if (seconds < 0)
            return 0;

        long dayChanges = -(seconds / Constants.SECONDS_IN_DAY);
        // remainingSeconds [0,86399]
        int remainingSeconds = (int) (seconds % Constants.SECONDS_IN_DAY);
        // instead of going back remainingSeconds
        int complementarySeconds = Constants.SECONDS_IN_DAY - remainingSeconds;
        // go backward 1 day and go forward complementarySeconds
        dayChanges = dayChanges - 1;
        dayChanges = dayChanges + this.add(complementarySeconds);

        return dayChanges;
    }

    // adds algebraic seconds to this time circularly
    // returns # day changes occurred, NOT # overflows
    public long addSeconds(final long seconds) {
        if (seconds == 0)
            return 0;
        else if (seconds > 0)
            return this.add(seconds);
        else
            return this.subtract(-seconds);
    }
}

