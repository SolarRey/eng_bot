import requests
import telebot
from bs4 import BeautifulSoup
from fake_user_agent import user_agent

import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Good It-morning, {message.from_user.first_name} 🌞'
    bot.send_message(message.chat.id, mess)


@bot.message_handler()
def start_q(message):
    req = message.text.lower()
    req = req.replace(' ', '-')

    print(f'name={message.from_user.first_name}\n')
    print(f'message={req}\n\n')

    param = req

    ua = user_agent()
    try:
        headers = {"User-Agent": ua}
        r = requests.get('https://dictionary.cambridge.org/dictionary/english-russian/' + param, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        lista = soup.findAll(class_='def-block ddef_block')

        if lista:
            for txt in lista:
                soup = BeautifulSoup(str(txt), "lxml")
                exp = BeautifulSoup(str(soup.findAll(class_='def ddef_d db')), "lxml")
                trn = BeautifulSoup(str(soup.findAll(class_='trans dtrans dtrans-se')), "lxml")
                exm = BeautifulSoup(str(soup.findAll(class_='examp dexamp')), "lxml")
                mess = f"{exp.get_text().replace('[', '').replace(']', '')}\n\n{trn.get_text().replace('[', '').replace(']', '')}\n\n{exm.get_text().replace('[', '').replace(']', '')}\n\n"
                bot.send_message(message.chat.id, mess)
                print('\n' + mess + '\n')
        else:
            url = 'https://dictionary.cambridge.org/dictionary/english/' + param
            r = requests.get(url, headers=headers)
            if url == r.url:
                soup = BeautifulSoup(r.text, "lxml")
                lista = soup.findAll(class_='def-block ddef_block')
                for txt in lista:
                    soup = BeautifulSoup(str(txt), "lxml")
                    exp = BeautifulSoup(str(soup.findAll(class_='def ddef_d db')), "lxml")
                    trn = BeautifulSoup(str(soup.findAll(class_='trans dtrans dtrans-se')), "lxml")
                    exm = BeautifulSoup(str(soup.findAll(class_='examp dexamp')), "lxml")
                    mess = f"{exp.get_text().replace('[', '').replace(']', '')}\n\n{trn.get_text().replace('[', '').replace(']', '')}\n\n{exm.get_text().replace('[', '').replace(']', '')}\n\n"
                    bot.send_message(message.chat.id, mess)
                    print('\n' + mess + '\n')
            else:
                bot.send_message(message.chat.id, 'Такого слова не существует')
    except:
        bot.send_message(message.chat.id, 'Ошибка, попробуй еще раз')


# bot.polling(none_stop=True)
bot.infinity_polling(timeout=10, long_polling_timeout=5)
