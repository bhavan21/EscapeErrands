package org.yashasvi.escapeerrands.restapiimpl;

import android.annotation.TargetApi;
import android.os.Build;
import android.support.annotation.RequiresApi;

import org.androidannotations.annotations.EBean;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.yashasvi.calender4j.core.classes.DateTime;
import org.yashasvi.calender4j.core.exceptions.InvalidDateException;
import org.yashasvi.calender4j.core.exceptions.InvalidTimeException;
import org.yashasvi.escapeerrands.models.Goal;
import org.yashasvi.escapeerrands.restapi.GoalDAO;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.TimeUnit;

import lombok.NonNull;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class GoalDAOImpl implements GoalDAO {

    @Override
    public List<Goal> getGoalsByRegex(@NonNull String pattern) {
        try {
            HttpUrl.Builder urlBuilder = HttpUrl.parse("https://eser.herokuapp.com/rest/goal/read/regex/").newBuilder();
            urlBuilder.addQueryParameter("search", pattern);
            String url = urlBuilder.build().toString();

            System.out.println(url);

            OkHttpClient client = new OkHttpClient.Builder()
                    .connectTimeout(60, TimeUnit.SECONDS)
                    .readTimeout(30, TimeUnit.SECONDS)
                    .build();

            Request request = new Request.Builder().url(url).build();

            Response response = client.newCall(request).execute();

            JSONObject jsonObject = new JSONObject(response.body().string());
            JSONArray body = jsonObject.getJSONArray("body");

            List<Goal> answer = new ArrayList<>();
            for (int i = 0; i < body.length(); ++i) {
                JSONObject jsonGoal = body.getJSONObject(i);
                Goal goal = new Goal();
                goal.setId(jsonGoal.getInt("id"));
                goal.setDescription(jsonGoal.getString("description"));
                goal.setAchieved(jsonGoal.getBoolean("is_achieved"));

                JSONArray jParentIds = jsonGoal.getJSONArray("parent_ids");
                List<Integer> parentIds = new ArrayList<>();
                for (int j = 0; j < jParentIds.length(); j++) {
                    parentIds.add(jParentIds.getInt(i));
                }
                goal.setParentIds(parentIds);

                JSONArray jChildIds = jsonGoal.getJSONArray("child_ids");
                List<Integer> childIds = new ArrayList<>();
                for (int j = 0; j < jChildIds.length(); j++) {
                    childIds.add(jChildIds.getInt(i));
                }
                goal.setChildIds(childIds);

                if (!Objects.equals(jsonGoal.getString("deadline"), "null")) {
                    JSONObject jDeadline = jsonGoal.getJSONObject("deadline");
                    DateTime deadline = DateTime.of(
                            jDeadline.getInt("year"),
                            jDeadline.getInt("month"),
                            jDeadline.getInt("day"),
                            jDeadline.getInt("hour"),
                            jDeadline.getInt("minute"),
                            jDeadline.getInt("second"),
                            jDeadline.getInt("microsecond")
                    );
                    goal.setDeadline(deadline);
                } else {
                    goal.setDeadline(null);
                }
                answer.add(goal);
            }

            return answer;
        } catch (IOException | JSONException | NullPointerException | InvalidDateException | InvalidTimeException e) {
            e.printStackTrace();
            return null;
        }
    }

    @Override
    public List<Goal> getFamilyOfGoal(int id) {
        return null;
    }

}
