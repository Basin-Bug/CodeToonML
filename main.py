from concurrent.futures import ProcessPoolExecutor #マルチプロセス
from Game import Game
from network import network

import sys, os
import time
import numpy as np
import matplotlib.pyplot as plt
import random

game = Game()
pg = network(25 * 2, 110, 50 * 4)


running_reward = 0
prev = 0
episode_number = 0
episode_num = []
running_new = []
max_reward = 0



def solve_input(game, inp):

  if inp == "rewards":
    print(game.reward)
    solve_input(game, str(input()))
  elif inp == "passwords":
    print(game.is_locked)
    solve_input(game, str(input()))
  nums = [0] * 4
  p = 0
  for i in range(len(inp)):
    if "0" <= inp[i] <= "9":
      if p < 2:
        nums[p] = int(inp[i])
        p += 1
      else:
        if nums[p] >= 1000 and p == 2:
          p += 1
        nums[p] = nums[p] * 10 + int(inp[i])

  if "attack" in inp:
    if "enemy" not in inp:
      game.is_enemy = False
    if nums[-2] == 0:
      game.attack(nums[0], nums[1], True)
    else:
      game.attack2(nums[0], nums[1], nums[2], True)
  elif "lock" in inp:
    if "enemy" not in inp:
      game.is_enemy = False
    if nums[-1] == 0:
      game.lock(nums[0], nums[1], nums[2], True)
    else:
      game.lock2(nums[0], nums[1], nums[2], nums[3], True)
  return game.calc_reward()

def process_action(game, action):
  print("AI:", end = "")
  choice = action // 50
  i = (action % 50) // 5
  j = (action % 50) % 5
  if choice == 0:
    if i <= 4:
      get_agent_move = "attack(enemy.memory[{}][{}]);".format(i, j)
    else:
      get_agent_move = "attack(memory[{}][{}]);".format(i - 5, j)
    game.attack(i, j, False)
    
  elif choice == 1:
    r = random.randint(1000, 10000)
    if i <= 4:
      get_agent_move = "attack(enemy.memory[{}][{}], {});".format(i, j, r)
    else:
      get_agent_move = "attack(memory[{}][{}], {});".format(i - 5, j, r)
    game.attack2(i, j, r, False)
    
  elif choice == 2:
    r = random.randint(1000, 10000)
    if i <= 4:
      get_agent_move = "enemy.memory[{}][{}].setPass({});".format(i, j, r)
    else:
      get_agent_move = "memory[{}][{}].setPass({})".format(i - 5, j, r)
    game.lock(i, j, r, False)
    
  elif choice == 3:
    bef = game.is_locked[5 * i + j]
    r = random.randint(1000, 10000)
    if i <= 4:
      get_agent_move = "enemy.memory[{}][{}].setPass({}, {});".format(i, j, bef, r)
    else:
      get_agent_move = "memory[{}][{}].setPass({}, {})".format(i - 5, j , bef, r)
    game.lock2(i, j, bef, r, False)
    
  return get_agent_move


def get_input():
  inp = str(input())
  reward = solve_input(game, inp)

def agent_move():
  aprob = pg.forward(game.reward)
  action = pg.select_action(aprob)
  agent_mv = process_action(game, action)
  reward = game.calc_reward()
  time.sleep(5)
  
  return agent_mv
while 1:
  if game.calc_reward == 50 or game.calc_reward == -50:
    print("#####GAME OVER#####")
    game.reset()
    episode_number += 1
    max_reward = max(max_reward, game.calc_reward)
  if episode_number == 2000:
    break
  get_input()
  move = agent_move()
  print(move)  
  print("agent's reward: {}".format(game.calc_reward()))
