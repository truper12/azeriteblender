from flask_script import Manager
from app import blueprint
from app.main import create_app##, sched
from app.main.crawler.score_crawler import crawl

app = create_app()
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)

# job = sched.add_job(crawl, 'cron', second='0', minute='0', hour='1') # crawling data every 1:00 AM
# job.func()

@manager.command
def run():
    app.run()

if __name__ == '__main__':
    manager.run()