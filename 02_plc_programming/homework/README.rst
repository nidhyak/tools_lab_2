===============
PLC Programming
===============

:Group 11:
   - Leonard Tan Chin Leong
   - Muzammil Muhammad 
   - Edison Koo

.. contents::

.. sectnum::

Exercise 01
===========

Source
------

::

   /* Exercise 01

   If DI_01 is pressed, the button DO_05 will light up if it is not originally lit
   up and turn off if it is lit up.

   */

   IF S:FS THEN
       DO_05 := 0;
       Counter := 0;
   END_IF;

   CASE Counter OF
       0:
           IF DI_01 THEN                   // Button pressed
               DO_05 := NOT DO_05;         // Toggle light
               Counter := 1;
           END_IF;
       1:
           IF NOT DI_01 THEN               // Button released
               Counter := 0;               // Reset counter
           END_IF;
   END_CASE;


Result
------

   .. image:: images/ex01.png

Exercise 02
===========

Source
------

::

   /* Exercise 02

   If DI_02 is pressed, followed by DI_03 is pressed, the button DO_02 and DO_05
   will light up if it is not originally lit up and turn off if it is lit up.

   */

   IF S:FS THEN
       DO_02 := 0;
       DO_05 := 0;
       Counter := 0;
   END_IF;

   CASE Counter OF
       0:                                  // No buttons pressed
           IF DI_02 AND NOT DI_03 THEN     // Only first button pressed
               Counter := 1;
           END_IF;
       1:
           IF DI_02 AND DI_03 THEN         // Both buttons pressed
               DO_02 := NOT DO_02;         // Toggle lights
               DO_05 := NOT DO_05;
               Counter := 0;               // Reset counter
           ELSIF DI_02 THEN                // First button held
               Counter := 1;
           ELSE                            // No buttons pressed
               Counter := 0;
           END_IF;
   END_CASE;

Result
------

   .. image:: images/ex02.png

Exercise 03
===========

Source
------

::

   /* Exercise 03

   Push DI_04 four times and DO_02 will light up and DO_02 will stay on till DI_04
   is pushed for the fifth time.

   */

   IF S:FS THEN
       DO_02 := 0;
       Counter := 0;
   END_IF;

   CASE Counter OF
       0, 2, 4, 6, 8:
           IF DI_04 THEN                   // Button pressed
               Counter := Counter + 1;
           END_IF;
       1, 3, 5:
           IF NOT DI_04 THEN               // Button released
               Counter := Counter + 1;
           END_IF;
       7:
           DO_02 := 1;                     // 4th press turns on light
           IF NOT DI_04 THEN               // Button released
               Counter := Counter + 1;
           END_IF;
       9:
           DO_02 := 0;                     // 5th press turns off light
           IF NOT DI_04 THEN               // Button released
               Counter := 0;               // Reset state
           END_IF;
   END_CASE;

Result
------

   .. image:: images/ex03.png

Exercise 04
===========

Source
------

::

   /* Exercise 04

   Push DI_06, and DO_05 will remain lighted up for three seconds and will go off.

   */

   IF S:FS THEN
       DO_05 := 0;
       Counter := 0;                       // state tracking
   END_IF;

   CASE Counter OF
       0:                                  // wait for button press
           DO_05 := 0;                     // light off
           IF DI_06 THEN                   // button pressed
               Counter := 1;
           END_IF;
       1:
           DO_05 := 1;                     // light on
           TON.PRE := 3000;                // milliseconds
           TON.TimerEnable := 1;           // start timer
           TONR(TON);
           IF TON.DN THEN                  // timer done
               TON.TimerEnable := 0;       // stop timer
               TONR(TON);
               Counter := 0;               // reset state
           END_IF;
   END_CASE;

Result
------

   .. image:: images/ex04.png

Exercise 05
===========

Source
------

::

   /* Exercise 05

   If the temperature sensor reads above 30 degrees, DO_02 and DO_10 buttons will
   light up.

   */

   IF S:FS THEN
       ThresTemp := 30.0;
   END_IF;

   DO_02 := Temp1 > ThresTemp;
   DO_10 := Temp1 > ThresTemp;

Result
------

   .. image:: images/ex05.png
