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
dropDownSelection1 = StringVar()
dropDownSelection2 = StringVar()
dropDownSelection3 = StringVar()
dropDownSelection4 = StringVar()

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
    for entry in entries2:
        roleList.append(entry.get())

    x = 0
    for x in range(len(nameList)):
        teamList.append(member(nameList[x], roleList[x]))
    list = Content.grid_slaves()

    for l in list:
        if isinstance(l, Entry):
            l.destroy()

    startUp()
    instruction.set("Adding Members")


def createTeamCommand():
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


def addMemberCommand():

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


def getScheduleCommand():
    name = dropDownSelection1.get()
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


def addTaskCommand():
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

def completeTaskCommand():
    nameToFind = dropDownSelection2.get()
    i = 0
    for i in range(len(teamList)):
        if(teamList[i].name == nameToFind):
            indexToDisplayTaskListFor = i
    menu = OptionMenu(Content, dropDownSelection3, *teamList[i].taskList)
    menu.grid(row=0, column=2)
    
    completeTaskButton = Button(Content,
        text="Complete task",
         command= lambda: [
            deleteTaskFromList(indexToDisplayTaskListFor),
            completeTaskButton.grid_remove(),
            menu.grid_remove(),

         ])
    completeTaskButton.grid(row=1, column=0)
def deleteTaskFromList(teamIndex):
    i =0
    taskIndex = 0
    for i in range(len(teamList[teamIndex].taskList)):
        if teamList[teamIndex].taskList == dropDownSelection3.get():
            taskIndex = i
    del teamList[teamIndex].taskList[taskIndex]
    print("testedddd\n", teamList[teamIndex].taskList)


def removeMemberCommand():
    nameToFind = dropDownSelection4.get()
    i = 0
    for i in range(len(teamList)):
        if(teamList[i].name == nameToFind):
            indexToDelete = i
    del teamList[indexToDelete]


    
def selectOptionCommand():
    if dropDownSelection.get() == options[0]:
        instruction.set("Choose member")
        dropDownSelection4.set("Member to Remove")
        i = 0
        roleList1 = []
        nameList1 = []
        for i in range(len(teamList)):
            roleList1.append(teamList[i].role)
            nameList1.append(teamList[i].name)
        menu = OptionMenu(Content, dropDownSelection4, *nameList1)
        menu.grid(row=0, column=1)
        continueButton = Button(
            Content,
            text="Remove",
            command= lambda:
            [removeMemberCommand(),
            continueButton.grid_remove(),
            menu.grid_remove()
            ]
        )
        continueButton.grid(row=1, column=0)

    if dropDownSelection.get() == options[1]:
        instruction.set("Enter your Member Information")
        continueButton = Button(
            Content,
            text="Continue add member",
            command=lambda:
            [addMemberCommand(),
             continueButton.grid_remove()])
        continueButton.grid(row=1, column=0)
        nameEntry.grid(row=0, column=1)
        roleEntry.grid(row=0, column=2)

    if dropDownSelection.get() == options[3]:
        dropDownSelection1.set("Select Member to View")
        i = 0
        roleList1 = []
        nameList1 = []
        for i in range(len(teamList)):
            roleList1.append(teamList[i].role)
            nameList1.append(teamList[i].name)
        menu = OptionMenu(Content, dropDownSelection1, *nameList1)
        print(str(nameList1))
        menu.grid(row=3, column=2)
        instruction.set("Select a Date")
        continueButton = Button(
            Content,
            text="Continue Get schedule",
            command=lambda:
            [getScheduleCommand(),
             continueButton.grid_remove()])
        continueButton.grid(row=1, column=0)
        cal.grid(row=0, column=1, rowspan=2, columnspan=2)

    if dropDownSelection.get() == options[4]:
        select.set("which role for the task?")
        i = 0
        roleList1 = []
        nameList1 = []
        for i in range(len(teamList)):
            roleList1.append(teamList[i].role)
            nameList1.append(teamList[i].name)
        noRepeatRoleList = [*set(roleList1)]
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
            [addTaskCommand(),
             continueButton.grid_remove()])
        continueButton.grid(row=1, column=0)

    if dropDownSelection.get() == options[5]:
        dropDownSelection2.set("Which teamMember?")
        i = 0
        roleList1 = []
        nameList1 = []
        for i in range(len(teamList)):
            roleList1.append(teamList[i].role)
            nameList1.append(teamList[i].name)
        menu = OptionMenu(Content, dropDownSelection2, *nameList1)
        menu.grid(row=0, column=2)
        continueButton = Button(
            Content,
            text="select member to complete task",
            command= lambda:
            [completeTaskCommand(),
            continueButton.grid_remove(),
            menu.grid_remove()
            ]
        )
        continueButton.grid(row=1, column=0)


options = [
    "Edit Team",
    "Add Member",
    "Edit Member",
    "View Schedule",
    "Add Task",
    "Complete Task"
]
dropDownSelection = StringVar()
dropDownSelection.set(options[0])
dropDown = OptionMenu(Content, dropDownSelection, *options)


def tempTextTeam(e):
    teamNameEntry.delete(0, "end")

instruction.set("Enter your Team Information")

teamNameEntry.insert(0, "Enter Team Name")
teamNameEntry.bind("<FocusIn>", tempTextTeam)

continueButton = Button(Content,
                        text="Continue",
                        command=lambda: [
                            createTeamCommand(),
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
                            command=selectOptionCommand).grid(row=2, column=0)


def testButtonCommand():
    list = Content.grid_slaves()
    for l in list:
        l.destroy()

    testButton = Button(Content, text="Test", command=testButtonCommand)
    testButton.grid(row=0, column=4)


#main
root.mainloop()
