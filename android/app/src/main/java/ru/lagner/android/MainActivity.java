package ru.lagner.android;

import android.animation.Animator;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.util.Log;
import android.view.SurfaceView;
import android.view.View;
import android.view.ViewGroup;

import org.greenrobot.eventbus.EventBus;
import org.greenrobot.eventbus.Subscribe;
import org.greenrobot.eventbus.ThreadMode;
import org.qtproject.qt5.android.bindings.QtActivity;

import ru.lagner.android.academ_weather.R;


public class MainActivity extends QtActivity {
    private static final String TAG = "ru.lagner";
    private ViewGroup mRootView = null;
    private View mSplash = null;
    private long mOnCreateMills = 0;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        mOnCreateMills = System.currentTimeMillis();
        super.onCreate(savedInstanceState);

        /*
        ColorDrawable back = new ColorDrawable(getResources().getColor(R.color.white_background));

        mRootView = (ViewGroup) getWindow().getDecorView().getRootView();
        mSplash = new SurfaceView(this);
        mSplash.setBackground(back);

        mRootView.addView(mSplash);
        */
    }

    @Override
    public void onStart() {
        super.onStart();
        EventBus.getDefault().register(this);
        Log.i(TAG, "MainActivity::onStart");
    }

    @Override
    public void onStop() {
        EventBus.getDefault().unregister(this);
        super.onStop();
    }

    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onCustomEvent(CustomEvent event) {
        Log.i(TAG, "on event: " + event.Id + "  in thread: " + Thread.currentThread().getId());

        switch (event.Id) {
            case 256: {
                removeJavaSplash();
                break;
            }
            case 257: {
                break;
            }
            default: break;
        }
    }

    private void removeJavaSplash() {
        if (mRootView == null)
            return;

        if (mSplash != null) {
            long delta = System.currentTimeMillis() - mOnCreateMills;
            Log.i(TAG, "[Performance] RemoveJavaSplash time: " + delta);

            mSplash.animate()
                    .alpha(0)
                    .setDuration(400)
                    .setListener(new Animator.AnimatorListener() {
                        @Override
                        public void onAnimationEnd(Animator animation) {
                            mRootView.removeView(mSplash);
                            Log.i(TAG, "java splash was removed");
                        }
                        @Override
                        public void onAnimationStart(Animator animation) {}
                        @Override
                        public void onAnimationCancel(Animator animation) {}
                        @Override
                        public void onAnimationRepeat(Animator animation) {}
                    });
        }
    }
}
