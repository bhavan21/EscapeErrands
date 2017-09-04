package org.yashasvi.escapeerrands.daos;

import android.support.annotation.Nullable;

import org.yashasvi.escapeerrands.beans.Goal;

import java.util.List;

import lombok.NonNull;

public interface GoalDAO {
    /**
     * @return null if any problem else # of matched goals
     */
    @Nullable
    public List<Goal> getGoalsByRegex(@NonNull final String pattern);

    public List<Goal> getFamilyOfGoal(final int id);

    /**
     * @return value of goal's is_achieved after toggling or null if any problem
     */
    @Nullable
    public Boolean toggleIsAchieved(final int id);
}
