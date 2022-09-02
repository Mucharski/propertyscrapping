import requests
import os
from RequestPage import RequestPage
from flask import Flask, jsonify
from dotenv import load_dotenv

from TelegramBot import TelegramBot

load_dotenv()

app = Flask(__name__)


@app.route("/")
def status():
    return jsonify({"Message": "API no ar"})

@app.route("/function/trigger")
def azureFunctionTrigger():
    bot_message = f"Trigger efetuado"
    send_text = 'https://api.telegram.org/bot' + os.environ.get("BOT_TOKEN") + f'/sendMessage?chat_id=1257871706&parse_mode=Markdown&text=' + bot_message

    requests.get(send_text)

    return jsonify({"Message": "Processado com sucesso!"})

@app.route("/scrapper/imovelweb")
def imovelweb():
    try:
        url = os.environ.get("URL")

        page = RequestPage(url).connectwithsite()

        most_recent_apartments = page.find_all("div", {"data-qa": "posting PROPERTY"})

        i = 0

        while i < 10:
            neighborhood = most_recent_apartments[i].find("div",
                                                          {"data-qa": "POSTING_CARD_LOCATION"}).get_text().strip()

            price = most_recent_apartments[i].find("div", {"data-qa": "POSTING_CARD_PRICE"}).get_text().strip()

            url = most_recent_apartments[i]["data-to-posting"]

            try:
                image = most_recent_apartments[i].find("div", {"data-qa": "POSTING_CARD_GALLERY"}).find("img")["src"]
            except TypeError:
                image = "https://cdn-icons-png.flaticon.com/512/1695/1695213.png"

            details = most_recent_apartments[i].find("div", {"data-qa": "POSTING_CARD_FEATURES"}).find_all("span")
            total_square_area = details[0].find("span").get_text().strip()

            description = most_recent_apartments[i].find("div",
                                                         {"data-qa": "POSTING_CARD_DESCRIPTION"}).get_text().strip()

            string_to_compare = f"{price};{total_square_area};{description}"

            new = True
            f = open("docs/LastProperty.txt", "r")
            last_twenty_apartments = f.read().split("\n")[:-1]  # SEMPRE TEM UMA LINHA EM BRANCO NO FINAL, NÃO PEGO ELA
            f.close()

            for apartment in last_twenty_apartments:
                if apartment == string_to_compare:
                    new = False
                    break

            if new:
                bot = TelegramBot(os.environ.get("BOT_TOKEN"), os.environ.get("BOT_CHAT_ID"))

                bot_message = f"*Novo apartamento* \n" \
                              f"*Preço*: {price}  \n" \
                              f"*Local*: {neighborhood} \n" \
                              f"*Tamanho*: {total_square_area}  \n" \
                              f"*Descrição*: {description}  \n" \
                              f"[Clique aqui para visualizar o anúncio]({os.environ.get('BASE_URL')}{url}"

                requests.get(bot.sendMessage(bot_message, image))

                last_twenty_apartments.insert(0, string_to_compare)
                last_twenty_apartments.pop()

                f = open("docs/LastProperty.txt", "w").close()  # LIMPA O ARQUIVO

                f = open("docs/LastProperty.txt", "a")

                for apartment in last_twenty_apartments:
                    f.write(f"{apartment}\n")

                f.close()

            i += 1

        return jsonify({"Message": "Processado com sucesso!"})
    except Exception as e:
        bot = TelegramBot(os.environ.get("BOT_TOKEN"), os.environ.get("BOT_CHAT_ID"))

        informations = {"QtdApartamentos": len(most_recent_apartments)}

        requests.get(bot.sendError(str(informations)))

        f = open("docs/errorslogs.txt", "a")
        f.write(str(e) + "\n" + str(informations))
        f.close()

        return jsonify({"Message": "Houve um erro ao processar a requisição", "Error": {"QtdApartamentos": len(most_recent_apartments)}})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
