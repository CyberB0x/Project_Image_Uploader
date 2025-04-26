import os
from uuid import uuid4

from loguru import logger

from database_manager import DBManager
from http_request_handler import AdvancedHTTPRequestHandler
from settings import IMAGES_PATH, \
    ALLOWED_EXTENSIONS, MAX_FILE_SIZE, ERROR_FILE, PAGE_LIMIT


class ImageHostingHttpRequestHandler(AdvancedHTTPRequestHandler):
    server_version = 'Image Hosting Server v0.1'

    def get_images_count(self) -> None:
        count = DBManager().execute_fetch_query('SELECT COUNT(*) FROM images;')[0][0]
        logger.info('Count: ' + str(count))
        self.send_json({
            'count': count
        })

    def get_images(self) -> None:
        page = self.headers.get('Page')
        logger.info(f'Page: {page}')
        query = (f"SELECT * FROM images ORDER BY upload_time DESC"
                 f" LIMIT {PAGE_LIMIT} OFFSET {(int(page) - 1) * PAGE_LIMIT};")
        logger.info(f'Query: {query}')
        images = DBManager().execute_fetch_query(query)
        if not images:
            return self.send_json({'images': []})

        to_json_images = []
        for image in images:
            to_json_images.append({
                'filename': image[1],
                'original_name': image[2],
                'size': image[3],
                'upload_time': image[4].strftime('%Y-%m-%d %H:%M:%s'),
                'file_type': image[5]
            })
        self.send_json({
            'images': to_json_images
            # next(os.walk(IMAGES_PATH))[2]
        })

    def post_upload(self) -> None:
        length = int(self.headers.get('Content-Length'))
        if length > MAX_FILE_SIZE:
            logger.warning('File too large')
            self.send_html(ERROR_FILE, 413)
            return

        data = self.rfile.read(length)
        orig_filename = self.headers.get('Filename')
        _, ext = os.path.splitext(orig_filename)
        image_id = uuid4()
        if ext not in ALLOWED_EXTENSIONS:
            logger.warning('File type not allowed')
            self.send_html(ERROR_FILE, 400)
            return
        DBManager().execute_query(
            f"INSERT INTO images (filename, original_name, size, file_type) "
            f"VALUES ('{image_id}', '{orig_filename}',"
            f" {length}, '{ext}');"
        )
        with open(IMAGES_PATH + f'{image_id}{ext}', 'wb') as file:
            file.write(data)
        self.send_html('upload_success.html', headers={
            'Location': f'http://localhost/{IMAGES_PATH}{image_id}{ext}'})

    def delete_image(self, image_id) -> None:
        full_filename = image_id
        if not full_filename:
            logger.warning('No filename provided')
            self.send_html(ERROR_FILE, 404)
            return

        filename, _ = os.path.splitext(full_filename)
        image_path = IMAGES_PATH + full_filename
        if not os.path.exists(image_path):
            logger.warning('Image not found')
            self.send_html(ERROR_FILE, 404)
            return

        os.remove(image_path)
        DBManager().execute_query(f"DELETE FROM images WHERE filename = '{filename}';")
        self.send_json({'Success': 'Image deleted'})
