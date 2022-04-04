import re
import sys
import time
import mysql.connector
import socket
import pygame


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text, pos, font, bg="White", feedback=""):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text, bg="White"):
        """Change the text whe you click"""
        self.text = self.font.render(text, True, pygame.Color("black"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        window.blit(self.surface, (self.x, self.y))

    def click_message(self, event, role):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    if role == "Login":
                        Login()
                    if role == "Sing up":
                        Sing_up()


def InputUser():
    global delete_password
    global delete_user_name
    pygame.draw.rect(window, color_password, input_rec_password)
    window.blit(text_surface_password, (input_rec_password.x + 5, input_rec_password.y + 5))

    pygame.draw.rect(window, color_username, input_rec_username)
    window.blit(text_surface_user_name, (input_rec_username.x + 5, input_rec_username.y + 5))

    pygame.draw.rect(window, color_ip, input_IP_server)
    window.blit(text_surface_IP, (input_IP_server.x + 5, input_IP_server.y + 5))

    window.blit(text_surface_message, (window.get_width() / 2 - 125, window.get_height() / 2 + 335))
    button.show()
    button2.show()
    if input_rec_username.w > text_surface_user_name.get_width() + 20:
        delete_user_name = True
    else:
        delete_user_name = False
    if input_rec_password.w > text_surface_password.get_width() + 20:
        delete_password = True
    else:
        delete_password = False
    if input_IP_server.w > text_surface_IP.get_width() + 20:
        delete_password = True
    else:
        delete_password = False


def CheckAccount(role):
    global message_text
    if role == "Login":
        mycursor.execute(f"SELECT * FROM Login WHERE username = '{user_name_text}'")
        myresult = mycursor.fetchone()
        print(myresult)
        if myresult == None:
            message_text = "Error the account is no exist"
            print("don't found")
            return False
        else:
            if user_name_text in myresult and password_text in myresult:
                message_text = "Loging in"
                print("found")
                return True
    elif role == "Sing up":
        mycursor.execute(f"SELECT * FROM Login WHERE username = '{user_name_text}'")
        myresult = mycursor.fetchone()
        print(myresult)
        if myresult != None:
            if user_name_text in myresult and password_text in myresult:
                message_text = "The user name is already exist"
                print("the user is exist")
                return False
        else:
            message_text = "Create user"
            print("create user")
            return True


def Login():
    global active_window
    if CheckAccount(role="Login"):
        sql = "INSERT INTO Login (IP) VALUES (%s)"
        mycursor.execute(sql, (Local_Ip,))
        mydb.commit()
        image = pygame.image.load('login.gif')
        window.blit(image, (window.get_width() / 2 - 300, window.get_height() / 2 - 170))
        active_window = True
    else:
        active_window = False


def Sing_up():
    if CheckAccount(role="Sing up"):
        sql = "INSERT INTO Login (username,password,IP) VALUES (%s, %s, %s)"
        val = (user_name_text, password_text, Local_Ip)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        mycursor.execute("SELECT * FROM Login")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
        Login()


clock = pygame.time.Clock()
Local_Ip = socket.gethostbyname(socket.gethostname())
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="753159753159Xz",
    database="Dragonraja"
)
mycursor = mydb.cursor()
mycursor.execute("DROP TABLE Login")
mycursor.execute("CREATE TABLE Login (username VARCHAR(255), password VARCHAR(255), IP VARCHAR(255))")
mycursor.execute("ALTER TABLE Login ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
image = pygame.image.load('img1.png')
pygame.init()
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
image = pygame.transform.scale(image, (window.get_width(), window.get_height()))
base_font = pygame.font.Font(None, 30)

user_name_text = 'Enter Username'
input_rec_username = pygame.Rect(0, 0, 225, 30)
input_rec_username.centerx = window.get_width() / 2
input_rec_username.centery = window.get_height() / 2

password_text = ''
password_hash = 'Enter Password'
input_rec_password = pygame.Rect(0, 0, 225, 30)
input_rec_password.centerx = window.get_width() / 2
input_rec_password.centery = window.get_height() / 2 + 45

ip_text = 'Enter IP server'
input_IP_server = pygame.Rect(0, 0, 255, 30)
input_IP_server.centerx = window.get_width() / 2
input_IP_server.centery = window.get_height() / 2 + 250

message_box = pygame.Rect(650, 600, 200, 30)
message_text = ''

button = Button("Login", (window.get_width() / 2 - 30, window.get_height() / 2 + 90), 30)
button2 = Button("Sign up", (window.get_width() / 2 - 30, window.get_height() / 2 + 135), 30)
Color_active = pygame.Color(0, 255, 0)
Color_passive = pygame.Color(255, 255, 255)
color_username = Color_passive
color_password = Color_passive
color_ip = Color_passive
delete_ip = False
delete_user_name = False
delete_password = False
active_ip = False
active_user_name = False
active_password = False
active_window = False
Sing_up_active = False
window.blit(image, (0, 0))
while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rec_username.collidepoint(event.pos):
                active_user_name = True
                if user_name_text == "Enter Username":
                    user_name_text = ''
            else:
                active_user_name = False

            if input_rec_password.collidepoint(event.pos):
                active_password = True
                if password_hash == 'Enter Password':
                    password_hash = ''
            else:
                active_password = False

            if input_IP_server.collidepoint(event.pos):
                active_ip = True
                if ip_text == "Enter IP server":
                    ip_text = ''
            else:
                active_ip = False

        if active_user_name:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_name_text = user_name_text[:-1]
                elif delete_user_name and not (
                        event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or event.key == pygame.K_DELETE or event.key == pygame.K_TAB):
                    user_name_text += event.unicode
        if active_password:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    password_text = password_text[:-1]
                    password_hash = password_hash[:-1]
                elif delete_password and not (
                        event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or event.key == pygame.K_DELETE or event.key == pygame.K_TAB):
                    password_text += event.unicode
                    password_hash += "*"
        if active_ip:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    ip_text = ip_text[:-1]
                elif delete_ip and not (event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or event.key == pygame.K_DELETE or event.key == pygame.K_TAB):
                    ip_text += event.unicode

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if not active_window:
            button.click_message(event, role="Login")
            button2.click_message(event, role="Sing up")

    if active_user_name:
        color_username = Color_active
    else:
        color_username = Color_passive
    if active_password:
        color_password = Color_active
    else:
        color_password = Color_passive
    if active_ip:
        color_ip = Color_active
    else:
        color_ip = Color_passive

    text_surface_password = base_font.render(password_hash, True, (0, 0, 0))
    text_surface_user_name = base_font.render(user_name_text, True, (0, 0, 0))
    text_surface_message = base_font.render(message_text, True, (255, 0, 0))
    text_surface_IP = base_font.render(ip_text, True, (0, 0, 0))

    if not active_window:
        InputUser()
    elif Sing_up_active:
        Sing_up()

    if input_rec_username.w > text_surface_user_name.get_width() + 20:
        delete_user_name = True
    else:
        delete_user_name = False
    if input_rec_password.w > text_surface_password.get_width() + 20:
        delete_password = True
    else:
        delete_password = False
    if input_IP_server.w > text_surface_IP.get_width() + 20:
        delete_ip = True
    else:
        delete_ip = False
    # pygame.draw.rect(window, (255, 255, 255), button)
    # text_surface_button = base_font.render("submit", True, (0, 0, 0))
    # window.blit(text_surface_button, (715, 603))

    pygame.display.flip()
    clock.tick(60)
