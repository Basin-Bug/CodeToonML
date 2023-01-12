from concurrent.futures import ProcessPoolExecutor #マルチプロセス
from Game import Game
from network import network

import sys, os
import time
import numpy as np
import matplotlib.pyplot as plt

game = Game()
pg = network(25 * 2, 110, 25 * 5)


running_reward = 0
prev = 0
episode_number = 0
episode_num = []
running_new = []
max_reward = 0

def solve_input(game, inp):
  nums = [0] * 4
  for i in range(len(inp)):
    p = 0
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
    if nums[-2] != 0:
      game.attack(nums[0], nums[1])
    else:
      game.attack(nums[0], nums[1], nums[2])
  elif "connect" in inp:
    game.connect(nums[0], nums[1])
  elif "lock" in inp:
    if "enemy" not in inp:
      game.is_enemy = False
    if nums[-1] == 0:
      game.lock(nums[0], nums[1], nums[2])
    else:
      game.lock(nums[0], nums[1], nums[2], nums[3])
  print(game.reward)
  return game.calc_reward()


def get_input():
  inp = str(input())
  reward = solve_input(game, inp)
  return reward

def agent_move(rewards):
  aprob = pg.forward(rewards)
  action = pg.select_action(aprob)
  reward = game.calc_reward()
  
while 1:
  if game.calc_reward == 50 or game.calc_reward == -50:
    print("#####GAME OVER#####")
    game.reset()
    episode_number += 1
    max_reward = max(max_reward, game.calc_reward)
  if episode_number == 2000:
    break
  get_input()
  #print(game.calc_reward())
