package ru.lagner.android;

import android.util.Log;
import org.greenrobot.eventbus.EventBus;


public class CppEventBus {
    private static final String TAG = "ru.lagner";
    private static EventBus instance = null;

    public static void init() {
        Log.i(TAG, "init cpp bus here");

        Class klass = CppEventBus.class;
        Log.i(TAG, "name: " + klass.getName());
        Log.i(TAG, "canonical name: " + klass.getCanonicalName());
        Log.i(TAG, "simple name: " + klass.getSimpleName());
    }

    public static boolean postEvent(int id) {
        Log.i(TAG, "java postEvent!!!!");

        try {
            if (instance == null) {
                instance = EventBus.getDefault();
            }

            String description = "test description";

            instance.post(new CustomEvent(id, description, "", null));

        } catch (final Exception ex) {
            Log.w(TAG, "can not post cpp event: " + ex.getMessage());
            return false;
        }
        return true;
    }
}
