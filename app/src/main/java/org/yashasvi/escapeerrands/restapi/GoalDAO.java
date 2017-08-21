package org.yashasvi.escapeerrands.restapi;

import org.yashasvi.escapeerrands.models.Goal;

import java.util.List;

import lombok.NonNull;

public interface GoalDAO {
    /**
     * @return null if any problem else # of matched goals
     * */
    public List<Goal> getGoalsByRegex(@NonNull final String pattern);
    public List<Goal> getFamilyOfGoal(final int id);
}
