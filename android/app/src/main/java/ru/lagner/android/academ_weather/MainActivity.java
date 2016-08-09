package ru.lagner.android.academ_weather;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {
    private Button mPushQt = null;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mPushQt = (Button) findViewById(R.id.push_qt);

        mPushQt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                runQtActivity();
            }
        });
    }

    private void runQtActivity() {
        Intent intent = new Intent(this, LocalQtActivity.class);
        startActivity(intent);
    }
}
