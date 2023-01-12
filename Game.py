"""
attack(), connect(), lock()実装済み
loop()やfor()は知らないようにしよ
printは報酬と関係ないので実装せず
"""
class Game:
  def __init__(self):
    #前半:AI 後半:User
    self.reward = [-1] * 25 + [1] * 25
    self.is_locked = [None] * 50
    self.is_enemy = True

  def attack(self, i, j, is_user):
    if not is_user:
      if self.is_enemy:
        address = 5 * i + j
        if self.reward[address] != 1:
          self.reward[address] = 1
      else:
        address = 5 * i + j + 25
        if self.reward[address] != 1 and 0 <= i <= 4 and 0 <= j <= 4:
          self.reward[address] = 1
    else:
      if self.is_enemy:
        address = 5 * i + j + 25
      else:
        address = 5 * i + j
      if self.reward[address] != -1 and 0 <= i <= 4 and 0 <= j <= 4:
        self.reward[address] = -1
    self.is_enemy = True
  
  def attack2(self, i, j, password, is_user):
    if not is_user:
      if self.is_enemy:
        address = 5 * i + j
      else:
        address = 5 * i + j + 25
      if self.reward[address] == -1 and self.is_locked[address] == password and 0 <= i <= 4 and 0 <= j <= 4:
        self.reward[address] = 1
        self.is_locked[address] = None
    else:
      if self.is_enemy:
        address = 5 * i + j + 25
      else:
        address = 5 * i + j
      if self.reward[address] == 1 and self.is_locked[address] == password and 0 <= i <= 4 and 0 <= j <= 4:
        self.reward[address] = -1
        self.is_locked[address] = None
    self.is_enemy = True
  
  def lock(self, i, j, password, is_user):
    if not is_user:
      if self.is_enemy:
        address = 5 * i + j
      else:
        address = 5 * i + j + 25
      if self.reward[address] == 1 and self.is_locked[address] == None and 0<= i <= 4 and 0 <= j <= 4:
        self.is_locked[address] = password
    else:
      if self.is_enemy:
        address = 5 * i + j + 25
      else:
        address = 5 * i + j
      if self.reward[address] == -1 and self.is_locked[address] == None and 0 <= i <= 4 and 0 <= j <= 4:
        self.is_locked[address] = password
    self.is_enemy = True
  
  def lock2(self, i, j, password_before, password_after, is_user):
    if not is_user:
      if self.is_enemy:
        address = 5 * i + j
      else:
        address = 5 * i + j + 25
      if self.reward == 1 and self.is_lock[address] == password_before and 0 <= i <= 4 and 0 <= j <= 4:
        self.is_lock[address] = password_after
    else:
      if self.is_enemy:
        address = 5 * i + j + 25
      else:
        address = 5 * i + j
      if self.reward == -1 and self.is_lock[address] == password_before and 0 <= i <= 4 and 0 <= j <= 4:
        self.is_lock[address] = password_after
    self.is_enemy = True

  def connect(self, i, j):
    self.is_enemy = False
  
  def calc_reward(self) -> int:
    return sum(self.reward)

  def reset(self):
    self.reward = [-1] * 25 + [1] * 25
    self.is_locked = [None] * 50
    self.is_enemy = True

