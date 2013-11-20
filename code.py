import web
from config.url import urls


app = web.application(urls,globals(),True)

config = web.storage(
	email = 'lenyemeng@anjukeinc.com',
	site_name = 'AMDC -- Anjuke Mobile Data Center',
	site_desc = 'Data Will Give You Truth!',
	static = '/static',
	)

render = web.template.render("templates",base="layout")
web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render


if __name__ == "__main__":
    app.run()
