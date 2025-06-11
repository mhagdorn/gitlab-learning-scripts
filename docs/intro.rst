Introduction
============

A collection of scripts that use the `GitLab REST API <https://docs.gitlab.com/ee/api/rest/>`__ to setup GitLab projects and repositories for a group of students. The functionality is inspired by `GitHub Classroom <https://classroom.github.com/>`__ but more light-weight without a graphical user interface. 

.. _course-configuration:

Course Configuration
--------------------
Courses are configured using a yaml file. The following entries are supported:

* ``gitlab`` the name of the gitlab server defined in python gitlab module `configuration file <https://python-gitlab.readthedocs.io/en/stable/cli-usage.html#configuration-files>`__.
* ``series`` the name of the course series, eg ``SpaceMed Digital Literacy``
* ``name`` the name of the particular course, eg ``2025``
* ``participants`` list of the participants
* ``max_participants`` (optional) maximum number of participants
* ``waiting`` (optional) list of people on waiting list
* ``cancelled`` (optional) list of people who have cancelled
* ``readme`` a `jinja2 <https://jinja.palletsprojects.com/en/stable/templates/>`__ template for the README.md file that will be put in each project
* ``sessions`` the list of sessions

  each item should have the following keys:

  * ``title`` the title of the session
  * ``date`` the the date when the session takes place
  * ``time`` the time when it takes place
  * ``place`` the locaiton where it takes place

The configuration file can contain other entries which are all passed to the templates.

Below is an example course configuration file.

.. literalinclude:: ../course.yml
   :language: yaml
