
controllerPrefix = 'controllers.'
urls = (
    '/', controllerPrefix + 'index.index',
    '/device/new', controllerPrefix + 'index.new',
    '/device/create',controllerPrefix + 'index.create',
    '/device/edit/(.*)',controllerPrefix + 'index.edit',
    '/device/delete/(.*)',controllerPrefix + 'index.delete',
        )
