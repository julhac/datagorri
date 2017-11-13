from datagorri.controller import Controller


class Router:
    def __init__(self, content_frame, routes=None):
        self._current_route = ''
        self._routes = {}
        self._content_frame = content_frame
        if routes is not None:
            self.add_routes(routes)

    def route(self, name):
        if self._current_route == name:
            return self

        controller = self.get_route(name)['controller']
        view = self.get_route(name)['view']
        controller.on_route(view, self._content_frame)

        self._current_route = name

        return self

    def add_route(self, name, to):
        if 'controller' not in to:
            raise ValueError('No controller defined for route:' + name)

        if 'view' not in to:
            raise ValueError('No view defined for route:' + name)

        if not isinstance(to['controller'], Controller):
            raise ValueError('The defined controller for the route "' + name + '" is no child class of Controller')

        self._routes[name] = to

        return self

    def add_routes(self, routes):
        if not isinstance(routes, dict):
            raise TypeError('Routes need to be a dict!')

        for name, controller in routes.items():
            self.add_route(name, controller)

        return self

    def get_routes(self):
        return self._routes

    def get_route(self, name):
        if name not in self._routes:
            raise KeyError('Unknown route "' + name + '"')

        return self._routes[name]

    def has_route(self, name):
        return name not in self._routes
