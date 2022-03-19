# -*- coding: utf-8 -*-
"""
--------------------------------------
Project Name: pyGames
File Name: helloRabbit.py
Author: Onway
Create Date: 2022/3/16
--------------------------------------
"""
import pygame
from pygame.locals import *
import math
import random
# 初始化
pygame.init()
# 设置宽高
screen = pygame.display.set_mode((640, 480))
# Keys用来记录按键情况，依次代表WASD
keys = [False, False, False, False]
# playerpos表示玩家的位置
playerPos = [100, 100]
# 跟踪玩家的精度变量，记录了射出的箭头数和射中的獾的数量
# 之后会用到这些信息记算玩家的射击精准度
acc = [0, 0]
# 跟踪箭头变量
arrows = []
# 定义了一个计时器，每隔一段时间就生成一只獾 每一帧减少badtime直到为零
badtimer = 100
badtimer1 = 0
badguys = [[640, 480]]
healthvalue = 194
pygame.mixer.init()
# 加载图片
player = pygame.image.load("resources\images\dude.png")
# 再加载一些背景
grass_img = pygame.image.load('resources\images\grass.png')
castle_img = pygame.image.load('resources\images\castle.png')
# 加载箭头图片
arrow_img = pygame.image.load('resources\images\\bullet.png')
# 加载獾的图片
badguyimg1 = pygame.image.load('resources\images\\badguy.png')
badguyimg = badguyimg1
# 加载城堡健康值的图片
healthbar_img = pygame.image.load('resources\images\healthbar.png')
health_img = pygame.image.load('resources\images\health.png')
# 加载胜利和失败的图片
win_img=pygame.image.load('resources\images\youwin.png')
lose_img=pygame.image.load('resources\images\gameover.png')
# 加载音乐
hit=pygame.mixer.Sound('resources\\audio\explode.wav')
enemy=pygame.mixer.Sound('resources\\audio\enemy.wav')
shoot=pygame.mixer.Sound('resources\\audio\shoot.wav')
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources\\audio\moonlight.wav')
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(0.25)
running=True
exitcode=False
# 不断循环
while running:
	# 画之前清除屏幕
	screen.fill(0)
	# 将风景加载到屏幕上
	for x in range(640 // grass_img.get_width() + 1):
		for y in range(480 // grass_img.get_height() + 1):
			screen.blit(grass_img, (x * 100, y * 100))
	screen.blit(castle_img, (0, 30))
	screen.blit(castle_img, (0, 135))
	screen.blit(castle_img, (0, 240))
	screen.blit(castle_img, (0, 345))
	# 首先获得鼠标和玩家的位置，然后通过atan2函数计算出弧度和角度
	# 当兔子被旋转时，位置会被改变
	# 所以需要计算玩家的新位置，将其在屏幕上显示出来
	# 在屏幕得的（100,100）位置加载小兔子的图片
	mouse_Position = pygame.mouse.get_pos()
	angle = math.atan2(mouse_Position[1] - (playerPos[1] + 23), mouse_Position[0] - (playerPos[0] + 26))
	playerrot = pygame.transform.rotate(player, 360 - angle * 57.29)
	playerpos1 = (playerPos[0] - playerrot.get_rect().width / 2, playerPos[1] - playerrot.get_rect().height / 2)
	screen.blit(playerrot, playerpos1)
	# 在屏幕上画出箭头 velx和vely使用的基本三角法计算，10是箭头的的速度
	# if语句检查箭头是否越界，如果是则删除箭头，第二个循环遍历箭头并以正确的旋转方式绘制他们
	index = 0
	for bullet in arrows:
		# index=0
		velx = math.cos(bullet[0]) * 2
		vely = math.sin(bullet[0]) * 2
		bullet[1] += velx
		bullet[2] += vely
		if bullet[1] < -64 or bullet[0] > 640 or bullet[2] < -64 or bullet[2] > 480:
			arrows.pop(index)
		index += 1
		# print(index)
		for projectile in arrows:
			arrow1 = pygame.transform.rotate(arrow_img, 360 - projectile[0] * 57.29)
			screen.blit(arrow1, (projectile[1], projectile[2]))
	# 更新并显示这些坏蛋
	# 检查badtimer是否为0，若为0，则新建一个獾并将badtimer恢复
	# 第一个循环检查獾的坐标，检查是否超出边界，若超出则删除
	# 第二个循环是画出所有的獾
	if badtimer == 0:
		badguys.append([640, random.randint(50, 430)])
		badtimer = 100 - (badtimer1 * 2)
		if badtimer1 >= 35:
			badtimer1 = 35
		else:
			badtimer1 += 5
	index = 0
	for badguy in badguys:
		if badguy[0] < -64:
			badguys.pop(index)
		badguy[0] -= 2
		# print(badguy[0])
		# 獾可以炸掉城堡 如果獾的x坐标离左边少于64 就删除坏蛋并减少玩家的健康值 减少值为5,20之间的一个随机数
		badrect = pygame.Rect(badguyimg.get_rect())
		badrect.top = badguy[1]
		badrect.left = badguy[0]
		if badrect.left < 64:
			# print(badrect.left)
			hit.play()
			healthvalue -= random.randint(5, 20)
			badguys.pop(index)
		# 循环所有的坏蛋和箭头来判断是否有獾和箭头碰撞
		# 如果碰撞上，删除獾，删除箭头，并且在精确的变量里加1
		# 使用了pygame的内建功能来检查两个矩形是否交叉
		index_arrow = 0
		for bullet in arrows:
			bulletrect = pygame.Rect(arrow_img.get_rect())
			bulletrect.top = bullet[2]
			bulletrect.left = bullet[1]
			if badrect.colliderect(bulletrect):
				enemy.play()
				acc[0] += 1
				badguys.pop(index)
				arrows.pop(index_arrow)
			index_arrow += 1
		index += 1
	for badguy in badguys:
		# print(badguy)
		screen.blit(badguyimg, badguy)
	# 添加一个计时 使用pygame默认的24号字体来显示时间信息
	font = pygame.font.SysFont('arial', 24)
	survivedtext = font.render(
		str((90000-pygame.time.get_ticks() )//60000) + ":" + str((90000-pygame.time.get_ticks() )//1000 % 60).zfill(2), True,
		(0, 0, 0))
	textrect = survivedtext.get_rect()
	textrect.topright = [635, 5]
	screen.blit(survivedtext, textrect)
	# 画出城堡健康值 首先画一个全红的生命值条 然后根据城堡的生命值往里边添加绿色
	screen.blit(healthbar_img, (5, 5))
	for health1 in range(healthvalue):
		screen.blit(health_img, (health1 + 8, 8))
	# 更新屏幕
	pygame.display.flip()
	# 检查一些新的事件 如果有退出命令，则终止程序的运行
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == K_w:
				keys[0] = True
			if event.key == K_a:
				keys[1] = True
			if event.key == K_s:
				keys[2] = True
			if event.key == K_d:
				keys[3] = True
		if event.type == pygame.KEYUP:
			if event.key == K_w:
				keys[0] = False
			if event.key == K_a:
				keys[1] = False
			if event.key == K_s:
				keys[2] = False
			if event.key == K_d:
				keys[3] = False
		# 当用户单击鼠标时，需要发射箭头
		if event.type == pygame.MOUSEBUTTONDOWN:
			shoot.play()
			position = pygame.mouse.get_pos()
			acc[1] += 1
			arrows.append(
				[math.atan2(position[1] - (playerpos1[1] + 23), position[0] - (playerpos1[0] + 26)), playerpos1[0] + 23,
				 playerpos1[1] + 23])
		# 检查鼠标是否单击，如果是则根据鼠标位置并根据玩家旋转的位置和光标位置计算箭头旋转，这个旋转值存在箭头数组中
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	# 移动玩家
	if keys[0]:
		playerPos[1] -= 5
	if keys[1]:
		playerPos[0] -= 5
	if keys[2]:
		playerPos[1] += 5
	if keys[3]:
		playerPos[0] += 5
	badtimer -= 0.5
	# 失败成功的条件 如果时间到了90s，停止运行游戏， 如果城堡被毁，停止运行
	# 精确度一直计算
	if pygame.time.get_ticks()>=90000:
		running =False
		exitcode=True
	if healthvalue<=0:
		running = False
		exitcode = False
	if acc[1]!=0:
		accuracy=acc[0]*1.0/acc[1]*100
		accuracy=("%.2f"%accuracy)
	else:accuracy=0
if exitcode==False:
	pygame.font.init()
	font=pygame.font.SysFont('arial',24)
	text=font.render('Accuracy:'+str(accuracy)+"%",True,(255,0,0))
	textrect=text.get_rect()
	textrect.centerx=screen.get_rect().centerx
	textrect.centery=screen.get_rect().centery+24
	screen.blit(lose_img,(0,0))
	screen.blit(text,textrect)
else:
	pygame.font.init()
	font=pygame.font.SysFont('arial',24)
	text=font.render('Accuracy:'+str(accuracy)+"%",True,(255,0,0))
	textrect = text.get_rect()
	textrect.centerx = screen.get_rect().centerx
	textrect.centery = screen.get_rect().centery + 24
	screen.blit(win_img,(0,0))
	screen.blit(text,textrect)
while True:
	for event in pygame.event.get():
		if event.type==pygame.QUIT :
			pygame.quit()
			exit()
	pygame.display.flip()

