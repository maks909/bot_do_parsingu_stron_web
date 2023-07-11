import telebot
import os
#import parser.py
class parse_bot():
    def __init__(self):
        plik = open(os.path.join(os.path.dirname(__file__), "TOKEN.ini"))
        TOKEN = plik.read()
        plik.close()
        self.bot = telebot.TeleBot(TOKEN)

        self.menu = [["Select price", "Select condition", "Select location", "Start searching"],
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
        self.condition = None
        self.city = None

        self.markup = telebot.types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)

        @self.bot.message_handler(commands=["start"])
        def start(m):
            for row in self.menu[0]:
                self.markup.row(row)
            print("started")
            mess = self.bot.send_message(m.chat.id, "Hello I can help you with finding good python book.", reply_markup=self.markup)
            print("Works??? ")
            self.bot.register_next_step_handler(mess , self.menu)
            print("works") 
            
        # @self.bot.message_handler(content_types=["text"])
        # def respond(m):
        #     if m.text == "Select price":
        #         mess = self.change_markup(markup=self.markup, list=self.menu[1], row_width=2, m=m)
        #         self.bot.register_next_step_handler(mess, self.price_menu)
        #     elif m.text == "Select location":
        #         mess = self.change_markup(markup=self.markup, list=self.menu[5], row_width=3, m=m)
        #         self.bot.register_next_step_handler(mess, self.location_menu)
        #     elif m.text == "<-----":
        #         self.change_markup(markup=self.markup, list=self.menu[0], row_width=3, m=m)
        #     elif m.text == "Select condition":
        #         mess = self.change_markup(markup=self.markup, list=self.menu[4], row_width=2, m=m)
        #         self.bot.register_next_step_handler(mess, self.condition_menu)
                
        #     elif m.text == "Start searching" and self.min_price != None and self.max_price != None and self.city != None:
        #         pass
        #     else:
        #         self.city = self.set_city(m, self.menu)
        
        print("step handlers suposed to save")
        self.bot.enable_save_next_step_handlers(delay=2)
        print("step handlers saved")
        print("step handlers suposed to load")
        self.bot.load_next_step_handlers()
        print("step handlers loaded")
        print("polling suposed to start")
        self.bot.infinity_polling()
        print("polling started") 

    def menu(self, m):
        print("Works")
        if m.text == "Select price":
            mess = self.change_markup(markup=self.markup, list=self.menu[1], row_width=2, m=m)
            self.bot.register_next_step_handler(mess, self.price_menu)
        elif m.text == "Select location":
            mess = self.change_markup(markup=self.markup, list=self.menu[5], row_width=3, m=m)
            try:    
                self.bot.register_next_step_handler(mess, self.location_menu)
            except Exception as ex:
                self.bot.send_message(m.chat.id, ex)
            # elif m.text == "<-----":
            #     self.change_markup(markup=self.markup, list=self.menu[0], row_width=3, m=m)
        elif m.text == "Select condition":
            mess = self.change_markup(markup=self.markup, list=self.menu[4], row_width=2, m=m)                
            self.bot.register_next_step_handler(mess, self.condition_menu)
            
        elif m.text == "Start searching" and self.min_price != None and self.max_price != None and self.city != None:
            pass
            # else:
            #     self.city = self.set_city(m, self.menu)

    def price_menu(self, m):
        if m.text == "Select min price":
            mess = self.change_markup(markup=self.markup, list=self.menu[2], row_width=3, m=m)
            self.bot.register_next_step_handler(mess, self.min_price_self.menu)
            return
        elif m.text == "Select max price":
            mess = self.change_markup(markup=self.markup, list=self.menu[3], row_width=3, m=m)
            self.bot.register_next_step_handler(mess, self.max_price_menu)
            return

    def min_price_menu(self, m):
        self.min_price = self.set_min_price(m, self.menu)
        if m.text == "<-----":
            self.bot.register_next_step_handler(m, self.price_menu)

    def max_price_menu(self, m):
        mess = self.max_price = self.set_max_price(m, self.menu)
        if m.text == "<-----":
            self.bot.register_next_step_handler(m, self.price_menu)
    
    def condition_menu(self, m):
        self.condition = set_condition(m, self.menu)
        if m.text == "<-----":
            self.bot.register_next_step_handler(m, self.menu)

    def location_menu(self, m):
        self.city = set_city(m, self.menu)
        if m.text == "<-----":
            self.bot.register_next_step_handler(m, self.menu)

    def change_markup(self, markup, list, row_width, m):
        try:    
            self.markup = telebot.types.ReplyKeyboardRemove()
            self.markup = telebot.types.ReplyKeyboardMarkup(row_width=row_width, one_time_keyboard=True)
            for row in list:
                self.markup.row(row)
            mess = self.bot.send_message(m.chat.id, "Pressed succesfully", reply_markup=self.markup)
            return mess
        except Exception as ex:
            print("Something went wrong \n", ex)

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