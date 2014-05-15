import web
from config.url import urls
from models.models import load_sqla



app = web.application(urls,globals(),True)
app.add_processor(load_sqla)

config = web.storage(
	email = 'lenyemeng@anjukeinc.com',
	site_name = 'ITOOLS',
	site_desc = 'Easier, Faster!',
	static = '/static',
	)

render = web.template.render("templates",base="layout")
web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render
web.config.debug = True


if __name__ == "__main__":
    app.run()
