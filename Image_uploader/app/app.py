from http.server import HTTPServer

from loguru import logger

from ImageHosting import ImageHostingHttpRequestHandler
from settings import SERVER_ADDRESS


def run(server_class=HTTPServer, handler_class=ImageHostingHttpRequestHandler):
    httpd = server_class(SERVER_ADDRESS, handler_class)
    logger.info(f'Serving on http://{SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.warning('Keyboard interrupt received, exiting.')
        httpd.server_close()
    finally:
        logger.info('Server stopped.')


if __name__ == '__main__':
    run()
