package org.yashasvi.escapeerrands.models;


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
    private LocalDateTime deadline;
    private boolean isAchieved;

    public Goal(int id, List<Integer> parents, List<Integer> children, String description, LocalDateTime deadline, boolean isAchieved) {
        this.id = id;
        this.parentIds = parents;
        this.childIds = children;
        this.description = description;
        this.deadline = deadline;
        this.isAchieved = isAchieved;
    }

}
