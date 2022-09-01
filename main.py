import requests
import os
from RequestPage import RequestPage
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def status():
    # url = os.environ.get("URL")
    #
    # page = RequestPage(url).connectwithsite()
    #
    # all_posts = page.find_all("div", {"data-qa": "posting PROPERTY"})
    #
    # f = open("docs/LastProperty.txt", "w")
    # for post in all_posts:
    #     price = post.find("div", {"data-qa": "POSTING_CARD_PRICE"}).get_text().strip()
    #
    #     details = post.find("div", {"data-qa": "POSTING_CARD_FEATURES"}).find_all("span")
    #     total_square_area = details[0].find("span").get_text().strip()
    #
    #     description = post.find("div", {"data-qa": "POSTING_CARD_DESCRIPTION"}).get_text().strip()
    #
    #     f.write(f"{price};{total_square_area};{description}\n")

    return jsonify({"Message": "API no ar"})


@app.route("/scrapper/imovelweb")
def imovelweb():
    try:
        url = os.environ.get("URL")

        page = RequestPage(url).connectwithsite()

        most_recent_apartments = page.find_all("div", {"data-qa": "posting PROPERTY"})

        i = 0

        while i < 10:
            bairro = most_recent_apartments[i].find("div", {"data-qa": "POSTING_CARD_LOCATION"}).get_text().strip()

            price = most_recent_apartments[i].find("div", {"data-qa": "POSTING_CARD_PRICE"}).get_text().strip()

            url = most_recent_apartments[i]["data-to-posting"]

            try:
                image = most_recent_apartments[i].find("div", {"data-qa": "POSTING_CARD_GALLERY"}).find("img")["src"]
            except TypeError:
                image = "https://divanmoveis.com.br/img/icons/404.png"

            details = most_recent_apartments[i].find("div", {"data-qa": "POSTING_CARD_FEATURES"}).find_all("span")
            total_square_area = details[0].find("span").get_text().strip()

            description = most_recent_apartments[i].find("div",
                                                         {"data-qa": "POSTING_CARD_DESCRIPTION"}).get_text().strip()

            string_to_compare = f"{price};{total_square_area};{description}"

            new = True
            f = open("docs/LastProperty.txt", "r+")
            last_twenty_apartments = f.read().split("\n")[:-1]

            for apartment in last_twenty_apartments:
                if apartment == string_to_compare:
                    new = False
                    break

            if new:
                token = os.environ.get("BOT_TOKEN")
                bot_chat_id = os.environ.get("BOT_CHAT_ID")
                bot_message = f"*Novo apartamento* \n" \
                              f"*Preço*: {price}  \n" \
                              f"*Local*: {bairro} \n" \
                              f"*Tamanho*: {total_square_area}  \n" \
                              f"*Descrição*: {description}  \n" \
                              f"[Clique aqui para visualizar o anúncio]({os.environ.get('BASE_URL')}{url}"
                send_text = 'https://api.telegram.org/bot' + token + f'/sendPhoto?photo={image}&chat_id=' + bot_chat_id + '&parse_mode=Markdown&caption=' + bot_message

                response = requests.get(send_text)

            #     f.write(string_to_compare)
            #     for apartment in last_twenty_apartments:
            #         f.write(apartment)
            #
            # f.close()
            i += 1

        return jsonify({"Message": "Processado com sucesso!"})
    except Exception as e:
        return jsonify({"Message": "Houve um erro ao processar a requisição", "Error": e})


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080)
