import telebot
import os
#import parser.py
class parse_bot():
    def __init__(self):
        plik = open(os.path.join(os.path.dirname(__file__), "TOKEN.ini"))
        TOKEN = plik.read()
        plik.close()
        self.bot = telebot.TeleBot(TOKEN)

        menu = [["Select price", "Select condition", "Select location", "Start searching"],
            ["Select min price", "Select max price", "<-----"],
            ["m Any", "m 20 zł", "m 50 zł", "m 100 zł", "m 150 zł", "m 200 zł", "m 250 zł", "m 300 zł", "m 350 zł", "<-----"], ["20 zł m", "50 zł m", "100 zł m", "150 zł m", "200 zł m", "250 zł m", "300 zł m", "350 zł m", "400 zł m", "450 zł m", "500 zł m", "550 zł m", "600 zł m", "650 zł m", "Any m", "<-----"],
            ["New", "Used", "<-----"],
            ["Warsawa",
            "Wrocław", 
            "Toruń",
            "Lublin",
            "Zielona Góra",
            "Łódź",
            "Kraków", 
            "Opole",
            "Rzeszów",
            "Białystok",
            "Gdańsk",
            "Katowice",
            "Kielce",
            "Olsztyn",
            "Poznań",
            "Szczecin",
            "Sosnowiec",
            "<-----"]]
        
        self.min_price = None
        self.max_price = None
        self.city = None

        self.markup = telebot.types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)

        @self.bot.message_handler(commands=["start"])
        def start(m):
            for row in menu[0]:
                self.markup.row(row)
            print("started")
            self.bot.send_message(m.chat.id, "Hello I can help you with finding good python book.", reply_markup=self.markup)
        
        @self.bot.message_handler(content_types=["text"])
        def respond(m):
            if m.text == "Select price":
                self.change_markup(markup=self.markup, list=menu[1], row_width=2, m=m)
            elif m.text == "Select condition":
                self.change_markup(markup=self.markup, list=menu[4], row_width=2, m=m)
            elif m.text == "Select location":
                self.change_markup(markup=self.markup,list=menu[5], row_width=3, m=m)
            elif m.text == "<-----":
                self.change_markup(markup=self.markup, list=menu[0], row_width=3, m=m)
            elif m.text == "Select min price":
                self.change_markup(markup=self.markup, list=menu[2], row_width=3, m=m)
            elif m.text == "Select max price":
                self.change_markup(markup=self.markup, list=menu[3], row_width=3, m=m)
            elif m.text == "Start searching" and self.min_price != None and self.max_price != None and self.city != None:
                pass
            else:
                self.min_price = self.set_min_price(m, menu)
                self.max_price = self.set_max_price(m, menu)
                self.city = self.set_city(m, menu)
        
        print("polling suposed to start")
        self.bot.polling()
        print("polling started")    

    def change_markup(self, markup, list, row_width, m):
        self.markup = telebot.types.ReplyKeyboardRemove()
        self.markup = telebot.types.ReplyKeyboardMarkup(row_width=row_width, one_time_keyboard=True)
        for row in list:
            self.markup.row(row)
        self.bot.send_message(m.chat.id, "Pressed succesfully", reply_markup=self.markup)


    def set_min_price(self, m, list):
        if m.text in list[2] and "m " in m.text:
            if m.text == "m Any":
                return "0 zł"
            return m.text[1:]

    def set_max_price(self, m, list):
        if m.text in list[3] and " m" in m.text:
            if m.text == "Any m":
                return "0 zł"
            return m.text[:-2]

    def set_condition(self, m, list):
        if m.text in list[4]:
            if m.text == "New":
                return "Nowe"
            elif m.text == "Used":
                return "Używane"
    def set_city(self, m, list):
        if m.text in list[5]:
            return m.text 

bot = parse_bot()