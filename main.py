import telebot

from dao.match_dao import MatchDAO
from dao.person_dao import PersonDAO
from dao.ticket_dao import TicketDAO
from domain.cashier import Cashier, UserAlreadyExistsError, IncorrectInputFormat
from domain.customer import Customer
from domain.fan_id_card import NotEnoughMoneyError
from domain.match import Match
from domain.organizer import Organizer
from domain.seat import Seat
from domain.ticket import SingleTicket, Ticket

bot = telebot.TeleBot('1447437162:AAFlqQ_odEZvxv-qx0oJVemiFyfE3Xch0CA')


class CurrentUser:
    def __init__(self):
        self.authenticated = False
        self.username = self.password = self.operation = self.role = self.person = None


class NewCustomer:
    def __init__(self):
        self.username = self.age = self.first_name = self.last_name = None


class NewMatch:
    def __init__(self):
        self.host_team = self.guest_team = self.date = self.match_type = None


user = CurrentUser()
new_customer = None
new_match = None
match = None


def send(message, text, next_handler=None):
    sent = bot.send_message(message.chat.id, text)
    if next_handler is not None:
        bot.register_next_step_handler(sent, next_handler)


@bot.message_handler(commands=["start"], regexp="start")
def show(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    if not user.authenticated:
        user_markup.row("Login")
    else:
        if user.role == "customer":
            user_markup.row("Show tickets")
            user_markup.row("Add balance")
            user_markup.row("Buy ticket", "Return ticket")
        elif user.role == "cashier":
            user_markup.row("Register new customer")
            user_markup.row("Block Fan ID Card", "Unblock Fan ID Card")
        elif user.role == "organizer":
            user_markup.row("Add match", "Update match")
            user_markup.row("Delete match", "Cancel match")
        user_markup.row("My credentials")
        user_markup.row("Logout")
    user_markup.row("Show matches")
    bot.send_message(message.chat.id, "Choose command", reply_markup=user_markup)


@bot.message_handler(regexp="Show matches")
def show_matches(message):
    result = MatchDAO.get_matches()
    matches = ""
    for row in result:
        matches += str(Match(*row)) + "\n"
    send(message, matches)


@bot.message_handler(regexp="My credentials")
def show_credentials(message):
    send(message, str(user.person))


@bot.message_handler(regexp="Logout")
def logout(message):
    user.authenticated = False
    user.role = ""
    send(message, "You have been logged out")


@bot.message_handler(regexp="Login")
def login(message):
    if not user.authenticated:
        send(message, "Enter your username", enter_username)


def enter_username(message):
    username = message.text
    if PersonDAO.does_exist(username):
        user.username = username
        send(message, "Enter your password", enter_password)
    else:
        send(message, "The username does not exist")


def enter_password(message):
    password = message.text
    if PersonDAO.is_password_correct(user.username, password):
        user.password = password
        user.authenticated = True
        user.role = PersonDAO.get_role_by_username(user.username)
        if user.role == "customer":
            user.person = Customer.construct(user.username)
        elif user.role == "cashier":
            user.person = Cashier.construct(user.username)
        elif user.role == "organizer":
            user.person = Organizer.construct(user.username)
        send(message, "You have been successfully logged in as {} {} {}".format(user.role, user.person.first_name, user.person.last_name), show)
    else:
        send(message, "The entered password is wrong. You can try to sign in again")

# customer

@bot.message_handler(regexp="Show tickets")
def show_tickets(message):
    if user.role == "customer":
        card_id = user.person.fan_id_card
        result = TicketDAO.get_tickets_id_by_card_id(card_id.id)
        tickets = ""
        for row in result:
            ticket_id = row[0]
            tickets += str(SingleTicket.construct(ticket_id)) + "\n--------------\n"
        send(message, tickets if tickets != "" else "You do not have any tickets")


@bot.message_handler(regexp="Add balance")
def add_balance(message):
    if user.role == "customer":
        if user.person.is_blocked():
            send(message, "Your Fan ID Card is blocked")
        else:
            send(message, "Your current balance: ${}\nEnter the value you would like to increase your balance".format(user.person.fan_id_card.balance), enter_value)


def enter_value(message):
    value = round(float(message.text), 2)
    user.person.increase_balance(value)
    send(message, "Your balance was increased and now equals ${}".format(user.person.fan_id_card.balance))


@bot.message_handler(regexp="Buy ticket")
def buy_ticket(message):
    if user.role == "customer":
        if user.person.is_blocked():
            send(message, "Your Fan ID Card is blocked")
        else:
            send(message, "Enter match ID you would like to attend", enter_match_id_to_buy_ticket)


def enter_match_id_to_buy_ticket(message):
    global match_id
    match_id = int(message.text)
    available_seats = get_available_seats(match_id)
    if available_seats == "":
        send(message, "There are no available seats for this match. Please choose another match", enter_match_id_to_buy_ticket)
        return
    send(message, "Choose an available seat for this match. Your balance: ${}".format(user.person.fan_id_card.balance))
    send(message, available_seats, choose_seat)


def choose_seat(message):
    ticket_id = int(message.text)
    ticket = SingleTicket.construct(ticket_id)
    try:
        user.person.buy_ticket(ticket)
        send(message, "The seat and ticket were successfully reserved. Balance: ${}".format(user.person.fan_id_card.balance))
    except NotEnoughMoneyError as error:
        send(message, str(error) + ". Please enter another seat", choose_seat)


def get_available_seats(match_id):
    result = TicketDAO.get_available_tickets_id_and_seats_and_price(match_id)
    tickets_id_and_seats_and_prices = ""
    for row in result:
        tickets_id_and_seats_and_prices += str(row[0]) + ": " + str(Seat(row[1], row[2], row[3])) + ". Price: ${}\n".format(row[4])
    return tickets_id_and_seats_and_prices


@bot.message_handler(regexp="Return ticket")
def return_ticket(message):
    if user.role == "customer":
        if user.person.is_blocked():
            send(message, "Your Fan ID Card is blocked")
        else:
            send(message, "Enter ticket ID you would like to return", enter_ticket_id_to_return)


def enter_ticket_id_to_return(message):
    ticket_id = int(message.text)
    ticket = SingleTicket.construct(ticket_id)
    user.person.return_ticket(ticket)
    send(message, "Ticket {} was successfully returned. Balance: ${}".format(ticket_id, user.person.fan_id_card.balance))


# cashier

@bot.message_handler(regexp="Register new customer")
def register_new_customer(message):
    if user.role == "cashier":
        global new_customer
        new_customer = NewCustomer()
        send(message, "Enter username", enter_new_username)


def enter_new_username(message):
    new_customer.username = message.text
    send(message, "Enter age", enter_age)


def enter_age(message):
    try:
        new_customer.age = int(message.text)
        if new_customer.age < 12:
            send(message, "The minimum age must be at least 12")
        else:
            send(message, "Enter first name", enter_first_name)
    except ValueError:
        send(message, "Age must be an integer. Please enter the age again in the correct format", enter_age)


def enter_first_name(message):
    new_customer.first_name = message.text
    send(message, "Enter last name", enter_last_name)


def enter_last_name(message):
    new_customer.last_name = message.text
    customer = Customer(new_customer.username, new_customer.first_name, new_customer.last_name, new_customer.age, None)
    try:
        user.person.register(customer)
        send(message, "The customer was successfully registered".format(customer.username))
        send(message, "Username: {}\nPassword: {}".format(customer.username, customer.password))
    except IncorrectInputFormat as error:
        send(message, error)
    except UserAlreadyExistsError as error:
        send(message, error)


@bot.message_handler(regexp="Unblock Fan ID Card")
def block_fan_id_card(message):
    if user.role == "cashier":
        send(message, "Enter Fan ID Card holder's username you would like to unblock", enter_username_to_unblock)


def enter_username_to_unblock(message):
    username = message.text
    customer = Customer.construct(username)
    user.person.unblock_fan_id_card(customer)
    send(message, "The Fan ID Card {} was successfully unblocked".format(customer.fan_id_card.id))


@bot.message_handler(regexp="Block Fan ID Card")
def block_fan_id_card(message):
    if user.role == "cashier":
        send(message, "Enter Fan ID Card holder's username you would like to block", enter_username_to_block)


def enter_username_to_block(message):
    username = message.text
    customer = Customer.construct(username)
    user.person.block_fan_id_card(customer)
    send(message, "The Fan ID Card {} was successfully blocked".format(customer.fan_id_card.id))


# organizer

@bot.message_handler(regexp="Add match")
def add_match(message):
    if user.role == "organizer":
        global new_match
        new_match = NewMatch()
        send(message, "Enter host team", enter_host_team)


def enter_host_team(message):
    new_match.host_team = message.text
    send(message, "Enter guest team", enter_guest_team)


def enter_guest_team(message):
    new_match.guest_team = message.text
    send(message, "Enter match date in format YYYY-MM-DD", enter_match_date)


def enter_match_date(message):
    new_match.date = message.text
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("Group")
    user_markup.row("Quarterfinal")
    user_markup.row("Semifinal")
    user_markup.row("Final")
    sent = bot.send_message(message.chat.id, "Choose match type", reply_markup=user_markup)
    bot.register_next_step_handler(sent, enter_match_type)


def enter_match_type(message):
    match_type = message.text
    new_match.match_type = match_type
    match = Match(None, new_match.host_team, new_match.guest_team, new_match.date, user.person.username, new_match.match_type)
    user.person.add_match(match)
    send(message, "The match {} between {} and {} was successfully added".format(match.id, match.host_team, match.guest_team))


@bot.message_handler(regexp='Update match')
def update_match(message):
    if user.role == "organizer":
        send(message, "Enter match ID you would like to update", enter_match_id_to_update)


def enter_match_id_to_update(message):
    match_id = int(message.text)
    global match
    match = Match.construct(match_id)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("Host team", "Guest team")
    user_markup.row("Match date", "Match type")
    user_markup.row("Cancel")
    sent = bot.send_message(message.chat.id, "Choose field you would like to update", reply_markup=user_markup)
    bot.register_next_step_handler(sent, enter_field_to_udpate)


def enter_field_to_udpate(message):
    field = message.text
    if field == "Host team":
        send(message, "Enter new name of host team", enter_new_host_team)
    elif field == "Guest team":
        send(message, "Enter new name of guest team", enter_new_guest_team)
    elif field == "Match date":
        send(message, "Enter new match date in format YYYY-MM-DD", enter_new_match_date)
    elif field == "Match type":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("Group")
        user_markup.row("Quarterfinal")
        user_markup.row("Semifinal")
        user_markup.row("Final")
        sent = bot.send_message(message.chat.id, "Choose match type", reply_markup=user_markup)
        bot.register_next_step_handler(sent, enter_new_match_type)


def enter_new_host_team(message):
    match.host_team = message.text
    user.person.update_match(match)
    send(message, "Host team name was successfully updated")


def enter_new_guest_team(message):
    match.guest_team = message.text
    user.person.update_match(match)
    send(message, "Guest team name was successfully updated")


def enter_new_match_date(message):
    match.date = message.text
    user.person.update_match(match)
    send(message, "Match date was successfully updated")


def enter_new_match_type(message):
    match.match_type = message.text
    user.person.update_match(match)
    send(message, "Match type name was successfully updated")


@bot.message_handler(regexp='Delete match')
def delete_match(message):
    if user.role == "organizer":
        send(message, "Enter match ID you would like to delete", enter_match_id_to_delete)


def enter_match_id_to_delete(message):
    match_id = int(message.text)
    user.person.delete_match(match_id)
    send(message, "The match {} was successfully deleted".format(match_id))


@bot.message_handler(regexp='Cancel match')
def cancel_match(message):
    if user.role == "organizer":
        send(message, "Enter match ID you would like to cancel", enter_match_id_to_cancel)


def enter_match_id_to_cancel(message):
    match_id = int(message.text)
    user.person.cancel_match(match_id)
    send(message, "The match {} was successfully cancelled".format(match_id))


bot.polling()
