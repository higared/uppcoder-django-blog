# Django 博客 Starter

一个最小可跑的 Django 博客：文章列表、文章详情、Django 后台写文章。
按 Uppcoder 官方 `django-postgresql-starter` 的口径写：数据库从环境变量来，
没有 `POSTGRES_*` 就用本地 SQLite；HTTPS 代理的设置已配好，后台登录不会报
`403 Origin checking failed`。

## 能干什么

- 首页 `/`：已发布文章列表（标题、摘要、时间）
- 详情页 `/post/<slug>/`：正文按段落显示
- 后台 `/admin/`：登录后写文章、改文章、上下架（`is_published`）
- 写文章时 slug 留空也行：英文标题自动生成，中文标题保存后自动变成 `post-<id>`

## 本地运行

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata sample_posts   # 导入 3 篇示例文章（可选）
python manage.py runserver
```

打开 http://127.0.0.1:8000/ 看首页，http://127.0.0.1:8000/admin/ 进后台。
本地默认用 SQLite（`db.sqlite3`，已在 `.gitignore` 里，不提交）。

想改配置，复制 `.env.example` 成 `.env` 再改（本地开发时手动读环境变量，
不用额外装 `python-dotenv`；Uppcoder 上直接在平台填变量，不用这个文件）。

## 部署到 Uppcoder Spark（免费版）

先确认：Uppcoder 免费版（Spark）同时只能跑 **1 个应用 + 1 个数据库**，
每天 500 CPU 秒，2GB 内存、2GB 磁盘。这个博客是轻量应用，低流量够用，
别拿它跑爬虫、回测、转码。

**截图里两个 Django 模板选哪一个：选上面那个 `Django + PostgreSQL starter`。**
不要选 `Django Full Stack`——它多了一个 pgAdmin，多占内存和 CPU，
小白博客用不上，免费版上反而更吃力。

步骤：

1. 注册并验证邮箱，Billing → Available Plans → Spark → Start free。
2. Stacks → Create → From a template，搜 `django`，选
   **Django + PostgreSQL starter**。
3. 在 Django 卡片上填管理员用户名、密码、邮箱；把这个项目的 Git 仓库地址
   填到 Django 卡片的 Git repository 里（先把这个文件夹推到你自己的
   GitHub/GitLab 仓库，分支 `main`），然后 Deploy。
   Uppcoder 会自动配好 `POSTGRES_*`，装好 PostgreSQL 驱动。
4. 部署好后，在 Stack 页面的 Web Terminal 里跑（Uppcoder 的 Python 环境
   是 pixi 的，直接用 `python` 会找不到 Django）：

```bash
pixi run -e web-django python manage.py migrate
pixi run -e web-django python manage.py createsuperuser --noinput
pixi run -e web-django python manage.py loaddata sample_posts
```

`createsuperuser --noinput` 用的是第 3 步在卡片上填的管理员账号。
`loaddata` 是可选的，只用来导入 3 篇示例文章，之后在后台删掉就行。

5. 打开应用自己的 HTTPS 地址看首页，`/admin/` 进后台写文章。
   想让别人访问，把页面顶部的 Private 切换成 Public。

## 项目结构

```
manage.py
requirements.txt          # Django / psycopg / gunicorn（没有 whitenoise）
mysite/
  settings.py             # 环境变量配数据库 + HTTPS 代理设置
  urls.py / wsgi.py / asgi.py
blog/
  models.py               # Post：标题、slug、摘要、正文、是否发布
  admin.py / views.py / urls.py
  migrations/0001_initial.py
  fixtures/sample_posts.json   # 3 篇示例文章
  templates/blog/         # base / post_list / post_detail，无外部 CDN
```

## 常见问题

- **后台登录 403**：一般是 `CSRF_TRUSTED_ORIGINS` 没配。Uppcoder 上
  `settings.py` 会从 `UPPCODER_SELF_URL` 自动取应用地址，不用手动改；
  如果换了自定义域名，把域名加进 `CSRF_TRUSTED_ORIGINS` 环境变量。
- **部署后首页是空的**：正常，数据库是空的。去后台写一篇，或跑
  `loaddata sample_posts` 导入示例。
- **中文标题的 slug 是空的**：保存时自动变成 `post-<id>`，不影响访问。
- **部署后 502（v2 已修）**：v1 用了 `whitenoise`，但 Uppcoder 的 pixi
  环境里没装它，启动时报 `ModuleNotFoundError: No module named 'whitenoise'`
  就直接崩了。v2 已去掉 whitenoise，项目名也从 `config` 改回官方默认的
  `mysite`（生产启动命令是 `gunicorn mysite.wsgi:application`）。
