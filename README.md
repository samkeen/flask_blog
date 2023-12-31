# Flask Blog

Refreshing myself on Flask
Using this
DigitalOcean [tutorial](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3)

## Setup

1. create your virtual env and activate

```bash
$ mkdir flask_blog && cd flask_blog
$ python -m venv .venv
$ source ./.venv/bin.activate
$ pip install -r requiremenst.txt


```

2. In the Db for the blog

```bash
$ python init/init_db.py
```

3. Set your app secret

```bash
$ cp dist.env .env
```

Edit `.env`, add your random secret

4. Now run the app (in debug mode)

```bash
$ flask run --debug
```

