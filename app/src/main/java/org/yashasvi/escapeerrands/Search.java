package org.yashasvi.escapeerrands;

import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.SearchView;
import android.view.Menu;

import org.androidannotations.annotations.EActivity;

@EActivity(R.layout.a_search)
public class Search extends AppCompatActivity {

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.search_menu, menu);

        SearchView searchView = (SearchView) menu.findItem(R.id.search_menu_search_item).getActionView();
        searchView.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
            @Override
            public boolean onQueryTextSubmit(String string) {
                return false;
            }

            @Override
            public boolean onQueryTextChange(String string) {
                return false;
            }
        });

        return true;
    }

}
