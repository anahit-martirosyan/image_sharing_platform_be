from wsgiref.simple_server import make_server
from pyramid.config import Configurator

import views

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('homepage', '/')
        config.add_view(views.get_homepage, route_name='homepage')

        config.add_route('new_user_registration', '/register')
        config.add_view(views.register, route_name='new_user_registration')

        config.add_route('get_user', '/user')
        config.add_view(views.get_user, route_name='get_user')

        config.add_route('update_user', '/update_user')
        config.add_view(views.update_user, route_name='update_user', request_method='PUT')

        config.add_route('delete_user', '/delete_user')
        config.add_view(views.delete_user, route_name='delete_user', request_method='DELETE')

        # config.scan()
        users_service = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8000, users_service)
    server.serve_forever()
