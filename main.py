import tkinter
from tkinter import messagebox
import json
import random
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def create_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    num_letter = random.randint(4, 8)
    num_num = random.randint(2, 6)
    num_sym = random.randint(2, 4)

    password = [random.choice(letters) for _ in range(num_letter)]
    password += [random.choice(numbers) for _ in range(num_num)]
    password += [random.choice(symbols) for _ in range(num_sym)]

    random.shuffle(password)
    passw = ''.join(password)

    pass_i.delete(0, tkinter.END)
    pass_i.insert(0, passw)
    pyperclip.copy(passw)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    w = website_i.get()
    e = email_i.get()
    p = pass_i.get()

    if not w:
        msg_l.config(text="Please enter the website url.", fg="red")
    elif not e:
        msg_l.config(text="Please enter the email/username.", fg="red")
    elif not p:
        msg_l.config(text="Please enter the password or use password generator button.", fg="red")
    else:
        # messagebox.askokcancel(title="Data verification", message="Do you want to save the data")
        data = {
            w: {
                'email': e,
                'pass': p
            }
        }
        try:
            with open("password_data.json", "r") as dataf:
                old_data = json.load(dataf)
        except FileNotFoundError:
            with open("password_data.json", "w") as dataf:
                json.dump(data, dataf, indent=4)
        else:
            old_data.update(data)
            with open("password_data.json", "w") as dataf:
                json.dump(old_data, dataf, indent=4)

        website_i.delete(0, tkinter.END)
        email_i.delete(0, tkinter.END)
        pass_i.delete(0, tkinter.END)
        msg_l.config(text="Data saved successfully!", fg="green")


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_pass():
    w = website_i.get()
    if not w:
        msg_l.config(text="Please enter the website url.", fg="red")
    else:
        try:
            with open('password_data.json') as dataf:
                data = json.load(dataf)
        except FileNotFoundError:
            msg_l.config(text=f"Credentials not for the website {w}.", fg="red")
        else:
            if w in data:
                msg_l.config(text="", fg="green")
                messagebox.showinfo(title=w, message=f"Email: {data[w].get('email')}\nPassword: {data[w].get('pass')}")
            else:
                msg_l.config(text=f"Credentials not for the website {w}.", fg="red")



# ---------------------------- UI SETUP ------------------------------- #
# Main Window
window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.resizable(width=False, height=False)

# Background Image
canvas = tkinter.Canvas(width=256, height=256)
back_image = tkinter.PhotoImage(file="password-manager.png")
canvas.create_image(128, 128, image=back_image)
canvas.grid(column=1, row=1, columnspan=3)

# Error Label
msg_l = tkinter.Label(text="", font=("Roboto", 10, "italic"))
msg_l.grid(column=1, row=2, columnspan=3)
msg_l.config(pady=5)

# Website Field
website_l = tkinter.Label(text="Website:", font=("Roboto", 12))
website_l.grid(column=1, row=3)
website_i = tkinter.Entry(width=29, background="white")
website_i.grid(column=2, row=3, columnspan=1)
website_i.focus()

# Find Password Button
f_pass_l = tkinter.Button(text="Search Password", font=("Roboto", 10), bg="white", command=search_pass)
f_pass_l.grid(column=3, row=3)

# Email/Username Field
email_l = tkinter.Label(text="Email/Username:", font=("Roboto", 12))
email_l.grid(column=1, row=4)
email_i = tkinter.Entry(width=50, background="white")
email_i.grid(column=2, row=4, columnspan=2)
email_i.insert(0, "test@gmail.com")
# Password Field
pass_l = tkinter.Label(text="Password:", font=("Roboto", 12))
pass_l.grid(column=1, row=5)
pass_i = tkinter.Entry(width=29, background="white")
pass_i.grid(column=2, row=5)

# Password Button
pass_l = tkinter.Button(text="Generate Password", font=("Roboto", 10), bg="white", command=create_pass)
pass_l.grid(column=3, row=5)

# Save Button
save_l = tkinter.Button(text="Add", font=("Roboto", 10), bg="white", width=37, command=save_data)
save_l.grid(column=2, row=7, columnspan=2)

window.mainloop()
