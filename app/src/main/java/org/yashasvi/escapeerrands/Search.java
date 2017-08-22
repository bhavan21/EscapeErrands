package org.yashasvi.escapeerrands;

import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.SearchView;
import android.view.Menu;
import android.widget.ListView;
import android.widget.Toast;

import org.androidannotations.annotations.Background;
import org.androidannotations.annotations.EActivity;
import org.androidannotations.annotations.UiThread;
import org.androidannotations.annotations.ViewById;
import org.yashasvi.escapeerrands.models.Goal;
import org.yashasvi.escapeerrands.restapi.GoalDAO;
import org.yashasvi.escapeerrands.restapiimpl.GoalDAOImpl;

import java.util.List;

import lombok.NonNull;

@EActivity(R.layout.a_search)
public class Search extends AppCompatActivity {

    private GoalDAO goalDAO = new GoalDAOImpl();

    @ViewById(R.id.a_search_goal_list)
    ListView goalList;

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.search_menu, menu);

        SearchView searchView = (SearchView) menu.findItem(R.id.search_menu_search_item).getActionView();
        searchView.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
            @Override
            public boolean onQueryTextSubmit(String string) {
                fetchGoals(string);
                return false;
            }

            @Override
            public boolean onQueryTextChange(String string) {
                return false;
            }
        });

        return true;
    }

    @Background
    void fetchGoals(@NonNull final String pattern) {
        List<Goal> goalList = goalDAO.getGoalsByRegex(pattern);
        if (goalList == null) {
            showMessage("Could not fetch goals");
        } else {
            renderGoals(goalList);
        }
    }

    @UiThread
    void renderGoals(@NonNull final List<Goal> goalList) {
        this.goalList.setAdapter(new GoalListAdapter(Search.this, goalList));
    }

    @UiThread
    void showMessage(@NonNull final String message) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
    }

}
