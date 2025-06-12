Apply Template
--------------

This program is used to fill in a `jinja2 <https://jinja.palletsprojects.com/en/stable/templates/>`__ template.
All variables defined in the :ref:`course-configuration` file are passed to the template.
The session number is passed by the variable ``snr``.

The list of participants is passed to the template if it contains a varaible ``users``.
The list of users contains objects of type :py:class:`gitlab_course.GLCUser`.

Usage
^^^^^

.. argparse::
   :ref: gitlab_course.apply_template.arg_parser
   :prog: glc_apply_template
