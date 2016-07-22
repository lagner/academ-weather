package ru.lagner.android;

import android.content.Intent;
import android.content.pm.ComponentInfo;
import android.content.pm.PackageManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;


public class SplashScreenActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        CppEventBus.init();

        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
        overridePendingTransition(0, 0);

        finish();
    }

    private void loadNativeLibs() {
        long startTime = System.currentTimeMillis();
        int nums = 0;

        ComponentInfo m_contextInfo;

        String[] m_qtLibs;

        try {
            m_contextInfo = getPackageManager().getActivityInfo(getComponentName(), PackageManager.GET_META_DATA);

            if (m_contextInfo.metaData.containsKey("android.app.qt_libs_resource_id")) {
                int resourceId = m_contextInfo.metaData.getInt("android.app.qt_libs_resource_id");
                m_qtLibs = getResources().getStringArray(resourceId);

                if (m_qtLibs != null) {
                    for (int i = 0; i < m_qtLibs.length; i++) {
                        System.loadLibrary(m_qtLibs[i]);
                    }
                    nums = m_qtLibs.length;
                }
            }
        } catch (PackageManager.NameNotFoundException e) {
            e.printStackTrace();
        }
        Log.i("splash", "loaded " + nums + " libs. Spent: " + (System.currentTimeMillis() - startTime));
    }
}
