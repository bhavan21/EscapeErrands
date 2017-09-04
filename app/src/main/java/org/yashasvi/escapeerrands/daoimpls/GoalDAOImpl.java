package org.yashasvi.escapeerrands.daoimpls;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.yashasvi.calender4j.core.classes.DateTime;
import org.yashasvi.calender4j.core.exceptions.InvalidDateException;
import org.yashasvi.calender4j.core.exceptions.InvalidTimeException;
import org.yashasvi.escapeerrands.beans.Goal;
import org.yashasvi.escapeerrands.daos.GoalDAO;

import java.io.IOException;
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
            // Sending request
            HttpUrl.Builder urlBuilder = HttpUrl.parse("https://escape-errands.herokuapp.com/rest/goal/read/regex/").newBuilder();
            urlBuilder.addQueryParameter("search", pattern);
            String url = urlBuilder.build().toString();

            OkHttpClient client = new OkHttpClient.Builder()
                    .connectTimeout(60, TimeUnit.SECONDS)
                    .readTimeout(30, TimeUnit.SECONDS)
                    .build();

            Request request = new Request.Builder().url(url).build();
            Response response = client.newCall(request).execute();

            // Parsing response
            JSONObject httpBody = new JSONObject(response.body().string());
            // NOTE : there is a body JSON array in body HTTP
            JSONArray body = httpBody.getJSONArray("body");

            List<Goal> answer = new ArrayList<>();
            for (int i = 0; i < body.length(); ++i) {
                JSONObject jsonGoal = body.getJSONObject(i);

                JSONArray jParentIds = jsonGoal.getJSONArray("parent_ids");
                List<Integer> parentIds = new ArrayList<>();
                for (int j = 0; j < jParentIds.length(); j++) {
                    parentIds.add(jParentIds.getInt(i));
                }

                JSONArray jChildIds = jsonGoal.getJSONArray("child_ids");
                List<Integer> childIds = new ArrayList<>();
                for (int j = 0; j < jChildIds.length(); j++) {
                    childIds.add(jChildIds.getInt(i));
                }

                DateTime deadline;
                if (!Objects.equals(jsonGoal.getString("deadline"), "null")) {
                    JSONObject jDeadline = jsonGoal.getJSONObject("deadline");
                    deadline = DateTime.of(
                            jDeadline.getInt("year"),
                            jDeadline.getInt("month"),
                            jDeadline.getInt("day"),
                            jDeadline.getInt("hour"),
                            jDeadline.getInt("minute"),
                            jDeadline.getInt("second"),
                            jDeadline.getInt("microsecond")
                    );
                } else {
                    deadline = null;
                }

                Goal goal = new Goal(
                        jsonGoal.getInt("id"),
                        parentIds,
                        childIds,
                        jsonGoal.getString("description"),
                        deadline,
                        jsonGoal.getBoolean("is_achieved")
                );

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
