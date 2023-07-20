import telebot
import os
import parser
class parse_bot():
    def __init__(self, parser):
        plik = open(os.path.join(os.path.dirname(__file__), "TOKEN.ini"))
        TOKEN = plik.read()
        plik.close()
        self.bot = telebot.TeleBot(TOKEN)
        self.parser = parser

        self.main_menu = [["Select price", "Select condition", "Select location", "Start searching"],
            ["Select min price", "Select max price", "<-----"],
            ["Any", "20 zł", "50 zł", "100 zł", "150 zł", "200 zł", "250 zł", "300 zł", "350 zł", "<-----"], ["20 zł", "50 zł", "100 zł", "150 zł", "200 zł", "250 zł", "300 zł", "350 zł", "400 zł", "450 zł", "500 zł", "550 zł", "600 zł", "650 zł", "Any", "<-----"],
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
        
        self.min_price = "0 zł"
        self.max_price = "0 zł"
        self.condition = "Wszystkie"
        self.city = "Cała Polska"

        self.markup = telebot.types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)

        @self.bot.message_handler(commands=["start"])
        def start(m):
            self.change_markup(self.markup, self.main_menu[0], 3, m)
            print("started")
            mess = self.bot.send_message(m.chat.id, "Hello I can help you with finding good python book.", reply_markup=self.markup)
            print("Works??? ")
            self.bot.register_next_step_handler(mess, self.menu)
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
        self.bot.polling(none_stop = True)
        print("polling started") 

    def menu(self, m):
        print("main menu started")
        self.change_markup(self.markup, self.main_menu[0], 3, m)
        print("Works")
        if m.text == "Select price":
            mess = self.change_markup(markup=self.markup, list=self.main_menu[1], row_width=2, m=m)
            self.bot.register_next_step_handler(mess, self.price_menu)
        elif m.text == "Select location":
            mess = self.change_markup(markup=self.markup, list=self.main_menu[5], row_width=3, m=m)
            try:    
                self.bot.register_next_step_handler(mess, self.location_menu)
            except Exception as ex:
                self.bot.send_message(m.chat.id, ex)
            # elif m.text == "<-----":
            #     self.change_markup(markup=self.markup, list=self.menu[0], row_width=3, m=m)
        elif m.text == "Select condition":
            mess = self.change_markup(markup=self.markup, list=self.main_menu[4], row_width=2, m=m)                
            self.bot.register_next_step_handler(mess, self.condition_menu)
            
        elif m.text == "Start searching":
            data_list = [{"min price":self.min_price, "max price":self.max_price, "condition":self.condition, "location":self.city}]
            self.parser.find_all_on_pages(5)
            self.parser.make_a_table(self.parser.books, ["title", "url", "price", "condition", "location", "refresh time"], "parsed_data")
            self.bot.send_message(m.chat.id, f'Szukam książki od {self.min_price} do {self.max_price}, o stanie "{self.condition}" w "{self.city}".')
            print(data_list)
            columns = ["min price", "max price", "condition", "location"]
            self.parser.make_a_table(list=data_list, columns=columns, name=str(m.chat.id))

    def price_menu(self, m):
        print("price menu started")
        if m.text == "Select min price":
            mess = self.change_markup(markup=self.markup, list=self.main_menu[2], row_width=3, m=m)
            self.bot.register_next_step_handler(mess, self.min_price_menu)#, self.menu)
            return
        elif m.text == "Select max price":
            mess = self.change_markup(markup=self.markup, list=self.main_menu[3], row_width=3, m=m)
            self.bot.register_next_step_handler(mess, self.max_price_menu)
            return
        elif m.text == "<-----":
            mess = self.change_markup(markup=self.markup, list=self.main_menu[0], row_width=3, m=m)
            self.bot.register_next_step_handler(mess, self.menu)

    # def min_price_menu(self, m):
    #     if m.text == "<-----":
    #         mess = self.change_markup(markup=self.markup, list=self.main_menu[1], row_width=3, m=m)
    #         self.bot.register_next_step_handler(mess, self.price_menu)
    #     else:
    #         self.min_price = self.set_min_price(m, self.main_menu)
    #         # mess = self.change_markup(markup=self.markup, list=self.main_menu[0], row_width=3, m=m)
    #         # self.bot.register_next_step_handler(mess, self.menu)     

    def min_price_menu(self, m):
        if m.text == "<-----":
            mess = self.change_markup(markup=self.markup, list=self.main_menu[1], row_width=3, m=m)
            self.bot.register_next_step_handler(mess, self.price_menu)
        else:
            self.min_price = self.set_min_price(m, self.main_menu)
            mess = self.change_markup(markup=self.markup, list=self.main_menu[0], row_width=3, m=m)
            self.bot.register_next_step_handler(mess, self.menu)

    def max_price_menu(self, m):
        if m.text == "<-----":
            mess = self.change_markup(markup=self.markup, list=self.main_menu[1], row_width=3, m=m)
            self.bot.register_next_step_handler(mess, self.price_menu)
        else:
            self.max_price = self.set_max_price(m, self.main_menu)
            mess = self.change_markup(markup=self.markup, list=self.main_menu[0], row_width=3, m=m)
            self.bot.register_next_step_handler(mess, self.menu)

    def condition_menu(self, m):
        if m.text == "<-----":
            mess = self.change_markup(markup=self.markup, list=self.main_menu[0], row_width=3, m=m)
            self.bot.register_next_step_handler(mess, self.menu)
        else:
            self.condition = self.set_condition(m, self.main_menu)
            mess = self.change_markup(markup=self.markup, list=self.main_menu[0], row_width=3, m=m)
            self.bot.register_next_step_handler(mess, self.menu)

    def location_menu(self, m):
        if m.text == "<-----":
            mess = self.change_markup(markup=self.markup, list=self.main_menu[0], row_width=3, m=m)
            self.bot.register_next_step_handler(mess, self.menu)
        else:    
            self.city = self.set_city(m, self.main_menu)     
            mess = self.change_markup(markup=self.markup, list=self.main_menu[0], row_width=3, m=m)
            self.bot.register_next_step_handler(mess, self.menu)

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
        if m.text in list[2]:
            if m.text == "Any":
                return "0 zł"
            return m.text[1:]

    def set_max_price(self, m, list):
        if m.text in list[3]:
            if m.text == "Any":
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

parse_program = parser.parser()
bot = parse_bot(parse_program)