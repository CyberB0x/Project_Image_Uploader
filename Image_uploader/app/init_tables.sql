CREATE TABLE IF NOT EXISTS images (
        id SERIAL PRIMARY KEY,
        filename VARCHAR(255) NOT NULL,
        original_name VARCHAR(255) NOT NULL,
        size INTEGER,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        file_type VARCHAR(10)
);
