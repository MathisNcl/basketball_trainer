FROM python:3.9-slim
WORKDIR /app
COPY api_requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY src/bball_trainer /usr/local/lib/python3.9/site-packages/bball_trainer

CMD ["uvicorn", "bball_trainer.api.main:app", "--host=0.0.0.0", "--reload"]