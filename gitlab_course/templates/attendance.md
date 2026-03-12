# Attendance {{ session.date }} - {{ session.title }}

{% for u in users | sort(attribute='sysID') -%}
* [ ] {{u.sysID }}: {{ u.name }}
{% endfor %}