from click import command
from tkcalendar import Calendar
from member import member
from task import task
from tkinter import *

#initializes window
root = Tk()
root.option_add("*Font", 'Sans 20')
root.configure(bg='#202020')
root.title("TeamMate")
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
#setting tkinter window size
root.geometry("%dx%d" % (width, height))

Header = Frame(root, bg='black', height=30)
Content = Frame(root, pady=10)
Footer = Frame(root)

instruction = StringVar()
instruction.set("Main Menu")
InstructionLabel = Label(Header,
                         textvariable=instruction,
                         bg='grey',
                         fg='white',
                         bd= 3
                         ).pack(),
                         
Header.config(bg='grey')
Header.pack(fill='both')
Content.pack()

#Entries
nameEntry = Entry(Content,  bg="#202020", fg='white',borderwidth=5)
roleEntry = Entry(Content, bg='#363636', fg='white')
teamNameEntry = Entry(Content, bg="#202020", fg='white',borderwidth=5)
descriptionEntry = Entry(Content,  bg="#202020", fg='white',borderwidth=5)
numTeamMembersEntry = Entry(Content, width=5,  bg="#202020", fg='white',borderwidth=5)
taskListLabel = Label(Content)

cal = Calendar(Content, font="Sans 12",  selectmode='day')
select = StringVar()
getScheduleDropDownSelection = StringVar()
DropDownSelection2 = StringVar()
dropDownSelection3 = StringVar()
dropDownSelection4 = StringVar()
dropDownSelection5 = StringVar()

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
    instruction.set("Team Created!")


def createTeamCommand():
    global teamName
    global numTeamMembers
    global i

    teamName = teamNameEntry.get()
    numTeamMembers = numTeamMembersSpinBox.get()
    continueButtonAddTeamsMembers = Button(
        Content,
        width= 10,
        bg="#363636",
        fg='white',
        text="Add Member",
        command=lambda:
        [addTeamsMembers(),
         continueButtonAddTeamsMembers.grid_remove(),nameLabel.grid_remove(), roleLabel.grid_remove()])
    continueButtonAddTeamsMembers.grid(row=1, column=0, padx=30)
    nameLabel = Label(Content, text="Name",  bg="#202020", fg='white')
    nameLabel.grid(row=0, column=1)
    roleLabel = Label(Content, text="Role", bg="#202020", fg='white')
    roleLabel.grid(row=0, column=2)
    for i in range(int(numTeamMembers)):
        en = Entry(Content,  bg="#202020", fg='white',borderwidth=5)
        en2 = Entry(Content,  bg="#202020", fg='white',borderwidth=5)
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
    name = getScheduleDropDownSelection.get()
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
    doneButton = Button(Content, width=10,
                        bg="#363636",
                        fg='white',
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
    nameToFind = DropDownSelection2.get()
    i = 0
    
    for i in range(len(teamList)):
        if(teamList[i].name == nameToFind):
            indexToDisplayTaskListFor = i
    menu = OptionMenu(Content, dropDownSelection3, *teamList[i].taskList)
    menu.config( bg="#202020", fg='white')
    menu.grid(row=0, column=2, padx=30)
    
    completeTaskButton = Button(Content, width=10,
        bg="#363636",
        fg='white',
        text="Complete",
         command= lambda: [
            deleteTaskFromList(indexToDisplayTaskListFor),
            completeTaskButton.grid_remove(),
            menu.grid_remove()
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

def changeRoleCommand():
    newRoleEntry = Entry(Content,  bg="#202020", fg='white',borderwidth=5)
    newRoleEntry.grid(row=0, column=1)
    finishChangeRoleButton = Button(Content, bg="#363636", width=10,
        fg='white',text="Set New Role", command=
        lambda: [changeRole(dropDownSelection5.get(),newRoleEntry.get()),
        newRoleEntry.grid_remove(),
        finishChangeRoleButton.grid_remove()
        ])
    finishChangeRoleButton.grid(row=1, column=0)
def changeRole(name, role):
    i = 0
    for i in range(len(teamList)):
        if(teamList[i].name == name):
            teamList[i].role = role
def selectOptionCommand():
    currentOption = dropDownSelection.get()
    list = Content.grid_slaves()
    count = 0
    for l in list:
        l.destroy()

    newSelectOptionButton = Button(Content, width=10,text="Select Option", command=selectOptionCommand, bg='#363636', fg='white')
    newSelectOptionButton.grid(row=1, column=0, pady=50)
    newDropDown = OptionMenu(Content, dropDownSelection, *options)
    newDropDown.config( bg="#202020", fg='white')
    dropDownSelection.set(currentOption)
    newDropDown.grid(row=0, column=0)
    

    if dropDownSelection.get() == options[0]:
        instruction.set("Select Member")
        dropDownSelection4.set("Member to Remove")
        i = 0
        roleList1 = []
        nameList1 = []
        for i in range(len(teamList)):
            roleList1.append(teamList[i].role)
            nameList1.append(teamList[i].name)
        menu = OptionMenu(Content, dropDownSelection4, *nameList1)
        menu.config( bg="#202020", fg='white')
        menu.grid(row=0, column=1, padx=30)
        continueButton = Button(
            Content,
            width=10,
            bg="#363636",
            fg='white',
            text="Remove",
            command= lambda:
            [removeMemberCommand(),
            continueButton.grid_remove(),
            menu.grid_remove(),
            instruction.set("Member Removed!")
            ]
        )
        continueButton.grid(row=1, column=0)

    if dropDownSelection.get() == options[1]:
        instruction.set("Enter Member Information")
        continueButton = Button(
            Content,
            width=10,
            bg="#363636",
            fg='white',
            text="Add Member",
            command=lambda:
            [addMemberCommand(),
             continueButton.grid_remove(),
             instruction.set("Member Added!")]
            )
        continueButton.grid(row=1, column=0)
        nameEntry.grid(row=0, column=1)
        roleEntry.grid(row=0, column=2)

    if dropDownSelection.get() == options[2]:
        instruction.set("Change Role")
        i = 0
        roleList1 = []
        nameList1 = []
        for i in range(len(teamList)):
            roleList1.append(teamList[i].role)
            nameList1.append(teamList[i].name)
        menu = OptionMenu(Content, dropDownSelection5, *nameList1)
        menu.config( bg="#202020", fg='white')
        menu.grid(row=0, column=1, padx=30)
        dropDownSelection5.set("Choose Member Role to Change")
        continueButton = Button(Content, text="Edit Role", bg="#363636", width=10,
        fg='white', command=lambda: 
            [changeRoleCommand(),
            menu.grid_remove(),
            continueButton.grid_remove(),
            instruction.set("Role Changed!")
            ])
        continueButton.grid(row=1, column=0)

    if dropDownSelection.get() == options[3]:
        getScheduleDropDownSelection.set("Select Member to View")
        i = 0
        roleList1 = []
        nameList1 = []
        for i in range(len(teamList)):
            roleList1.append(teamList[i].role)
            nameList1.append(teamList[i].name)
        menu = OptionMenu(Content, getScheduleDropDownSelection, *nameList1)
        menu.config( bg="#202020", fg='white')
        print(str(nameList1))
        menu.grid(row=3, column=2, padx=30)
        instruction.set("Select a Date")
        continueButton = Button(
            Content,
            bg="#363636",
            width=10,
            fg='white',
            text="View Schedule",
            command=lambda:
            [getScheduleCommand(),
             continueButton.grid_remove()])
        continueButton.grid(row=1, column=0)
        cal.grid(row=0, column=1, rowspan=2, columnspan=2)

    if dropDownSelection.get() == options[4]:
        select.set("Select Role for Task")
        i = 0
        roleList1 = []
        nameList1 = []
        for i in range(len(teamList)):
            roleList1.append(teamList[i].role)
            nameList1.append(teamList[i].name)
        noRepeatRoleList = [*set(roleList1)]
        menu = OptionMenu(Content, select, *noRepeatRoleList)
        menu.config( bg="#202020", fg='white')
        menu.grid(row=0, column=2, padx=30)
        instruction.set("Enter Task")
        cal.grid(row=1, column=2)
        descriptionEntry.grid(row=0, column=1)

        def tempTextTask(e):
            descriptionEntry.delete(0, "end")

        descriptionEntry.insert(0, "Enter Task Description")
        descriptionEntry.bind("<FocusIn>", tempTextTask)

        continueButton = Button(
            Content,
            bg="#363636",
            fg='white',
            width=10,
            text="Add Task",
            command=lambda:
            [addTaskCommand(),
             continueButton.grid_remove(),
             instruction.set("Task Added!")])
        continueButton.grid(row=1, column=0)

    if dropDownSelection.get() == options[5]:
        DropDownSelection2.set("Which teamMember?")
        dropDownSelection3.set("Which Task?")
        i = 0
        roleList1 = []
        nameList1 = []
        for i in range(len(teamList)):
            roleList1.append(teamList[i].role)
            nameList1.append(teamList[i].name)
        menu = OptionMenu(Content, DropDownSelection2, *nameList1)
        menu.config( bg="#202020", fg='white')
        menu.grid(row=0, column=2, padx=30)
        continueButton = Button(
            Content,
            bg="#363636",
            width=10,
            fg='white',
            text="Select Member",
            command= lambda:
            [completeTaskCommand(),
            continueButton.grid_remove(),
            menu.grid_remove(),
            instruction.set("Task Completed!")
            ]
        )
        continueButton.grid(row=1, column=0)


options = [
    "Remove Member",
    "Add Member",
    "Change Role",
    "View Schedule",
    "Add Task",
    "Complete Task"
]
dropDownSelection = StringVar()
dropDownSelection.set(options[0])
dropDown = OptionMenu(Content, dropDownSelection, *options)
dropDown.config( bg="#202020", fg='white')



def tempTextTeam(e):
    teamNameEntry.delete(0, "end")



teamNameEntry.insert(0, "Enter Team Name")
teamNameEntry.bind("<FocusIn>", tempTextTeam)

continueButton = Button(Content, 
                        text="Continue",
                        bg='#363636',
                        fg= 'white',
                        width=10,
                        command=lambda: [
                            createTeamCommand(),
                            continueButton.grid_remove(),
                            numTeamMembersEntry.grid_remove(),
                            numTeamMembersSpinBox.grid_remove(),
                            teamNameEntry.grid_remove()
                        ])
numTeamMembersSpinBox = Spinbox(Content, from_=1, to=100, width=5, bg="#202020", fg='white')
def welcomeCommand():
    continueButton.grid(row=0, column=0)
    teamNameEntry.grid(row=0, column=1, padx=50)
    numTeamMembersSpinBox.grid(row=0, column=3)
    instruction.set("Enter Team Information")


def startUp():
    dropDown.grid(row=0, column=0)
    dropDownButton = Button(Content, text="Select Option", bg="#363636", fg='white', width=10,
                            command=selectOptionCommand)
    dropDownButton.grid(row=2, column=0)


welcomeLabel = Label(Content, text="Welcome to teamMate!", relief= "flat", font=('Sans open', 20), bg="#202020", fg="white")
welcomeLabel.grid(row=0, column=0, pady=40)
Content.config(bg="#202020")
welcomeButton = Button(Content, text= "Get Started", font=('Sans serif',20), bg="#363636", fg= "white", borderwidth=3, width=10,
    command=lambda: [welcomeCommand(),
        welcomeButton.grid_remove(),
        welcomeLabel.grid_remove()])
welcomeButton.grid(row=1, column=0, pady=60)

root.mainloop()
