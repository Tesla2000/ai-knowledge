## Running

You can run script with docker or python

### Python
```shell
python main.py --config_file src/{project_name_low}/config_sample.toml
```

### Cmd
```shell
poetry install
poetry run {project_name_low}
```

### Docker
```shell
docker build -t {docker_image_name} .
docker run -it {docker_image_name} /bin/sh
python main.py
```
