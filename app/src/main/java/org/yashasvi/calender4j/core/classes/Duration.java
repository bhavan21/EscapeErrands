package org.yashasvi.calender4j.core.classes;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.ToString;

// handles DateTime difference
@Getter
@ToString
@EqualsAndHashCode
public class Duration {
    private long days;
    private long microseconds;

    public static Duration of(long days, long microseconds) {
        Duration duration = new Duration();
        duration.days = days;
        duration.microseconds = microseconds;
        return duration;
    }

    public Duration(Duration b) {
        this.days = b.days;
        this.microseconds = b.microseconds;
    }

    public void plus(Duration b) {
        this.days += b.days;
        this.microseconds += b.microseconds;
    }

    public void minus(Duration b) {
        this.days -= b.days;
        this.microseconds -= b.microseconds;
    }

    public void normalize() {
        this.days += this.microseconds / Constants.MICROSECONDS_IN_DAY;
        this.microseconds = this.microseconds % Constants.MICROSECONDS_IN_DAY;
    }

    private Duration() {
    }
}
