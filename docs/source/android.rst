.. _android:

Android
=======

Android has a great and extensive API to control devices, your application
etc. Some parts of the Android API are directly accessible with Pyjnius but
some of them require you to code in Java.

.. note::
    Since Android 8.0 (Oreo) the maximum limit for the local references
    previously known as "local reference table overflow" after 512 refs
    has been lifted, therefore PyJNIus can create proper Java applications
    with a lot of local references. `Android JNI tips
    <https://developer.android.com/training/articles/perf-jni>`_

Get the DPI
-----------

The `DisplayMetrics
<http://developer.android.com/reference/android/util/DisplayMetrics.html>`_
contains multiple fields that can return a lot of information about the device's
screen::

    from jnius import autoclass
    DisplayMetrics = autoclass('android.util.DisplayMetrics')
    metrics = DisplayMetrics()
    print('DPI', metrics.getDeviceDensity())

.. Note ::
  To access nested classes, use `$` e.g.
  `autoclass('android.provider.MediaStore$Images$Media')`.

Recording an audio file
-----------------------

By looking at the `Audio Capture
<http://developer.android.com/guide/topics/media/audio-capture.html>`_ guide
for Android, you can see the simple steps for recording an audio file.
Let's do it with Pyjnius::

    from jnius import autoclass
    from time import sleep

    # get the needed Java classes
    MediaRecorder = autoclass('android.media.MediaRecorder')
    AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
    OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
    AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')

    # create out recorder
    mRecorder = MediaRecorder()
    mRecorder.setAudioSource(AudioSource.MIC)
    mRecorder.setOutputFormat(OutputFormat.THREE_GPP)
    mRecorder.setOutputFile('/sdcard/testrecorder.3gp')
    mRecorder.setAudioEncoder(AudioEncoder.AMR_NB)
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

    from jnius import autoclass
    from time import sleep

    # get the MediaPlayer java class
    MediaPlayer = autoclass('android.media.MediaPlayer')

    # create our player
    mPlayer = MediaPlayer()
    mPlayer.setDataSource('/sdcard/testrecorder.3gp')
    mPlayer.prepare()

    # play
    print('duration:', mPlayer.getDuration())
    mPlayer.start()
    print('current position:', mPlayer.getCurrentPosition())
    sleep(5)

    # then after the play:
    mPlayer.release()


Accessing the Activity
----------------------

This example will show how to start a new Intent. Be careful: some Intents
require you to setup parts in the `AndroidManifest.xml` and have some
actions performed within your Activity. This is out of the scope of Pyjnius but
we'll show you what the best approach is for playing with it.

Using the Python-for-android project, you can access the default
`PythonActivity`. Let's look at an example that demonstrates the
`Intent.ACTION_VIEW`::

    from jnius import cast
    from jnius import autoclass

    # import the needed Java class
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')

    # create the intent
    intent = Intent()
    intent.setAction(Intent.ACTION_VIEW)
    intent.setData(Uri.parse('http://kivy.org'))

    # PythonActivity.mActivity is the instance of the current Activity
    # BUT, startActivity is a method from the Activity class, not from our
    # PythonActivity.
    # We need to cast our class into an activity and use it
    currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
    currentActivity.startActivity(intent)

    # The website will open.


Accelerometer access
--------------------

The accelerometer is a good example that shows how to write a little
Java code that you can access later with Pyjnius.

The `SensorManager
<http://developer.android.com/reference/android/hardware/SensorManager.html>`_
lets you access the device's sensors. To use it, you need to register a
`SensorEventListener
<http://developer.android.com/reference/android/hardware/SensorEventListener.html>`_
and overload 2 abstract methods: `onAccuracyChanged` and `onSensorChanged`.

Open your python-for-android distribution, go in the `src` directory, and
create a file `org/myapp/Hardware.java`. In this file, you will create
everything needed for accessing the accelerometer::

    package org.myapp;

    import org.kivy.android.PythonActivity;
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
    from jnius import autoclass

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
        print(lastEvent.values)

        sleep(.1)

    # don't forget to deactivate it
    Hardware.accelerometerEnable(False)

You'll obtain something like this::

    [-0.0095768067985773087, 9.4235782623291016, 2.2122423648834229]
    ...


Using TextToSpeech
------------------

Same as the audio capture, by looking at the `An introduction to Text-To-Speech in Android
<http://android-developers.blogspot.fr/2009/09/introduction-to-text-to-speech-in.html>`_ blog post, it's easy to do it with Pyjnius::

    from jnius import autoclass
    Locale = autoclass('java.util.Locale')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
    tts = TextToSpeech(PythonActivity.mActivity, None)

    # Play something in english
    tts.setLanguage(Locale.US)
    tts.speak('Hello World.', TextToSpeech.QUEUE_FLUSH, None)

    # Queue something in french
    tts.setLanguage(Locale.FRANCE)
    tts.speak('Bonjour tout le monde.', TextToSpeech.QUEUE_ADD, None)

