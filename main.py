import math
from RequestPage import RequestPage
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def status():
    return jsonify({"Message": "API no ar"})


@app.route("/scrapper/imovelweb")
def imovelweb():
    url = "https://www.imovelweb.com.br/apartamentos-venda-agua-verde-curitiba-bigorrilho-batel-curitiba-cabral-curitiba" \
          "-abranches-ahu-alto-da-gloria-curitiba-alto-da-xv-curitiba-bacacheri-bairro-alto-curitiba-barigui-curitiba" \
          "-barreirinha-curitiba-boa-vista-curitiba-cachoeira-curitiba-cajuru-curitiba-campina-do-siqueira-campo-comprido" \
          "-capao-raso-centro-civico-curitiba-champagnat-curitiba-ecoville-curitiba-hugo-lange-jardim-botanico-curitiba" \
          "-jardim-social-curitiba-juveve-merces-curitiba-novo-mundo-curitiba-orleans-curitiba-parque-tangua-pilarzinho" \
          "-reboucas-curitiba-santa-candida-curitiba-vila-izabel-curitiba-mais-de-2-quartos-menos-275000-reales-ordem-publicado-maior.html"

    page = RequestPage(url).connectwithsite()

    most_recent_apartment = page.find("div", {"data-qa": "posting PROPERTY"})
    price = most_recent_apartment.find("div", {"data-qa": "POSTING_CARD_PRICE"}).get_text().strip()
    # PEGAR PREÇO - ENDEREÇO E DADOS

    return jsonify({"Message": "Processado com sucesso!"})

app.run(host='0.0.0.0')
