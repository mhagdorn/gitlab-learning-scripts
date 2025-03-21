# Comments{% if session is not none %}: {{ session.title }} - {{ session.date }}{% endif %}

{% for u in users %}
## {{ u.sysID }} - {{ u.name }}
* [ ] has merge request
* [ ] has merged


{% endfor %}
