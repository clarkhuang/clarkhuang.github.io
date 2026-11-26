# Build from the repository root so the service uses the same catalogs as Pages.
FROM python:3.12-slim
WORKDIR /srv/site/integrations/reader-sync
COPY integrations/reader-sync/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY lessons.json book.json /srv/site/
COPY book/ /srv/site/book/
COPY videos/ /srv/site/videos/
COPY integrations/reader-sync/ ./
USER 65534:65534
ENV PORT=8080
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT} 'app:create_app()'"]
