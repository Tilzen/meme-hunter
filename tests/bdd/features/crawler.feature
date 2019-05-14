# language:pt

Funcionalidade: Contagem de Muertes e Arribas
  Eu, como usuário, quero que haja uma filtragem nos memes que vão ser baixados
  através da quantidade de Arribas e Muertes.

  Cenário: Mais Muertes
    Dado um numero de muertes
    Quando ele for superior ao número de arribas
    Então o meme é ignorado

  Cenário: Mais Arribas
    Dado um numero de arribas
    Quando ele for superior ao número de muertes
    Então o meme é baixado

  Cenário: Menos de 300 Arribas
    Dado um numero de arribas
    Quando ele for inferior à 300
    Então o meme é ignorado

  Cenário: Mais de 300 Arribas
    Dado um numero de arribas
    Quando ele for superior à 300
    Então verificar se o número de arribas é superior ao de muertes
