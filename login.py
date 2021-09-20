d = {'agan': 'gan19891107', 'song': '1234567890'}


def login(login_window, main_window):
    name = login_window.user_name.text()
    password = login_window.password.text()
    if name in d:
        if password == d.get(name):
            main_window.show()
            login_window.close()
