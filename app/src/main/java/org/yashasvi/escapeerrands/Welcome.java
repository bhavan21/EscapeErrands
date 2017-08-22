package org.yashasvi.escapeerrands;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;

import org.androidannotations.annotations.AfterViews;
import org.androidannotations.annotations.Background;
import org.androidannotations.annotations.Click;
import org.androidannotations.annotations.EActivity;
import org.androidannotations.annotations.UiThread;
import org.androidannotations.annotations.ViewById;
import org.androidannotations.api.BackgroundExecutor;


@EActivity(R.layout.a_welcome)
public class Welcome extends AppCompatActivity {

    private static final String WELCOME_MESSAGE = "Hi There!\nWelcome To\nEscape Errands!";

    @ViewById
    TextView welcomeMessage;

    @AfterViews
    void afterViews() {
        startWelcomeAnimation();
    }

    @Background(id = "welcome_animation")
    void startWelcomeAnimation() {
        try {
            for (int i = 0; i < WELCOME_MESSAGE.length() + 1; ++i) {
                renderString(WELCOME_MESSAGE.substring(0, i));
                Thread.sleep(50);
            }
        } catch (InterruptedException ignored) {

        }
    }

    @UiThread
    void renderString(String string) {
        welcomeMessage.setText(string);
    }

    @Click({R.id.welcome_message})
    void startApp() {
        BackgroundExecutor.cancelAll("welcome_animation", true);
        welcomeMessage.setText(WELCOME_MESSAGE);
        startActivity(new Intent(this, Search_.class));
        finish();
    }
}
