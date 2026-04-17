FROM python:3.12-alpine AS builder

WORKDIR /src

COPY mkdocs.yml README.md ./
COPY docs ./docs

RUN pip install --no-cache-dir mkdocs==1.6.1 \
    && mkdocs build --clean --site-dir /site

FROM nginx:1.27-alpine

COPY --from=builder /site /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]