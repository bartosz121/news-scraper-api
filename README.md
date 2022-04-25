# News Scraper API

Scrapes news using `Scrapy` every 3 hours using `Celery` and stores them in Mongo database which are served by REST API built with `Flask` and `Flask-RESTful`

List of [Scrapy spiders](https://docs.scrapy.org/en/latest/topics/spiders.html) :

- BBC
- CNN
- Fox News
- The New York Times
- The Economist
- The Washington Post
- The Wall Street Journal

## Demo
Live demo available [here](https://newsscraperapi.bartoszmagiera.me/api/v1/news)

- ### Get latest news

```bash
# api/v1/news
$ curl -s http://localhost:5000/api/v1/news | json_pp
{
   "hasNext" : true,
   "pageNumber" : 1,
   "result" : "[{\"title\": \"A California Home That Made a \\u2018Westworld\\u2019 Cameo Asks $23.5 Million\", \"source_name\": \"The Wall Street Journal\", \"source_unique_id\": \"1650903830\", \"url\": \"https://www.wsj.com/articles/a-california-home-that-made-a-westworld-cameo-asks-23-5-million-11650903830?mod=latest_headlines\", \"img_url\": \"https://images.wsj.net/im-528673?width=100&height=67\", \"created\": \"2022-04-25T19:00:32.772000\", \"id\": \"6266efd0a06562aa6b45aad2\"},
   ...
   ]"
}
```

- ### Get latest news from one source

```bash
# api/v1/news?source={source_name}
$ curl -s "http://localhost:5000/api/v1/news?source=bbc" | json_pp
{
   "hasNext" : true,
   "pageNumber" : 1,
   "result" : "[{\"title\": \"Number of US police officers murdered up by 59%\", \"source_name\": \"BBC\", \"source_unique_id\": \"61218611\", \"url\": \"https://www.bbc.com/news/world-us-canada-61218611\", \"img_url\": \"https://ichef.bbci.co.uk/news/{width}/cpsprodpb/625A/production/_124287152_gettyimages-1368414605.jpg\", \"created\": \"2022-04-25T19:00:08.555000\", \"id\": \"6266efb8a06562aa6b45aaa6\"},
   ...
   ]"
}
```

- ### Specify page number in query parameter

```bash
# api/v1/news?page={page_number}
$ curl -s "http://localhost:5000/api/v1/news?page=3" | json_pp
{
   "hasNext" : true,
   "pageNumber" : 3,
   "result" : "[{\"title\": \"Twitter board agrees to $44bn takeover by Elon Musk\", \"source_name\": \"BBC\", \"source_unique_id\": \"61222470\", \"url\": \"https://www.bbc.com/news/business-61222470\", \"img_url\": \"https://ichef.bbci.co.uk/news/{width}/cpsprodpb/83B3/production/_115651733_breaking-large-promo-nc.png\", \"description\": \"Mr Musk, who made the shock bid just over a week ago, has claimed he can \\\"unlock\\\" the social media firm's potential.\", \"created\": \"2022-04-25T19:00:05.738000\", \"id\": \"6266efb5a06562aa6b45aa7d\"},
   ...
   ]"
}
```
## Run Locally

Clone the project

```bash
  git clone https://github.com/bartosz121/news-scraper-api
```

Go to the project directory

```bash
  cd news-scraper-api
```

Create .env file

```bash
  nano .env
```

`API_KEY` can be any string, it is used to authenticate scrapy pipeline which makes POST requests to put scraped news in database

```bash
  PROD=
  PROD_MONGO_URI=
  DEV_MONGO_URI=
  API_KEY=
  PIPELINE_BASE_URL=
  CELERY_BROKER_URL=
```

Start the app

```bash
  docker-compose up -d --build
```

API will be available under port 5000

```bash
  curl http://localhost:5000/api/v1/news
```

## Run Scrapy manually

You can run scrapy spiders manually with `scrapy crawl {spider_name}` command

```bash
$ docker exec -it newsscraperapi-flask sh
  scrapy crawl bbc
```
