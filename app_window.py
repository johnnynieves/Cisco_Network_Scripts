from tkinter import *


app = Tk()

menu_lable = Label(app, text="MAIN MENU", font=('bold', 16), pady=20)
menu_lable.grid(row=0, column=3)

device_info = Button(app, text="1. Get Device Info", font=('bold', 11), pady=5)
device_info.grid(row=2, column=2, sticky=W)

ios_ver_button = Button(app, text="2. Get IOS Version",
                        font=('bold', 11), pady=5)
ios_ver_button.grid(row=2, column=3, sticky=W)

upgrade = Button(app, text="3. IOS Upgrade", font=('bold', 11), pady=5)
upgrade.grid(row=2, column=4, sticky=W)

link_stat = Button(
    app, text="4. Check Link Status", font=('bold', 11), pady=5)
link_stat.grid(row=3, column=2, sticky=W)

port_security = Button(
    app, text="5. Check Port-Security", font=('bold', 11), pady=5)
port_security.grid(row=3, column=3, sticky=W)

int_desc = Button(
    app, text="6. Check Interface Descriptions", font=('bold', 11), pady=5)
int_desc.grid(row=3, column=4, sticky=W)

make_golden = Button(
    app, text='7. Make "Golden Configs"', font=('bold', 11), pady=5)
make_golden.grid(row=4, column=2, sticky=W)

compare_golden = Button(
    app, text='8. Verify "Golden" Configs"', font=('bold', 11), pady=5)
compare_golden.grid(row=4, column=3, sticky=W)

app_close = Button(app, text="0. Exit", font=('bold', 11), pady=5)
app_close.grid(row=4, column=4, sticky=E+W)

menu_option = StringVar()
menu_entry = Entry(app, textvariable=menu_option)
menu_entry.grid(row=5, column=2, sticky=W, padx=5)

app.title('Easy Network Manager')
app.geometry('780x480')


app.mainloop()
