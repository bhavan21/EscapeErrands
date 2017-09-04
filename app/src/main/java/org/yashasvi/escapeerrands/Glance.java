package org.yashasvi.escapeerrands;

import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.SearchView;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ListView;
import android.widget.Toast;

import org.yashasvi.escapeerrands.beans.Goal;
import org.yashasvi.escapeerrands.daos.GoalDAO;
import org.yashasvi.escapeerrands.daoimpls.GoalDAOImpl;

import java.util.List;

import es.dmoral.toasty.Toasty;

public class Glance extends AppCompatActivity {

    private GoalDAO goalDAO = new GoalDAOImpl();
    private ListView goalListView;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.a_glance);
        goalListView = (ListView) findViewById(R.id.a_glance_goal_list);
        new GoalPuller("").execute();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.glance_menu, menu);

        SearchView searchView = (SearchView) menu.findItem(R.id.a_glance_menu_search_item).getActionView();
        searchView.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
            @Override
            public boolean onQueryTextSubmit(String string) {
                new GoalPuller(string).execute();
                return false;
            }

            @Override
            public boolean onQueryTextChange(String string) {
                return false;
            }
        });

        MenuItem pullAllGoals = menu.findItem(R.id.a_glance_menu_pull_all_goals_item);
        pullAllGoals.setOnMenuItemClickListener(new MenuItem.OnMenuItemClickListener() {
            @Override
            public boolean onMenuItemClick(MenuItem menuItem) {
                new GoalPuller("").execute();
                return false;
            }
        });

        return true;
    }

    private class GoalPuller extends AsyncTask<String, Integer, List<Goal>> {
        private ProgressDialog progressDialog;
        private String pattern;

        public GoalPuller(final String pattern) {
            this.pattern = pattern;
            progressDialog = new ProgressDialog(Glance.this);
            progressDialog.setMessage("Connecting ...");
            progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
            progressDialog.setCancelable(false);
            progressDialog.setCanceledOnTouchOutside(false);
            progressDialog.setIndeterminate(true);
            progressDialog.show();
        }

        @Override
        protected List<Goal> doInBackground(final String... strings) {
            return goalDAO.getGoalsByRegex(pattern);
        }

        @Override
        protected void onPostExecute(final List<Goal> goalList) {
            if (goalList == null) {
                Toasty.error(Glance.this, "Could not fetch goals!", Toast.LENGTH_SHORT).show();
            } else {
                goalListView.setAdapter(new GoalListAdapter(Glance.this, goalList));
            }
            progressDialog.dismiss();
        }
    }

}
