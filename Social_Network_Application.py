from tkinter import *
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import tkinter.messagebox
import os


class User:
    def __init__(self, unique_id):
        self._unique_id = unique_id
        self._Contact_list = []
        self._Sent_message_list = []
        self._Received_message_list = []
        self._Group_message_list = []

    def get_unique_id(self):
        return self._unique_id

    def add_contact(self, contact_id):
        if contact_id not in self._Contact_list:
            self._Contact_list.append(contact_id)

    def send_message(self, unique_id, message):
        self._Sent_message_list.append((unique_id, message))

    def receive_message(self, unique_id, message):
        self._Received_message_list.append((unique_id, message))

    def receive_group_message(self, unique_id, group_id, message):
        self._Group_message_list.append((unique_id, group_id, message))

    def list_contacts(self):
        return self._Contact_list

    def list_groups(self):
        # noinspection PyGlobalUndefined
        global group_list
        group_list = []
        for group in Group_list:
            if group.in_member_list(self):
                group_list.append(group)
        return group_list

    def list_incoming_messages(self):
        return self._Received_message_list

    def list_group_messages(self):
        return self._Group_message_list


class Group:
    def __init__(self, unique_id):
        self._unique_id = unique_id
        self._Member_list = []
        self._Received_message_list = []

    def get_unique_id(self):
        return self._unique_id

    def add_member(self, member_id):
        if member_id not in self._Member_list:
            self._Member_list.append(member_id)

    def receive_group_message(self, unique_id, message):
        self._Received_message_list.append((unique_id, message))
        for member in self._Member_list:
            if member != unique_id:
                member.receive_group_message(unique_id, self, message)

    def in_member_list(self, user):
        if user in self._Member_list:
            return True
        return False


def get_people_in_the_network(directory):
    with open(directory + "/social_network.txt", 'r') as social_network_file:
        line = social_network_file.readline()
        line = line.strip('\n')
        line = line.strip('\r')
        line = line.strip()
        if line == "# users":
            for current_line in social_network_file:
                current_line = current_line.strip('\n')
                current_line = current_line.strip('\r')
                current_line = current_line.strip()
                if current_line == "# groups":
                    line = current_line
                    break
                if current_line != "":
                    if current_line.startswith('<') and current_line.endswith('>'):
                        current_line = current_line.strip('<')
                        current_line = current_line.strip('>')
                        current_line = current_line.strip()
                        colon_index = current_line.index(':')
                        current_user_id = current_line[0:colon_index]
                        current_user = None
                        if not in_user_list(current_user_id):
                            current_user = User(current_user_id)
                            User_list.append(current_user)
                        else:
                            current_user = get_user(current_user_id)
                        current_line = current_line[colon_index + 1:]
                        contact_id_list = current_line.split(',')
                        for contact_id in contact_id_list:
                            contact_id = contact_id.strip()
                            if not in_user_list(contact_id):
                                temp = User(contact_id)
                                User_list.append(temp)
                                current_user.add_contact(temp)
                            else:
                                current_user.add_contact(get_user(contact_id))
        if line == "# groups":
            for current_line in social_network_file:
                current_line = current_line.strip('\n')
                current_line = current_line.strip('\r')
                current_line = current_line.strip()
                if current_line != "":
                    if current_line.startswith('<') and current_line.endswith('>'):
                        current_line = current_line.strip('<')
                        current_line = current_line.strip('>')
                        current_line = current_line.strip()
                        colon_index = current_line.index(':')
                        current_group_id = current_line[0:colon_index]
                        current_group = None
                        if not in_group_list(current_group_id):
                            current_group = Group(current_group_id)
                            Group_list.append(current_group)
                        else:
                            current_group = get_group(current_group_id)
                        current_line = current_line[colon_index + 1:]
                        member_id_list = current_line.split(',')
                        for member_id in member_id_list:
                            member_id = member_id.strip()
                            if not in_user_list(member_id):
                                temp = User(member_id)
                                User_list.append(temp)
                                current_group.add_member(temp)
                            else:
                                current_group.add_member(get_user(member_id))


def get_messages_from_file(directory):
    if os.path.exists(directory + "/messages.txt"):
        with open(directory + "/messages.txt", 'r') as message_file:
            if os.path.getsize(directory + "/messages.txt"):
                for current_line in message_file:
                    if "_Sender_:" in current_line:
                        flag0 = 1
                        sender_id = current_line[9:]
                        sender_id = sender_id.strip()
                        sender_id = sender_id.strip('\n')
                        sender_id = sender_id.strip('\r')
                        sender = get_user(sender_id)
                    else:
                        continue
                    try:
                        current_line = next(message_file)
                    except StopIteration:
                        break
                    if "_Receiver_:" in current_line:
                        receiver_id = current_line[11:]
                        receiver_id = receiver_id.strip()
                        receiver_id = receiver_id.strip('\n')
                        receiver_id = receiver_id.strip('\r')
                        receiver = get_user(receiver_id)
                        flag1 = 0
                        if receiver is None:
                            flag1 = 1
                            receiver = get_group(receiver_id)
                    try:
                        current_line = next(message_file)
                    except StopIteration:
                        break
                    flag = 0
                    if "_Message_:" in current_line:
                        message = [current_line[10:]]
                        try:
                            current_line = next(message_file)
                        except StopIteration:
                            flag = 1
                        while current_line != "" and current_line != "\n" and current_line != "\r" and flag != 1:
                            message.append(current_line)
                            try:
                                current_line = next(message_file)
                            except StopIteration:
                                flag = 1
                                break
                    if flag0 == 1:
                        sender.send_message(receiver, message)
                        if flag1 != 1:
                            receiver.receive_message(sender, message)
                        else:
                            receiver.receive_group_message(sender, message)
                    if flag == 1:
                        break
    else:
        with open(directory + "/messages.txt","w+") as message_file:
            pass


def write_messages_to_file(directory, sender_id, receiver_id, message):
    with open(directory + "/messages.txt", 'a') as message_file:
        message_file.write("\n")
        message_file.write("_Sender_:" + sender_id + "\n")
        message_file.write("_Receiver_:" + receiver_id + "\n")
        i = 1
        for line in message:
            if i == 1:
                message_file.write("_Message_:" + line)
            else:
                message_file.write(line)
            i += 1


def in_user_list(user_id):
    for x in User_list:
        if user_id == x.get_unique_id():
            return True
    return False


def get_user(user_id):
    for x in User_list:
        if user_id == x.get_unique_id():
            return x
    return None


def in_group_list(group_id):
    for x in Group_list:
        if group_id == x.get_unique_id():
            return True
    return False


def get_group(group_id):
    for x in Group_list:
        if group_id == x.get_unique_id():
            return x
    return None


User_list = []
Group_list = []
get_people_in_the_network(os.getcwd())
get_messages_from_file(os.getcwd())


class TopFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="White", relief="raised")
        self.master = master
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, columnspan=2, sticky=S + N + E + W)
        self.label1 = Label(self, text="SOCIAL NETWORK", font=("Helvetica", 11, "bold"), bg="white", relief="raised",
                            padx=10, pady=10)
        self.label1.grid(row=0, column=0, sticky=E + W)
        self.grid_columnconfigure(0, weight=1)


class LeftFrame10(Frame):
    def __init__(self, master=None, rightframe=None):
        super().__init__(master, bg="#42e6f5")
        self.master = master
        self.rightframe = rightframe
        master.grid_rowconfigure(1, weight=300)
        master.grid_columnconfigure(0, weight=1)
        self.grid(row=1, column=0, sticky=S + N + E + W)
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
        for j in range(3):
            self.grid_columnconfigure(j, weight=1)
        self.label1 = Label(self, text="Choose Your Current User", font=("Helvetica", 12, "bold"), bd=3, pady=5, padx=5,
                            bg="#6ea4f5", relief="raised")
        self.label1.grid(row=0, column=0, columnspan=3, sticky=E + W + N)
        self.value = StringVar(self, User_list[0].get_unique_id())
        self.value.trace_variable('w', self.clear_rightframe)
        self.drop_down_user_list = ttk.Combobox(self, textvariable=self.value,
                                                values=[x.get_unique_id() for x in User_list])
        self.drop_down_user_list.configure(width=26, justify="left", font=("Helvetica", 11, "bold"),
                                           background="LightBlue", foreground="Black")
        self.drop_down_user_list.grid(row=1, column=1)

    def clear_rightframe(self, *args):
        for widget in self.rightframe.winfo_children():
            widget.destroy()


class LeftFrame20(Frame):
    def __init__(self, master=None, left_frame=None, right_frame=None):
        super().__init__(master, bg="#0071c7")
        self.master = master
        self.left_frame = left_frame
        self.right_frame = right_frame
        master.grid_rowconfigure(2, weight=700)
        master.grid_columnconfigure(0, weight=1)
        self.grid(row=2, column=0, sticky=S + N + E + W)
        for i in range(11):
            self.grid_rowconfigure(i, weight=1)
        for j in range(3):
            self.grid_columnconfigure(j, weight=1)
        self.button1 = Button(self, text="Display Incoming Messages", command=self.display_incoming_messages,
                              font=("Helvetica", 11, "bold"), bd=3, padx=5,
                              pady=5, relief="raised", bg="LightSteelBlue1")
        self.button1.grid(row=1, column=1)
        self.button2 = Button(self, text="Display Contacts", command=self.display_contacts,
                              font=("Helvetica", 11, "bold"), bd=3, padx=5,
                              pady=5, relief="raised", bg="LightSteelBlue1")
        self.button2.grid(row=3, column=1)
        self.button3 = Button(self, text="Display Groups", command=self.display_groups,
                              font=("Helvetica", 11, "bold"), bd=3, padx=5,
                              pady=5, relief="raised", bg="LightSteelBlue1")
        self.button3.grid(row=5, column=1)
        self.button4 = Button(self, text="Compose and Post Messages", command=self.compose_and_post,
                              font=("Helvetica", 11, "bold"), bd=3, padx=5,
                              pady=5, relief="raised", bg="LightSteelBlue1")
        self.button4.grid(row=7, column=1)
        self.button5 = Button(self, text="Exit", command=exit, font=("Helvetica", 11, "bold"), bd=3, padx=5,
                              pady=5, relief="raised", bg="LightSteelBlue1")
        self.button5.grid(row=9, column=1)
        self.grid_columnconfigure(0, weight=1)

    def create_canvas(self):
        self.right_frame.grid_rowconfigure(0, weight=1000)
        self.right_frame.grid_rowconfigure(1, weight=10)
        self.right_frame.grid_columnconfigure(0, weight=1000)
        self.right_frame.grid_columnconfigure(1, weight=10)
        canvas = Canvas(self.right_frame, bg="White", width=870, height=640)
        canvas.grid(row=0, column=0)
        h_bar = Scrollbar(self.right_frame, orient=HORIZONTAL)
        h_bar.grid(row=1, column=0, sticky=E + W)
        h_bar.grid_anchor(S)
        h_bar.config(command=canvas.xview)
        v_bar = Scrollbar(self.right_frame, orient=VERTICAL)
        v_bar.grid(row=0, column=1, sticky=N + S)
        v_bar.grid_anchor(E)
        v_bar.config(command=canvas.yview)
        canvas.configure(yscrollcommand=v_bar.set, xscrollcommand=h_bar.set)
        canvas.configure(scrollregion=(5, 5, 10000, 10000))
        return canvas

    def display_contacts(self):
        user_id = self.left_frame.value.get()
        contact_list = []
        for user in User_list:
            if user_id == user.get_unique_id():
                contact_list = user.list_contacts()
                break
        canvas = self.create_canvas()
        i = 1
        canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Navy", font=("Helvetica", 13, "bold"),
                           text="List Of Contacts of " + user_id + " are:")
        i += 2
        count = 1
        if len(contact_list) == 0:
            canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Black", font=("Helvetica", 11, "bold"),
                               text="No Existing Contacts")
        else:
            for contact in contact_list:
                canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Black", font=("Helvetica", 11, "bold"),
                                   text=str(count) + ") " + contact.get_unique_id())
                i += 1
                count += 1

    def display_groups(self):
        # noinspection PyGlobalUndefined
        global group_list
        user_id = self.left_frame.value.get()
        for user in User_list:
            if user_id == user.get_unique_id():
                group_list = user.list_groups()
                break
        canvas = self.create_canvas()
        i = 1
        canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Navy", font=("Helvetica", 13, "bold"),
                           text="List Of Groups " + user_id + " is a Member of:")
        i += 2
        count = 1
        if len(group_list) == 0:
            canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Black", font=("Helvetica", 11, "bold"),
                               text="No Existing Groups")
        else:
            for group in group_list:
                canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Black", font=("Helvetica", 11, "bold"),
                                   text=str(count) + ") " + group.get_unique_id())
                i += 1
                count += 1

    def display_incoming_messages(self):
        messages_list = []
        group_messages_list = []
        user_id = self.left_frame.value.get()
        for user in User_list:
            if user_id == user.get_unique_id():
                messages_list = user.list_incoming_messages()
                group_messages_list = user.list_group_messages()
                break
        canvas = self.create_canvas()
        i = 1
        canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Navy", font=("Helvetica", 13, "bold"),
                           text="Messages received by " + user_id + " are:")
        i += 2
        # noinspection PyGlobalUndefined
        global image_ref
        image_ref = []
        if len(messages_list) == 0 and len(group_messages_list) == 0:
            canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Black", font=("Helvetica", 11, "bold"),
                               text="No Messages")
        else:
            for sender, message in messages_list:
                canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Blue", font=("Helvetica", 11, "bold"),
                                   text=str(sender.get_unique_id()) + ":")
                i += 1
                for line in message:
                    line = line.strip('\n')
                    line = line.replace("\t", "    ")
                    if "<i>" in line:
                        # noinspection PyGlobalUndefined
                        global this_image
                        start = line.find("<i>") + 3
                        end = line.find("</i>", start)
                        address = line[start:end]
                        image_load = Image.open(address)
                        image_load = image_load.resize((450, 300), Image.ANTIALIAS)
                        this_image = ImageTk.PhotoImage(image_load)
                        image_ref.append(this_image)
                        canvas.create_text(10, i * 20, anchor=W, justify=LEFT,
                                           fill="Black", font=("Helvetica", 11, "bold"),
                                           text=line[0:start - 3])
                        i += 1
                        canvas.create_image(10, i * 20, image=this_image, anchor=NW)
                        i += this_image.height() / 20 + 1
                        canvas.create_text(10, i * 20, anchor=W, justify=LEFT,
                                           fill="Black", font=("Helvetica", 11, "bold"),
                                           text=line[end + 4:])
                        i += 1
                    else:
                        canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Black",
                                           font=("Helvetica", 11, "bold"), text=line)

                        i += 1
                i += 1
        if len(group_messages_list) != 0:
            for sender, group, message in group_messages_list:
                canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Red", font=("Helvetica", 11, "bold"),
                                   text=str(group.get_unique_id()) + ":")
                i += 1
                canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Blue", font=("Helvetica", 11, "bold"),
                                   text=str(sender.get_unique_id()) + ":")
                i += 1
                for line in message:
                    line = line.strip('\n')
                    line = line.replace("\t", "    ")
                    if "<i>" in line:
                        start = line.find("<i>") + 3
                        end = line.find("</i>", start)
                        address = line[start:end]
                        image_load = Image.open(address)
                        image_load = image_load.resize((450, 300), Image.ANTIALIAS)
                        this_image = ImageTk.PhotoImage(image_load)
                        image_ref.append(this_image)
                        canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Black",
                                           font=("Helvetica", 11, "bold"),
                                           text=line[0:start - 3])
                        i += 1
                        canvas.create_image(10, i * 20, image=this_image, anchor=NW)
                        i += this_image.height() / 20 + 1
                        canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Black",
                                           font=("Helvetica", 11, "bold"),
                                           text=line[end + 4:])
                        i += 1
                    else:
                        canvas.create_text(10, i * 20, anchor=W, justify=LEFT, fill="Black",
                                           font=("Helvetica", 11, "bold"), text=line)

                        i += 1
                i += 1

    def compose_and_post(self):
        user = None
        user_id = self.left_frame.value.get()
        for user in User_list:
            if user_id == user.get_unique_id():
                break
        canvas = self.create_canvas()
        i = 1
        canvas.create_text(10, i * 20, anchor=W, justify=CENTER, fill="Navy", font=("Helvetica", 13, "bold"),
                           text="COMPOSE AND POST")
        i += 2
        canvas.create_text(10, i * 20, anchor=W, justify=CENTER, fill="Blue", font=("Helvetica", 11, "bold"),
                           text="Select your contact or group to whom you want to send a message below:")
        i += 2
        receiver_list = [x.get_unique_id() for x in user.list_contacts()] + \
                        [x.get_unique_id() for x in user.list_groups()]
        if len(receiver_list) != 0:
            value = StringVar(canvas, receiver_list[0])
        else:
            value = StringVar(canvas, "")
        drop_down_list = ttk.Combobox(canvas, textvariable=value, values=receiver_list)
        drop_down_list.configure(width=30, justify="left", font=("Helvetica", 11, "bold"),
                                 background="LightBlue", foreground="Black")
        canvas.create_window(10, i * 20, anchor=NW, window=drop_down_list)
        i += 5
        canvas.create_text(10, i * 20, anchor=W, justify=CENTER, fill="Blue", font=("Helvetica", 11, "bold"),
                           text="Compose your message here:")
        i += 1
        textbox1 = Text(canvas, width=100, height=20, padx=10, pady=10, bd=5, relief="sunken",
                        font=('Helvetica', 10, 'bold'))
        canvas.create_window(10, i * 20, anchor=NW, window=textbox1)
        i += 16
        file_label = Label(canvas, bg="White", fg="Green", padx=5, pady=5, font=('Helvetica', 12, 'bold'))
        canvas.create_window(210, i * 20, anchor=NW, window=file_label)
        choose_file = Button(canvas, text="Choose Images To Attach",
                             command=lambda: self.browse_files(file_label, user, value, textbox1, send_message),
                             height=1, bd=3, padx=2, pady=2, relief="raised", font=('Helvetica', 11, 'bold'),
                             bg="LightGrey", fg="black")
        canvas.create_window(10, i * 20, anchor=NW, window=choose_file)
        i += 2
        send_message = Button(canvas, text="Send",
                              command=lambda: self.send_message(user.get_unique_id(), value.get(), textbox1),
                              height=1, bd=3, padx=2, pady=2, relief="raised", font=('Helvetica', 11, 'bold'),
                              bg="Cyan", fg="black", activebackground="Lime")
        canvas.create_window(350, i * 20, anchor=NW, window=send_message)

    def browse_files(self, file_label, user, value, textbox1, send_message):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a File",
                                              filetypes=(("JPG files", "*.jpg"),
                                                         ("JPEG files", "*.jpeg"),
                                                         ("PNG files", "*.png"),
                                                         ("All files", "*.*")))
        file_label.configure(text=filename)
        send_message.configure(command=lambda: self.send_message(user.get_unique_id(),
                                                                 value.get(), textbox1,
                                                                 str("<i>" + filename + "</i>\n")))

    @staticmethod
    def send_message(sender_id, receiver_id, textbox1, image_file=None):
        message = [textbox1.get(1.0, END)]
        if image_file is not None:
            message.append(image_file)
        sender = get_user(sender_id)
        receiver = get_user(receiver_id)
        flag = 0
        if receiver is None:
            flag = 1
            receiver = get_group(receiver_id)
        sender.send_message(receiver, message)
        if flag == 0:
            receiver.receive_message(sender, message)
        else:
            receiver.receive_group_message(sender, message)
        write_messages_to_file(os.getcwd(), sender.get_unique_id(), receiver_id, message)
        tkinter.messagebox.showinfo("Notification", "Message has been sent to " + receiver_id + " successfully")


class RightFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#170073")
        self.master = master
        master.grid_columnconfigure(1, weight=3)
        self.grid(row=1, column=1, rowspan=3, sticky=S + N + E + W)


class Window(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.geometry("1000x600")
        master.wm_title("Social Network")
        self.top_frame = TopFrame(master)
        self.right_frame = RightFrame(master)
        self.left_frame1 = LeftFrame10(master, self.right_frame)
        self.left_frame2 = LeftFrame20(master, self.left_frame1, self.right_frame)


root = Tk()
app = Window(root)
root.mainloop()

