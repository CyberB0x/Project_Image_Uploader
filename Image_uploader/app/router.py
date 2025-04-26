import re

from loguru import logger

from sing import SingletonMeta


class Router(metaclass=SingletonMeta):
    def __init__(self):
        self.routes = {
            'GET': {},
            'POST': {},
            'DELETE': {},
        }

    @staticmethod
    def convert_path(path):
        return re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', path)

    def add_route(self, method, path, handler):
        pattern = self.convert_path(path)
        compiled = re.compile(pattern)
        self.routes[method][compiled] = handler

    def resolve(self, method, path) -> tuple[callable, dict]:
        logger.info(f'Resolving {method} {path}')
        if method not in self.routes:
            return None, {}

        for pattern, handler in self.routes[method].items():
            match = pattern.match(path)
            if match:
                logger.info(f'Found handler for {method} {path}')
                kwargs = match.groupdict()
                return handler, kwargs
        return None, {}
