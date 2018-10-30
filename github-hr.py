import datetime

import github3
from jinja2 import Environment, FileSystemLoader
from mongoengine import *

from models import Rank, User

gh = github3.login(token='token')


def record(location):
    for position, user in enumerate(list(gh.search_users(f'location:{location}')), 1):
        repositories = list(gh.repositories_by(user.login))
        forks = len(list(filter(lambda repo: repo.fork, repositories)))
        rating = Rank(datetime.datetime.now(), position, len(repositories), forks)
        try:
            user = User.objects.get(login=user.login)
            user.update(push__ratings=rating)
            user.reload()
        except DoesNotExist:
            user = User(user.login, location, [rating])
            user.save()


def generate_html(location):
    users = User.objects(location=location)
    months = {r.time.strftime('%Y-%m') for i in users for r in i.ranks}

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')
    output_from_parsed_template = template.render(users=User.objects(), months=months)

    with open(f'reports/report-{location}.html', 'w') as fh:
        fh.write(output_from_parsed_template)


if __name__ == '__main__':
    record('Cherkassy')
    generate_html('Cherkassy')
