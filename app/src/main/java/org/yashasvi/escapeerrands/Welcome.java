package org.yashasvi.escapeerrands;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;


public class Welcome extends AppCompatActivity {

    private static final String WELCOME_MESSAGE = "Escape Errands!";
    private TextView welcomeMessage;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.a_welcome);
        welcomeMessage = (TextView) findViewById(R.id.a_welcome_message);
        new WelcomeAnimator().execute();
    }

    private class WelcomeAnimator extends AsyncTask<Integer, String, Integer> {
        @Override
        protected Integer doInBackground(Integer... integers) {
            try {
                Thread.sleep(500);
                for (int i = 0; i < WELCOME_MESSAGE.length() + 1; ++i) {
                    publishProgress(WELCOME_MESSAGE.substring(0, i));
                    Thread.sleep(10);
                }
                Thread.sleep(100);
            } catch (InterruptedException ignored) {

            }
            return null;
        }

        @Override
        protected void onPostExecute(Integer integer) {
            startActivity(new Intent(Welcome.this, Glance.class));
            Welcome.this.finish();
        }

        @Override
        protected void onProgressUpdate(String... strings) {
            welcomeMessage.setText(strings[0]);
        }
    }

}
