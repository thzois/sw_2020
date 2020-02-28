import json

events = None
with open('events.json') as events_json_file:
    events = json.load(events_json_file)


navbar = ''
files = []

for i in range(1, len(events['events']) + 1):
    navbar += f'\t\t\t\t\t<li class="nav-item">\n \
\t\t\t\t\t\t<a class="nav-link js-scroll-trigger" href="./event{i}.html">Event {i}</a>\n \
\t\t\t\t\t</li>\n'
    files.append(open(f'../web-app/event{i}.html', 'w'))

with open('event_template.html') as event_template_file:
    for line in event_template_file:
        for file in files:
            file.write(line)
            if 'SWAnalytics NAV' in line:
                file.write(f'\t\t\t\t<ul class="navbar-nav ml-auto">\n {navbar} \t\t\t\t</ul>\n')