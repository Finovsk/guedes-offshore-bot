## Sobre

Quanto o offshore do Guedes rendeu hoje?
Bem, agora tem um bot pra te atualizar.

## Instalação

Docker build:

```sh
docker built -t finovsk/guedes-offshore-bot .
```


## Exemplo de uso

```sh
docker run -v $(pwd):/app/ -e CONSUMER_KEY=YYY -e CONSUMER_SECRET=YYY -e KEY=YYY -e SECRET=YYY -e CREDENTIALS=YYY finovsk/guedes-offshore-bot
```
### Fontes

Cotações dólar-real antigas: http://www.yahii.com.br/dolardiario19.html

Cotação dólar-real atual: https://economia.awesomeapi.com.br/json/last/USD-BRL

Valor inicial do investimento:  USD 9.500.000,00 ~ R$ 36.665.250,00 
