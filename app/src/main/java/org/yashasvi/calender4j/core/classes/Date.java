package org.yashasvi.calender4j.core.classes;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NonNull;
import lombok.ToString;
import org.yashasvi.calender4j.core.exceptions.InvalidDateException;

import java.util.Calendar;

/**
 * 01/01/0001 is the least date supported.
 * Epoch = date 01/01/0001.
 *
 * @author yashasvi sriram
 * @version 2.0
 */

@Getter
@ToString
@EqualsAndHashCode
public class Date {
    // 1 - INT_MAX
    private int year;
    // 1 - 12
    private int month;
    // 1 - 31
    private int day;

    /*
     * StdForm is set of the fields
     * (stdYear, stdMonth, stdDay, monthExtraDays, leapExtraDays)
     *
     * StdForm of a date is such that
     * std_year * 365 + std_month * 30 + std_day + leap_extras + month_extras
     * will give (no of days passed from Epoch 01/01/0001) + 1
     *
     * Ex : for
     *      01/01/0001 => 1
     *      02/01/0001 => 2
     *
     * This is seeing Gregorian Calender (which has so many irregularities)
     * as a uniform calender model
     * with NOISE of extra days in leap years
     * and extra days due to different number of days in months
     * */
    private class StdForm {
        private int leapExtraDays;
        private int monthExtraDays;   // due to varying no days in months , equals
        private int stdYear;
        private int stdMonth;
        private int stdDay;
    }

    public static Date now() {
        Calendar currentTime = Calendar.getInstance();
        Date date = new Date();
        date.day = currentTime.get(Calendar.DAY_OF_MONTH);
        date.month = currentTime.get(Calendar.MONTH) + 1;
        date.year = currentTime.get(Calendar.YEAR);
        return date;
    }

    public static Date of(final int year, final int month, final int day) throws InvalidDateException {
        Date date = new Date();
        date.year = year;
        date.month = month;
        date.day = day;
        if (!date.isValid()) throw new InvalidDateException();
        return date;
    }

    public Date(@NonNull final Date b) {
        this.year = b.year;
        this.month = b.month;
        this.day = b.day;
    }

    /**
     * returns # days from epoch
     */
    public long minusEpoch() {
        StdForm stdForm = this.getStdForm();
        return (stdForm.stdYear) * Constants.DAYS_IN_STD_YEAR
                + (stdForm.stdMonth) * Constants.DAYS_IN_STD_MONTH
                + (stdForm.stdDay)
                + (stdForm.leapExtraDays)
                + (stdForm.monthExtraDays) - 1; // refer to std form definition
    }

    /**
     * returns # days from date
     */
    public long minus(@NonNull final Date date) {
        StdForm stdFormA = this.getStdForm();
        StdForm stdFormB = date.getStdForm();
        return (stdFormA.stdYear - stdFormB.stdYear) * Constants.DAYS_IN_STD_YEAR
                + (stdFormA.stdMonth - stdFormB.stdMonth) * Constants.DAYS_IN_STD_MONTH
                + (stdFormA.stdDay - stdFormB.stdDay)
                + (stdFormA.leapExtraDays - stdFormB.leapExtraDays)
                + (stdFormA.monthExtraDays - stdFormB.monthExtraDays);
    }

    public boolean isLeapYear() {
        return this.year % 400 == 0 || (this.year % 100 != 0 && this.year % 4 == 0);
    }

    public boolean isGreaterThan(@NonNull final Date B) {
        if (this.year > B.year)
            return true;
        else if (this.year < B.year)
            return false;
        if (this.month > B.month)
            return true;
        else if (this.month < B.month)
            return false;
        if (this.day > B.day)
            return true;
        else if (this.day < B.day)
            return false;

        return false;
    }

    public boolean isEqualTo(@NonNull final Date B) {
        return this.day == B.day && this.month == B.month && this.year == B.year;
    }

    public boolean isLessThan(@NonNull final Date B) {
        return B.isGreaterThan(this);
    }

    public boolean isGreaterThanOrEqualTo(Date B) {
        return this.isGreaterThan(B) || this.isEqualTo(B);
    }

    public boolean isLessThanOrEqualTo(Date B) {
        return this.isLessThan(B) || this.isEqualTo(B);
    }

    /**
     * adds param number of (algebraic) days to this date.
     * time complexity is LINEAR in no days to be added.
     * if the date obtained after algebraic addition is invalid rollbacks to initial state and throws IllegalAccessException.
     */
    public void addDays(final long noDays) throws IllegalAccessException {
        Date copy = new Date(this);
        if (noDays == 0) {
            return;
        } else if (noDays > 0) {
            for (long i = 0; i < noDays; i++) {
                this.toTomorrow();
            }
        } else {
            long posNoDays = -noDays;
            for (long i = 0; i < posNoDays; i++) {
                this.toYesterday();
            }
        }
        // roll back and throw exception
        if (!this.isValid()) {
            this.year = copy.year;
            this.month = copy.month;
            this.day = copy.day;
            throw new IllegalAccessException("Date before 01/01/0001 is not supported");
        }
    }

    private Date() {
    }

    boolean isValid() {
        if (this.year < 1)
            return false;
        if (this.month < 1 || this.month > 12)
            return false;
        switch (this.month % 2) {
            case 1:
                if (this.month >= 9)
                    return !(this.day < 1 || this.day > 30);
                else
                    return !(this.day < 1 || this.day > 31);
            case 0:
                if (this.month == 2) {
                    if (this.isLeapYear())
                        return !(this.day < 1 || this.day > 29);
                    else
                        return !(this.day < 1 || this.day > 28);
                } else if (this.month >= 8)
                    return !(this.day < 1 || this.day > 31);
                else
                    return !(this.day < 1 || this.day > 30);
            default:
                return false;
        }
    }

    private StdForm getStdForm() {
        StdForm stdForm = new StdForm();
        stdForm.stdDay = this.day;
        // monthExtraDays
        stdForm.stdMonth = this.month - 1;
        if (this.month > 1)
            stdForm.monthExtraDays = Constants.STD_MONTH_EXTRAS_ARRAY[this.month - 2];
        else
            stdForm.monthExtraDays = 0;
        // leapExtraDays
        stdForm.stdYear = this.year - 1;
        stdForm.leapExtraDays = this.year / 4 - this.year / 100 + this.year / 400;
        if (this.isLeapYear() && this.month < 3 && stdForm.leapExtraDays > 0)
            stdForm.leapExtraDays--;
        return stdForm;
    }

    private void toTomorrow() {
        if (this.isLeapYear()) {
            if (this.day + 1 > Constants.DAYS_IN_MONTH_LY[this.month - 1]) {
                if (this.month + 1 > 12) {
                    this.year += 1;
                    this.month = 1;
                    this.day = 1;
                } else {
                    this.month += 1;
                    this.day = 1;
                }
            } else {
                this.day += 1;
            }
        } else {
            if (this.day + 1 > Constants.DAYS_IN_MONTH_NLY[this.month - 1]) {
                if (this.month + 1 > 12) {
                    this.year += 1;
                    this.month = 1;
                    this.day = 1;
                } else {
                    this.month += 1;
                    this.day = 1;
                }
            } else {
                this.day += 1;
            }
        }
    }

    // date may become invalid
    // this method does not keep that in check
    private void toYesterday() {
        if (this.isLeapYear()) {
            if (this.day - 1 < 1) {
                if (this.month - 1 < 1) {
                    this.year -= 1;
                    this.month = 12;
                    this.day = 31;
                } else {
                    this.month -= 1;
                    this.day = Constants.DAYS_IN_MONTH_LY[this.month - 1];
                }
            } else {
                this.day -= 1;
            }
        } else {
            if (this.day - 1 < 1) {
                if (this.month - 1 < 1) {
                    this.year -= 1;
                    this.month = 12;
                    this.day = 31;
                } else {
                    this.month -= 1;
                    this.day = Constants.DAYS_IN_MONTH_NLY[this.month - 1];
                }
            } else {
                this.day -= 1;
            }
        }
    }
}
