Check User
----------

This program is used to check whether the participants have
 * an active Gitlab account
 * at least one ssh key
 * a personal repository

Open merge requests are shown with the ``-m`` option.

Usage
^^^^^

.. argparse::
   :ref: gitlab_course.checkaccounts.arg_parser
   :prog: glc_check_users
