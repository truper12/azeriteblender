from flask_script import Manager
from app import blueprint
from app.main import create_app, sched
from app.main.crawler.score_crawler import crawl

app = create_app()
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)

# sched.add_job(crawl, 'interval', seconds = 3)
sched.add_job(crawl, 'cron', second='0', minute='17', hour='19')

@manager.command
def run():
    app.run()

if __name__ == '__main__':
    manager.run()