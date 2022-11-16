from task import task
class member:
  taskList = []
  #Initialization of a member of the team
  def __init__(self, name_in, role_in):
    self.name = name_in
    self.role = role_in

  #Set member's name
  def set_name(self, name_in):
    self.name = name_in
  #str
  def __str__(self):
    return f"{self.name} {self.role}"

  #Get member's name
  def get_name(self):
    return self.name
  
  #Set member's role
  def set_role(self, role_in):
    self.role = role_in

  #Get member's role
  def get_role(self):
    return self.role

    
