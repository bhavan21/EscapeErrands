package org.yashasvi.escapeerrands.beans;


import android.support.annotation.Nullable;

import org.yashasvi.calender4j.core.classes.DateTime;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;
import lombok.ToString;

@Getter
@EqualsAndHashCode
@ToString
public class Goal implements Serializable {
    private int id;
    private List<Integer> parentIds;
    private List<Integer> childIds;
    private String description;
    @Nullable
    private DateTime deadline;
    private boolean isAchieved;

    public Goal(final int id,
                @NonNull final List<Integer> parentIds,
                @NonNull final List<Integer> childIds,
                @NonNull final String description,
                @Nullable final DateTime deadline,
                final boolean isAchieved) {
        this.id = id;
        this.parentIds = parentIds;
        this.childIds = childIds;
        this.description = description;
        this.deadline = deadline;
        this.isAchieved = isAchieved;
    }
}
