Send Email
--------------

This program fills in a `jinja2 <https://jinja.palletsprojects.com/en/stable/templates/>`__ template and constructs an email message. 
You can select the group of people you want to send the email to.
The organiser always gets a copy. 
The email is sent when a mail server is specified.
Otherwise it is simply printed on screen.

All variables defined in the :ref:`course-configuration` file are passed to the template.
The session number is passed by the variable ``snr``.

The list of participants is passed to the template if it contains a varaible ``users``.
The list of users contains objects of type :py:class:`gitlab_course.GLCUser`.

Usage
^^^^^

.. argparse::
   :ref: gitlab_course.send_email.arg_parser
   :prog: glc_send_email
