package org.yashasvi.escapeerrands.models;


import org.yashasvi.calender4j.core.classes.DateTime;

import java.time.LocalDateTime;
import java.util.List;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@EqualsAndHashCode
@ToString
public class Goal {
    private int id;
    private List<Integer> parentIds;
    private List<Integer> childIds;
    private String description;
    private DateTime deadline;
    private boolean isAchieved;

    public Goal() {
    }

    public Goal(int id, List<Integer> parents, List<Integer> children, String description, DateTime deadline, boolean isAchieved) {
        this.id = id;
        this.parentIds = parents;
        this.childIds = children;
        this.description = description;
        this.deadline = deadline;
        this.isAchieved = isAchieved;
    }

}
