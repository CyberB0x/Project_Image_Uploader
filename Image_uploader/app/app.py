from http.server import HTTPServer

from loguru import logger

from DBManager import DBManager
from ImageHostingHandler import ImageHostingHttpRequestHandler
from Router import Router
from settings import SERVER_ADDRESS


def run(server_class=HTTPServer, handler_class=ImageHostingHttpRequestHandler):
    DBManager().init_tables()
    router = Router()
    router.add_route('GET', '/api/images/', handler_class.get_images)
    router.add_route('GET', '/api/images_count/', handler_class.get_images_count)
    router.add_route('POST', '/upload/', handler_class.post_upload)
    router.add_route('DELETE', '/api/delete/<image_id>', handler_class.delete_image)

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
