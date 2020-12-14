import telebot

from dao.match_dao import MatchDAO
from dao.person_dao import PersonDAO, UserExistsError
from dao.ticket_dao import TicketDAO
from dao.fan_id_card_dao import FanIDCardDAO
from domain.customer import Customer
from domain.fan_id_card import FanIDCard

bot = telebot.TeleBot('1447437162:AAFlqQ_odEZvxv-qx0oJVemiFyfE3Xch0CA')


person_dao = PersonDAO()
fan_id_card_dao = FanIDCardDAO()
match_dao = MatchDAO()
ticket_dao = TicketDAO()
fan_id_card_dao = FanIDCardDAO()
is_authorized = True


@bot.message_handler(regexp='login')
def login(message):
    global is_authorized
    is_authorized = False
    sent = bot.send_message(message.chat.id, "Enter your username")
    bot.register_next_step_handler(sent, enter_username)


def enter_password(message):
    password = message.text
    if person_dao.is_password_correct(username, password):
        is_authorized = True
        global current_username, current_fan_id_card
        current_username = username
        current_fan_id_card = fan_id_card_dao.get_card_id_by_username(username)
        return
    sent = bot.send_message(message.chat.id, "The entered password is wrong. Please enter the password again")
    bot.register_next_step_handler(sent, enter_password)


@bot.message_handler(commands=["start"])
def start_message(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("Buy ticket", "Return ticket")
    user_markup.row("Follow subscription", "Cancel subscription")
    user_markup.row("Block Fan Card ID", "Unblock Fan Card ID")
    user_markup.row("Register new customer")
    user_markup.row("Add balance")
    user_markup.row("Show matches")
    bot.send_message(message.chat.id, "Choose command", reply_markup=user_markup)


@bot.message_handler(regexp="Show matches")
def show_matches(message):
    available_matches = get_available_matches()
    if available_matches is None:
        bot.send_message(message.chat.id, "No matches available")
        return
    bot.send_message(message.chat.id, available_matches)


@bot.message_handler(regexp="Register new customer")
def register_new_customer(message):
    sent = bot.send_message(message.chat.id, "Enter age")
    bot.register_next_step_handler(sent, enter_age)


def enter_age(message):
    global age
    age = message.text
    if int(age) < 12:
        bot.send_message(message.chat.id, "The age must be at least 12")
        return
    sent = bot.send_message(message.chat.id, "Enter username")
    bot.register_next_step_handler(sent, enter_username)


def enter_username(message):
    global username
    username = message.text
    if not is_authorized:
        if person_dao.does_username_exist(username):
            sent = bot.send_message(message.chat.id, "Enter password")
            bot.register_next_step_handler(sent, enter_password)
            return
        else:
            sent = bot.send_message(message.chat.id, "Username was not found in the system. Please try again")
            bot.register_next_step_handler(sent, enter_username)
            return
    sent = bot.send_message(message.chat.id, "Enter first name")
    bot.register_next_step_handler(sent, enter_first_name)


def enter_first_name(message):
    global first_name
    first_name = message.text
    sent = bot.send_message(message.chat.id, "Enter last name")
    bot.register_next_step_handler(sent, enter_last_name)


def enter_last_name(message):
    global last_name
    last_name = message.text
    generated_card_id = fan_id_card_dao.generate_next_id()
    customer = Customer(username, first_name, last_name, age, generated_card_id)
    try:
        person_dao.add_person(customer)
        fan_id_card = FanIDCard(generated_card_id, username, False)
        fan_id_card_dao.add_fan_id_card(fan_id_card)
        bot.send_message(message.chat.id,
                         "Customer {} {} was successfully created.\nUsername: {}\nPassword: {}\nFan ID "
                         "Card: {}"
                         .format(first_name, last_name, username, customer.password, generated_card_id))
    except UserExistsError as error:
        bot.send_message(message.chat.id, error)


@bot.message_handler(regexp="Buy ticket|Return ticket|Follow subscription|Cancel subscription|Block Fan Card ID|Unblock Fan Card ID|Add balance")
def enter_fan_id_message(message):
    global current_operation
    current_operation = message.text
    sent = bot.send_message(message.chat.id, "Enter Fan ID")
    bot.register_next_step_handler(sent, enter_fan_id)


def enter_fan_id(message):
    fan_id_card_id = message.text
    if not fan_id_card_id.isnumeric():
        bot.send_message(message.chat.id, "Fan ID Card must be an integer")
        return
    fan_id_card = fan_id_card_dao.get_fan_id_card(fan_id_card_id)
    if fan_id_card is None:
        bot.send_message(message.chat.id, "Fan ID Card {} was not found in the system".format(fan_id_card_id))
        return
    if fan_id_card.is_blocked and current_operation != "Unblock Fan Card ID":
        bot.send_message(message.chat.id, "Fan ID Card {} is blocked".format(fan_id_card_id))
        return
    global current_username
    global current_fan_id_card
    current_fan_id_card = fan_id_card_id
    current_username = fan_id_card_dao.get_username_by_fan_id(fan_id_card_id)
    if current_operation == "Buy ticket":
        sent = bot.send_message(message.chat.id, "Enter Match ID")
        available_matches = get_available_matches()
        if available_matches is None:
            bot.send_message(message.chat.id, "No matches are available")
            return
        bot.send_message(message.chat.id, available_matches)
        bot.register_next_step_handler(sent, enter_match_id)
    elif current_operation == "Return ticket":
        sent = bot.send_message(message.chat.id, "Choose a ticket you want to return")
        bot.send_message(message.chat.id, get_tickets_by_card_id(current_fan_id_card))
        bot.register_next_step_handler(sent, return_ticket)
    elif current_operation == "Follow subscription":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("All matches of a team")
        user_markup.row("All one stage matches")
        bot.send_message(message.chat.id, "Choose subscription type ", reply_markup=user_markup)
    elif current_operation == "Cancel subscription":
        pass
    elif current_operation == "Block Fan Card ID":
        fan_id_card_dao.block(current_fan_id_card)
        bot.send_message(message.chat.id, "Fan ID Card {} was successfully blocked".format(current_fan_id_card))
    elif current_operation == "Unblock Fan Card ID":
        fan_id_card_dao.unblock(current_fan_id_card)
        bot.send_message(message.chat.id, "Fan ID Card {} was successfully unblocked".format(current_fan_id_card))
    elif current_operation == "Add balance":
        sent = bot.send_message(message.chat.id, "Enter the amount of money in $")
        bot.register_next_step_handler(sent, add_balance)


def add_balance(message):
    value = round(float(message.text), 2)
    person_dao.add_balance(current_username, value)
    current_balance = person_dao.get_balance(current_username)
    bot.send_message(message.chat.id, "Balance was successfully increased by {} $. Right now balance equals {} $".format(value, current_balance))


@bot.message_handler(regexp="All matches of a team|All one stage matches")
def choose_subscription_type(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("Group Stage")
    user_markup.row("Quarterfinal")
    user_markup.row("Semifinal")
    user_markup.row("Final")
    bot.send_message(message.chat.id, "Choose stage type ", reply_markup=user_markup)


def enter_match_id(message):
    match_id = message.text
    match = match_dao.get_match(match_id)
    if match is None:
        bot.send_message(message.chat.id, "Match ID does not exist. Please enter match that exists")
        bot.register_next_step_handler(message.chat.id, enter_match_id)
        return
    available_seats = get_available_seats(match_id)
    if available_seats is None:
        sent = bot.send_message(message.chat.id, "No seats for this match are available. Please choose another match")
        bot.register_next_step_handler(sent, enter_match_id)
    else:
        sent = bot.send_message(message.chat.id, "Choose an available seat")
        bot.send_message(message.chat.id, available_seats)
        bot.register_next_step_handler(sent, enter_seat)


def get_available_seats(match_id):
    ticket_dao = TicketDAO()
    tickets_id_and_seats = ticket_dao.get_seats_for_match(match_id)
    result = ""
    for ticket_id_and_seat in tickets_id_and_seats:
        result += "ID: " + str(ticket_id_and_seat[0]) + "; " + str(ticket_id_and_seat[1]) + "\n"
    return result if result != "" else None


def enter_seat(message):
    ticket_id = message.text
    if not ticket_dao.does_ticket_id_exist(ticket_id):
        sent = bot.send_message(message.chat.id, "Entered seat does not exist. Please enter ticket again")
        bot.register_next_step_handler(sent, enter_seat)
        return
    balance = person_dao.get_balance(current_username)
    price = ticket_dao.get_ticket_price(ticket_id)
    if balance < price:
        sent = bot.send_message(message.chat.id, "Not enough money ({}) to pay for the seat. Please choose another seat".format(round(balance, 2)))
        bot.register_next_step_handler(sent, enter_seat)
        return
    person_dao.subtract_balance(current_username, price)
    ticket_dao.reserve_ticket(ticket_id, current_fan_id_card)
    bot.send_message(message.chat.id, "The seat was successfully reserved. Balance: {} $".format(round(balance - price, 2)))


def get_available_matches():
    match_dao = MatchDAO()
    matches = match_dao.get_matches()
    result = ""
    for match in matches:
        result += str(match) + "\n"
    return result if result != "" else None


def get_tickets_by_card_id(card_id):
    tickets = ticket_dao.get_tickets_by_card_id(card_id)
    result = ""
    for ticket in tickets:
        result += str(ticket) + "\n"
    return result


def return_ticket(message):
    ticket_id = message.text
    if not ticket_dao.does_ticket_id_exist(ticket_id):
        sent = bot.send_message(message.chat.id, "Ticket id does not exist. Please enter ticket ticket again")
        bot.register_next_step_handler(sent, return_ticket)
        return
    balance = person_dao.get_balance(current_username)
    price = ticket_dao.get_ticket_price(ticket_id)
    person_dao.add_balance(current_username, price)
    ticket_dao.return_ticket(ticket_id)
    bot.send_message(message.chat.id, "The ticket was successfully returned. Balance: {}".format(balance + price))


# @bot.message_handler(regexp="Login")
# def value_message(message):
#     keyboardV = telebot.types.InlineKeyboardMarkup()
#     kbv1 = telebot.types.InlineKeyboardButton(text="Доллар", callback_data="USD")
#     kbv2 = telebot.types.InlineKeyboardButton(text="Евро", callback_data="EUR")
#     kbv3 = telebot.types.InlineKeyboardButton(text="Фунт", callback_data="GBP")
#     keyboardV.add(kbv1, kbv2, kbv3)
#     bot.send_message(message.chat.id, "Выберите валюту: ", reply_markup=keyboardV)
#
#
# @bot.message_handler(regexp="Новости")
# def selectCounrty(message):
#     # Клавиатура выбора стран
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     kb1 = telebot.types.InlineKeyboardButton(text="Россия", callback_data="country1")
#     kb2 = telebot.types.InlineKeyboardButton(text="Германия", callback_data="country2")
#     keyboard.add(kb1, kb2)
#     bot.send_message(message.chat.id, "Список стран: ", reply_markup=keyboard)
#
#
# @bot.callback_query_handler(func=lambda c: True)
# def inline(callback):
#     print(callback.data)


bot.polling()
