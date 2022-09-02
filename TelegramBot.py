class TelegramBot:
    def __init__(self, token, bot_chat_id):
        self.token = token
        self.bot_chat_id = bot_chat_id

    def sendMessage(self, bot_message, image):
        send_text = 'https://api.telegram.org/bot' + self.token + f'/sendPhoto?photo={image}&chat_id=' + self.bot_chat_id + '&parse_mode=Markdown&caption=' + bot_message

        return send_text

    def sendError(self, informations):
        bot_message = f"Ocorreu um erro ao enviar as informações.\nConfira o log de erros.\n{informations}"
        send_text = 'https://api.telegram.org/bot' + self.token + f'/sendMessage?chat_id=1257871706&parse_mode=Markdown&text=' + bot_message

        return send_text