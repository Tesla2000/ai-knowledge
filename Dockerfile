FROM public.ecr.aws/lambda/python:3.12

WORKDIR /var/task

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dnd ./dnd_character_creator
RUN ln -s /var/task/dnd_character_creator /var/task/dnd
COPY scraped_data ./scraped_data


CMD ["dnd_character_creator.server.handler.handler"]
