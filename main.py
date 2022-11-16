from click import command
from tkcalendar import Calendar
from member import member
from task import task
from tkinter import *
#a lil comment test #2
#for multiple branches
#initializes window
root = Tk()
root.title("TeamMate")
root.geometry("600x600")

Header = Frame(root, bg='black', height=30)
Content = Frame(root, pady=10)
Footer = Frame(root)

instruction = StringVar()
instruction.set("Main Menu")
InstructionLabel = Label(Header,
                         textvariable=instruction,
                         bg='black',
                         fg='white').pack()

Header.pack(fill='both')
Content.pack()

#Entries
nameEntry = Entry(Content)
roleEntry = Entry(Content)
teamNameEntry = Entry(Content)
descriptionEntry = Entry(Content)
numTeamMembersEntry = Entry(Content, width=5)
taskListLabel = Label(Content)

cal = Calendar(Content, selectmode='day')
select = StringVar()
selected1 = StringVar()

#variables
i = 0

teamList = []
teamName = ''
numTeamMembers = 0

nameEntries = []
entries = []
entries2 = []

nameList = []
roleList = []


#methods
def addTeamsMembers():
    global nameList
    global roleList

    for entry in entries:
        nameList.append(entry.get())
    print("name List\n" + str(nameList))

    for entry in entries2:
        roleList.append(entry.get())
    print("\nRole List: \n" + str(roleList))

    x = 0
    for x in range(len(nameList)):
        teamList.append(member(nameList[x], roleList[x]))
    list = Content.grid_slaves()

    for l in list:
        if isinstance(l, Entry):
            l.destroy()

    startUp()
    instruction.set("Adding Members")


def contButtonCreateTeam():
    global teamName
    global numTeamMembers
    global i

    teamName = teamNameEntry.get()
    numTeamMembers = numTeamMembersEntry.get()
    continueButtonAddTeamsMembers = Button(
        Content,
        text="Add Members",
        command=lambda:
        [addTeamsMembers(),
         continueButtonAddTeamsMembers.grid_remove(),nameLabel.grid_remove(), roleLabel.grid_remove()])
    continueButtonAddTeamsMembers.grid(row=1, column=0)
    print(numTeamMembers)
    nameLabel = Label(Content, text="Name")
    nameLabel.grid(row=0, column=1)
    roleLabel = Label(Content, text="Role")
    roleLabel.grid(row=0, column=2)
    for i in range(int(numTeamMembers)):
        en = Entry(Content)
        en2 = Entry(Content)
        en.grid(row=i + 1, column=1, ipady=3)
        en2.grid(row=i + 1, column=2, ipady=3)
        entries.append(en)
        entries2.append(en2)
    teamNameEntry.delete(0, END)
    numTeamMembersEntry.delete(0, END)

    instruction.set("Creating Team")


def contButtonAddMember():

    teamList.append(member(nameEntry.get(), roleEntry.get()))
    nameEntry.delete(0, END)
    roleEntry.delete(0, END)
    nameEntry.grid_remove()
    roleEntry.grid_remove()
    instruction.set("Member Added!")


def listRemove():
    list = Content.grid_slaves()
    count = 0

    for l in list:

        if isinstance(l, OptionMenu):
            count = count + 1
            if count == 1:
                l.destroy()


def contButtonGetSchedule():
    name = selected1.get()
    print(name)
    date = cal.get_date()
    output = ""
    i = 0
    for i in range(len(teamList)):
        if name == teamList[i].name:
            for j in range(len(teamList[i].taskList)):
                if teamList[i].taskList[j].dueDate == date:
                    output += teamList[i].taskList[j].description + "\n"
    print(output)
    taskListLabel.config(text=output)
    taskListLabel.grid(row=2, column=1)
    doneButton = Button(Content,
                        text="Done",
                        command=lambda: [
                            taskListLabel.grid_remove(),
                            cal.grid_remove(),
                            listRemove(),
                            doneButton.grid_remove()
                        ])
    doneButton.grid(row=2, column=3)


def contButtonAddTask():
    task1 = task(descriptionEntry.get(), select.get(), cal.get_date())
    print(descriptionEntry.get(), select.get())
    i = 0
    for i in range(len(teamList)):
        if (teamList[i].role == select.get()):
            teamList[i].taskList.append(task1)
    print("task list test: \n", teamList[0].taskList[0].dueDate)
    descriptionEntry.delete(0, END)
    descriptionEntry.grid_remove()
    cal.grid_remove()
    list = Content.grid_slaves()
    count = 0

    for l in list:

        if isinstance(l, OptionMenu):
            count = count + 1
            if count == 1:
                l.destroy()


def contButton1():

    if selected.get() == options[1]:
        instruction.set("Enter your Member Information")
        continueButton = Button(
            Content,
            text="Continue add member",
            command=lambda:
            [contButtonAddMember(),
             continueButton.grid_remove()])
        continueButton.grid(row=1, column=0)
        nameEntry.grid(row=0, column=1)
        roleEntry.grid(row=0, column=2)

    if selected.get() == options[3]:
        selected1.set("Select Member to View")
        menu = OptionMenu(Content, selected1, *nameList)
        print(str(nameList))
        menu.grid(row=3, column=2)
        instruction.set("Select a Date")
        continueButton = Button(
            Content,
            text="Continue Get schedule",
            command=lambda:
            [contButtonGetSchedule(),
             continueButton.grid_remove()])
        continueButton.grid(row=1, column=0)
        cal.grid(row=0, column=1, rowspan=2, columnspan=2)

    if selected.get() == options[4]:
        select.set("which role for the task?")
        noRepeatRoleList = [*set(roleList)]
        menu = OptionMenu(Content, select, *noRepeatRoleList)
        menu.grid(row=0, column=2)
        instruction.set("Enter a Task")
        cal.grid(row=1, column=2)
        descriptionEntry.grid(row=0, column=1)

        def tempTextTask(e):
            descriptionEntry.delete(0, "end")

        descriptionEntry.insert(0, "Enter Description")
        descriptionEntry.bind("<FocusIn>", tempTextTask)

        continueButton = Button(
            Content,
            text="Continue add task",
            command=lambda:
            [contButtonAddTask(),
             continueButton.grid_remove()])
        continueButton.grid(row=1, column=0)


options = [
    "Edit Team",
    "Add Member",
    "Edit Member",
    "View Schedule",
    "Add Task",
]
selected = StringVar()
selected.set(options[0])
dropDown = OptionMenu(Content, selected, *options)


def tempTextTeam(e):
    teamNameEntry.delete(0, "end")

instruction.set("Enter your Team Information")

teamNameEntry.insert(0, "Enter Team Name")
teamNameEntry.bind("<FocusIn>", tempTextTeam)

continueButton = Button(Content,
                        text="Continue",
                        command=lambda: [
                            contButtonCreateTeam(),
                            continueButton.grid_remove(),
                            incrementButton.grid_remove(),
                            decrementButton.grid_remove(),
                            numTeamMembersEntry.grid_remove(),
                            teamNameEntry.grid_remove()
                        ])

continueButton.grid(row=0, column=0)
teamNameEntry.grid(row=0, column=1)

memCount = 1
numTeamMembersEntry.insert(0, memCount)


def increment():
    global memCount
    numTeamMembersEntry.delete(0, END)
    memCount += 1
    numTeamMembersEntry.insert(0, memCount)


def decrement():
    global memCount
    if memCount != 1:
        numTeamMembersEntry.delete(0, END)
        memCount -= 1
        numTeamMembersEntry.insert(0, memCount)
    else:
        pass


incrementButton = Button(Content, text="+", command=lambda: increment())
decrementButton = Button(Content, text="-", command=lambda: decrement())

decrementButton.grid(row=0, column=2)
incrementButton.grid(row=0, column=4)

numTeamMembersEntry.grid(row=0, column=3)


def startUp():
    dropDown.grid(row=0, column=0)
    dropDownButton = Button(Content, text="Select option",
                            command=contButton1).grid(row=2, column=0)


def testButtonCommand():
    list = Content.grid_slaves()
    for l in list:
        l.destroy()

    testButton = Button(Content, text="Test", command=testButtonCommand)
    testButton.grid(row=0, column=4)


#main
root.mainloop()
