package org.yashasvi.escapeerrands;

import android.content.Context;
import android.os.AsyncTask;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.CheckBox;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import org.yashasvi.calender4j.core.classes.DateTime;
import org.yashasvi.escapeerrands.beans.Goal;
import org.yashasvi.escapeerrands.daoimpls.GoalDAOImpl;
import org.yashasvi.escapeerrands.daos.GoalDAO;

import java.util.List;

import es.dmoral.toasty.Toasty;

// todo : do this better if possible
public class GoalListAdapter extends BaseAdapter {
    private static LayoutInflater inflater = null;

    private Context context;
    private List<Goal> goalDataList;
    private GoalDAO goalDAO = new GoalDAOImpl();

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
                TextView goalIdTV = v.findViewById(R.id.goal_item_id);
                CheckBox isAchievedCB = v.findViewById(R.id.goal_item_is_achieved);
                int id = Integer.parseInt(goalIdTV.getText().toString());
                new IsAchievedToggler(isAchievedCB).execute(id);
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

    @Override
    public Object getItem(int position) {
        return position;
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    private class DataViewBinder {
        private LinearLayout goalItemContainer;
        private TextView id;
        private TextView description;
        private TextView deadline;
        private CheckBox isAchieved;

        DataViewBinder(View rowView) {
            this.goalItemContainer = rowView.findViewById(R.id.goal_item);
            this.id = this.goalItemContainer.findViewById(R.id.goal_item_id);
            this.description = this.goalItemContainer.findViewById(R.id.goal_item_description);
            this.deadline = this.goalItemContainer.findViewById(R.id.goal_item_deadline);
            this.isAchieved = this.goalItemContainer.findViewById(R.id.goal_item_is_achieved);
        }

        void bind(Goal goal) {
            this.id.setText(Integer.toString(goal.getId()));
            this.description.setText(goal.getDescription());
            if (goal.getDeadline() == null)
                this.deadline.setText(".");
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

    private class IsAchievedToggler extends AsyncTask<Integer, Integer, Boolean> {

        private CheckBox isAchievedCB;

        public IsAchievedToggler(CheckBox isAchievedCB) {
            this.isAchievedCB = isAchievedCB;
        }

        @Override
        protected Boolean doInBackground(Integer... integers) {
            return goalDAO.toggleIsAchieved(integers[0]);
        }

        @Override
        protected void onPostExecute(Boolean isAchieved) {
            if (isAchieved == null) {
                Toasty.info(context, "Error toggling!", Toast.LENGTH_SHORT).show();
            } else {
                isAchievedCB.setChecked(isAchieved);
            }
        }
    }

}
