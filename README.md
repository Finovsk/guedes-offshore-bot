## Installation

Docker build:

```sh
docker built -t finovsk/guedes-offshore-bot .
```


## Usage example

```sh
docker run -v $(pwd):/app/ -e CONSUMER_KEY=YYY -e CONSUMER_SECRET=YYY -e KEY=YYY -e SECRET=YYY finovsk/guedes-offshore-bot
```