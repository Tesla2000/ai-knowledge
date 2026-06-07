FROM public.ecr.aws/lambda/python:3.12

WORKDIR /var/task

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dnd ./dnd_character_creator
COPY scraped_data ./scraped_data

COPY scripts/generate_schema.py ./scripts/
RUN python scripts/generate_schema.py

CMD ["dnd_character_creator.server.handler.handler"]
