import json

events = None
with open('events.json') as events_json_file:
    events = json.load(events_json_file)


navbar = ''
files = []

for i in range(1, len(events['events']) + 1):
    navbar += f'<li class="nav-item">  <a class="nav-link js-scroll-trigger" href="./event{i}.html" style="color:white">Event {i}</a> </li>'
    files.append(open(f'event{i}.html', 'w'))

with open('event_template.html') as event_template_file:
    for line in event_template_file:
        for file in files:
            file.write(line)
            if 'SWAnalytics NAV' in line:
                file.write(
                    f'\n <ul class="navbar-nav ml-auto">  {navbar}   </ul>')