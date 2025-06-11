Check Course Configuration
--------------------------

Check if the course configuration file (see :ref:`course-configuration`) is correct.

The program fails when the number of participants exceeds the configured maximum number of participants. In that case move people to the waiting list. Similarly, it will also fail if there are people on the waiting list although the number of participants is below the maximum number of participants. Finally, the tools also checks if there are double entries in any of the lists.

Usage
^^^^^

.. argparse::
   :ref: gitlab_course.checkcourse.arg_parser
   :prog: glc_check_course
