package org.yashasvi.escapeerrands;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.CheckBox;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.yashasvi.calender4j.core.classes.DateTime;
import org.yashasvi.escapeerrands.beans.Goal;

import java.util.List;

// todo : do this better if possible
public class GoalListAdapter extends BaseAdapter {
    private static LayoutInflater inflater = null;

    private Context context;
    private List<Goal> goalDataList;

    public GoalListAdapter(Context context, List<Goal> goalDataList) {
        this.context = context;
        this.goalDataList = goalDataList;
        inflater = (LayoutInflater) this.context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    }

    @Override
    public int getCount() {
        return this.goalDataList.size();
    }

    @Override
    public View getView(final int position, View convertView, ViewGroup parent) {
        View rowView = inflater.inflate(R.layout.goal_item, parent, false);

        DataViewBinder dataViewBinder = new DataViewBinder(rowView);
        dataViewBinder.bind(goalDataList.get(position));

        rowView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
            }
        });
        rowView.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View view) {
                return false;
            }
        });

        return rowView;
    }

    private class DataViewBinder {
        private LinearLayout goalItemContainer;
        private TextView description;
        private TextView deadline;
        private CheckBox isAchieved;

        DataViewBinder(View rowView) {
            this.goalItemContainer = rowView.findViewById(R.id.goal_item);
            this.description = this.goalItemContainer.findViewById(R.id.goal_item_description);
            this.deadline = this.goalItemContainer.findViewById(R.id.goal_item_deadline);
            this.isAchieved = this.goalItemContainer.findViewById(R.id.goal_item_is_achieved);
        }

        void bind(Goal goal) {
            this.description.setText(goal.getDescription());
            if (goal.getDeadline() == null)
                this.deadline.setText("#");
            else {
                // todo : do this better
                DateTime dt = goal.getDeadline();
                String dts = dt.getDate().getDay() + "/" +
                        dt.getDate().getMonth() + "/" +
                        dt.getDate().getYear() + " " +
                        dt.getTime().getHour() + ":" +
                        dt.getTime().getMinute() + ":" +
                        dt.getTime().getSecond();
                this.deadline.setText(dts);
            }
            this.isAchieved.setChecked(goal.isAchieved());
        }
    }

    @Override
    public Object getItem(int position) {
        return position;
    }

    @Override
    public long getItemId(int position) {
        return position;
    }
}
