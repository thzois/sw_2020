import json

# read events.json 
def read_events():
    with open("events.json", "r") as read_file:
        return json.load(read_file)


def generate_html(events):
    navbars = []
    files = []
    
    for i in range(1, len(events['events']) + 1):
        nav = ''
        for j in range(1, len(events['events']) + 1):
            if i == j:
                # add style=color: white (active page)
                nav += f'\t\t\t\t\t<li class="nav-item">\n \
\t\t\t\t\t\t<a class="nav-link js-scroll-trigger" href="./event{j}.html" style="color: white">Event {j}</a>\n \
\t\t\t\t\t</li>\n'
            else:
                nav += f'\t\t\t\t\t<li class="nav-item">\n \
\t\t\t\t\t\t<a class="nav-link js-scroll-trigger" href="./event{j}.html">Event {j}</a>\n \
\t\t\t\t\t</li>\n'

        navbars.append(nav)
        files.append(open(f'../web-app/event{i}.html', 'w'))

    with open('event_template.html') as event_template_file:
        for line in event_template_file:
            nav_idx = 0
            for file in files:
                file.write(line)
                if 'SWAnalytics NAV' in line:
                    file.write(f'\t\t\t\t<ul class="navbar-nav ml-auto">\n {navbars[nav_idx]} \t\t\t\t</ul>\n')
                nav_idx += 1


def main():
    events = read_events()
    generate_html(events)


if __name__ == "__main__":
    main()