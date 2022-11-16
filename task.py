

class task:
    description = "undecided"
    role = "undecided"
    dueDate = "NA"
    def __init__(self, description, role, dueDate):
        self.description = description
        self.role = role
        self.dueDate = dueDate
    def __str__(self):
        return f"{self.description} {self.role} {self.dueDate}"
