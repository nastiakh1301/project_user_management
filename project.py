import re
from pathlib import Path
import random
from string import ascii_lowercase, ascii_letters, digits, punctuation

BASE_DIR = Path(__file__).resolve().parent

def main():
    menu()
    return True


def menu():
    user_list = []
    user_data = {}
    print(
        "\nГоловне меню: " 
        "\n1. Зареєструвати нового користувача."
        "\n2. Подивитись список користувачів"
    )
    a = input("Оберіть наступну дію: ")

    if a == '1':
        registration()

    elif a == '2':
        open_file(user_data, user_list)
        print(f"Кількість зареєстрованих користувачів: {len(user_list)}")    

        if input("Відобразити всіх користувачів? (Y/n) ") == "Y":
            for i, item in enumerate(user_list):
                print(i + 1, item["phone"])

            if input("Відобразити детальну інформацію про користувача? (Y/n) ") == "Y":
                user = {}
                user = show_user(user_list)
                print(
                    "\n1. Скинути пароль."
                    "\n2. Видалити користувача"
                )
                b = input("Оберіть наступну дію: ")
                if b == '1':
                    reset_password(user)
                    save_new_password(user)
                    menu()
                #elif b == '2':
                #    delete_user(user_data, user_list)
                #    menu()
                else:
                    print("Спробуйте ще раз")
                    menu()
            else:
                menu()
        else:
            menu()
    else:
        print("Спробуйте ще раз")
        menu()
    return True


def registration():
    user_list = []
    user_data = {}
    open_file(user_data, user_list)
    user_data = {"phone" : None, "email" : None, "password" : None}
    user_list.append(user_data)

    while True:
        phone = get_phone()
        email = get_email()
        password = get_password()
        user_data = {"phone" : phone, "email" : email, "password" : password}
        if check_phone(phone, user_list) is True:
            print("Такий номер вже є. Спробуйте ще раз.")
        else:
            user_list.append(user_data)
            save_data(user_data)
            print(
                f"\nВітаємо з успішною реєстрацією!"
                f"\nВаш номер телефону: +{phone}"
                f"\nВаш email: {email}"
                f'\nВаш пароль: {"*" * len(password)}'
            ) 
        if input("Continue? (Y/n) ") == "n":
            break
            
    menu()
    return user_list


def get_phone():
    phone = input("Введіть номер телефону: ")
    phone = re.sub(r"\D", "", phone)
    return "380" + phone[-9:] if len(phone) > 8 else get_phone()


def get_email():
    email = input("Введіть email: ")
    if len(email) < 6 or email.count("@") != 1 or email.startswith("@"):
        print("Невірний формат. Введіть повторно.")
        return get_email()
    return email


def get_password():
    password = input("Введіть пароль: ")
    if len(password) < 8 or re.findall(r"\s", password):
        print("Пароль надто простий. Придумайте більш надійний.")
        return get_password()

    u_counter = l_counter = d_counter = s_counter = 0
    for i in password:
        if i.isupper():
            u_counter += 1
        elif i.islower():
            l_counter += 1
        elif i.isdigit():
            d_counter += 1
        else:
            s_counter += 1

    if min(u_counter, l_counter, d_counter, s_counter) == 0:
        print("Пароль надто простий. Придумайте більш надійний.")
        return get_password()

    if input("Повторіть пароль: ") != password:
        print("Паролі не співпадають.")
        return get_password()
    return password


def open_file(user_data, user_list):
    with open(BASE_DIR / "users.txt", "r") as f:
        onstring = f.read().split("\n")[:-1]
        for item in onstring:
            dic = item[1:-1].split(", ")
            user_data = {}
            for p in dic:
                key = p.split(": ")[0]
                value = p.split(": ")[1]
                user_data[key[1:-1]] = value[1:-1]
            user_list.append(user_data)
    return user_list


def save_data(user_data):
    with open(BASE_DIR / "users.txt", "a") as f:
        print(f"{user_data}", file=f)


def save_new_password(user):
    with open(BASE_DIR / "users.txt", "a") as f:
        print(f"{user}", file=f)


def check_phone(phone, user_list):
    for p in user_list:
        if p["phone"] == phone:
            return True


def show_user(user_list):
    number = int(input("Введіть номер користувача: "))
    selected_user = user_list[number - 1]
    print(selected_user)
    return selected_user


def reset_password(user):
    new_password = gen_strong_pw()
    user.update({"password" : new_password})
    print(new_password)
    return user


def gen_password(chars, length=8):
    password = ""
    for i in range(length):
        password += random.choice(chars)
    return password


def gen_strong_pw():
    length = random.randint(8, 16)
    password = gen_password(digits + ascii_letters + punctuation, length)

    counter_d = counter_u = counter_l = counter_s = 0
    for char in password:
        if char.isdigit():
            counter_d += 1
        elif char.isupper():
            counter_u += 1
        elif char.islower():
            counter_l += 1
        elif not char.isspace():
            counter_s += 1

    if counter_d and counter_u and counter_l and counter_s:
        return password
    return gen_strong_pw()
            


#def delete_user(user_data, user_list):
#    open_file(user_data, user_list)
#    return True



if __name__ == "__main__":
    main()