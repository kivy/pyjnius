.. _android:

Android
=======

Android have a great and extensive API to control the device, your application
etc. Some part of the Android API is accessible directly with Pyjnius, but some
of them requires you to code in Java.


Get the DPI
-----------

The `DisplayMetrics
<http://developer.android.com/reference/android/util/DisplayMetrics.html>`_ contains multiple fields that can return a lot of information about the device's screen::

    from pyjnius.reflect import autoclass
    DisplayMetrics = autoclass('android.util.DisplayMetrics')
    metrics = DisplayMetrics()
    print 'DPI', metrics.densityDpi


Recording an audio file
-----------------------

By looking at the `Audio Capture
<http://developer.android.com/guide/topics/media/audio-capture.html>`_ guide
from Android, you can see the simple step to do for recording an audio file.
Let's do in with Pyjnius::

    from pyjnius.reflect import autoclass
    from time import sleep

    # get the needed Java class
    MediaRecorder = autoclass('android.media.MediaRecorder')
    AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
    OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
    AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')

    # create out recorder
    mRecorder = MediaRecorder()
    mRecorder.setAudioSource(AudioSource.MIC)
    mRecorder.setOutputFormat(OutputFormat.THREE_GPP) 
    mRecorder.setOutputFile('/sdcard/testrecorder.3gp')
    mRecorder.setAudioEncoder(AudioEncoder.ARM_NB)
    mRecorder.prepare()

    # record 5 seconds
    mRecorder.start()
    sleep(5)
    mRecorder.stop()
    mRecorder.release()

And tada, you'll have a `/sdcard/testrecorder.3gp` file!


Playing an audio file
---------------------

Following the previous section on how to record an audio file, you can read it
using the Android Media Player too::

    from pyjnius.reflect import autoclass
    from time import sleep

    # get the MediaPlayer java class
    MediaPlayer = autoclass('android.media.MediaPlayer')

    # create our player
    mPlayer = MediaPlayer()
    mPlayer.setDataSource('/sdcard/testrecorder.3gp')
    mPlayer.prepare()

    # play
    print 'duration:', mPlayer.getDuration()
    mPlayer.start()
    print 'current position:', mPlayer.getCurrentPosition()
    sleep(5)

    # then after the play:
    mPlayer.release()


Accessing to the Activity
-------------------------

This example will show how to start a new Intent. Be careful, some Intent
require you to setup some parts in the `AndroidManifest.xml`, and have some
actions done within your own Activity. This is out of the scope of Pyjnius, but
we'll show you what is the best approach for playing with it.

On Python-for-android project, you can access to the default `PythonActivity`.
Let's see an example that demonstrate the `Intent.ACTION_VIEW`::

    from jnius import cast
    from jnius.reflect import autoclass

    # import the needed Java class
    PythonActivity = autoclass('org.renpy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')

    # create the intent
    intent = Intent()
    intent.setAction(Intent.ACTION_VIEW)
    intent.setData(Uri('http://kivy.org'))

    # PythonActivity.mActivity is the instance of the current Activity
    # BUT, startActivity is a method from the Activity class, not our
    # PythonActivity.
    # We need to cast our class into an activity, and use it
    currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
    currentActivity.startActivity(intent)

    # The website will open.


Accelerometer access
--------------------

The accelerometer is a good example that show how you need to wrote a little
Java code that you can access later with Pyjnius.

The `SensorManager
<http://developer.android.com/reference/android/hardware/SensorManager.html>`_
lets you access to the device's sensors. To use it, you need to register a
`SensorEventListener
<http://developer.android.com/reference/android/hardware/SensorEventListener.html>`_
and overload 2 abstract methods: `onAccuracyChanged` and `onSensorChanged`.

Open your python-for-android distribution, go in the `src` directory, and
create a file `org/myapp/Hardware.java`. In this file, you will create
everything needed for accessing the accelerometer::

    package org.myapp;

    import org.renpy.android.PythonActivity;
    import android.content.Context;
    import android.hardware.Sensor;
    import android.hardware.SensorEvent;
    import android.hardware.SensorEventListener;
    import android.hardware.SensorManager;

    public class Hardware {

        // Contain the last event we got from the listener
        static public SensorEvent lastEvent = null;
         
        // Define a new listener
        static class AccelListener implements SensorEventListener {
            public void onSensorChanged(SensorEvent ev) {
                lastEvent = ev;
            }
            public void onAccuracyChanged(Sensor sensor , int accuracy) {
            }
        }

        // Create our listener
        static AccelListener accelListener = new AccelListener();

        // Method to activate/deactivate the accelerometer service and listener
        static void accelerometerEnable(boolean enable) {
            Context context = (Context) PythonActivity.mActivity;
            SensorManager sm = (SensorManager) context.getSystemService(Context.SENSOR_SERVICE);
            Sensor accel = sm.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);

            if (accel == null)
                return;

            if (enable)
                sm.registerListener(accelListener, accel, SensorManager.SENSOR_DELAY_GAME);
            else
                sm.unregisterListener(accelListener, accel);
        }
    }

So we created one method named `accelerometerEnable` to activate/deactivate the
listener. And we saved the last event received in `Hardware.lastEvent`.
Now you can use it in Pyjnius::

    from time import sleep
    from jnius.reflect import autoclass

    Hardware = autoclass('org.myapp.Hardware')

    # activate the accelerometer
    Hardware.accelerometerEnable(True)

    # read it
    for i in xrange(20):

        # read the last event
        lastEvent = Hardware.lastEvent

        # we might not get any events.
        if not lastEvent:
            continue

        # show the current values!
        print lastEvent.values

        sleep(.1)

    # don't forget to deactivate it
    Hardware.accelerometerEnable(False)

You'll obtain something like this::

    [-0.0095768067985773087, 9.4235782623291016, 2.2122423648834229]
    ...

