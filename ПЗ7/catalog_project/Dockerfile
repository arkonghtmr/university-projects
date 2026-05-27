FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system django \
    && adduser --system --ingroup django django \
    && mkdir -p /data /static \
    && chown -R django:django /data /static /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=django:django . .
RUN chmod +x /app/scripts/entrypoint.sh

USER django

EXPOSE 8000

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
CMD ["gunicorn", "catalog_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
