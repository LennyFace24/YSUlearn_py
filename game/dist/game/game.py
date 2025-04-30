import pygame 
import os

## 变量初始化
pygame.init()
color = (111,220,249)

## 画布大小
canvas = pygame.display.set_mode((900,900))

## 标题
pygame.display.set_caption('跨栏游戏')

## 图片读取
bg = pygame.image.load("bg.png").convert()
obstacle = pygame.image.load("obstacle.png").convert_alpha()
jump_player = pygame.image.load("jump.png").convert_alpha()

frameRect = bg.get_rect()
clock = pygame.time.Clock()

## 索引
i = 0 ## 控制背景循环
k = 0 ## 控制人物循环
j = 0 ## 控制障碍循环

## 参数
scale_factor = 4 ## 人物缩放比率
obs_scale_factor = 1.5 ## 障碍缩放比率
player_yoffset = 0 ## 人物跳跃偏移
max_speed = 21 ## 人物最大速度
player_yspeed = max_speed ## 人物跳跃速度
is_jumping = False ## 是否在跳跃
speed_change = False ## 速度是否需要改变
now_y = 630 ## 现在的y坐标
score = 0 ## 玩家分数

## 文字
font = pygame.font.SysFont('SimHei', 72) ## 大字体
small_font = pygame.font.SysFont('SimHei', 36) ## 小字体
gameover_title = font.render("游戏结束", True, (255, 0, 0)) ## 结束标题

## 动态人物
frames = []
obstacles = []

## 障碍处理
obstacle_size = obstacle.get_size()
obs_new_size = (int(obstacle_size[0] * obs_scale_factor), int(obstacle_size[1] * obs_scale_factor))
scaled_obstacle = pygame.transform.scale(obstacle,obs_new_size)

## 人物大小处理
for i in range(1,len(os.listdir("playerimg"))+1):
    frame = pygame.image.load(f"./playerimg/{i}.png").convert_alpha()
    original_size = frame.get_size()
    new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
    scaled_frame = pygame.transform.scale(frame, new_size)
    frames.append(scaled_frame)

size_jump = jump_player.get_size()
new_size_jump = (int(size_jump[0] * scale_factor), int(size_jump[1] * scale_factor))
scaled_jump_player = pygame.transform.scale(jump_player,new_size_jump)

## 关闭界面条件
exit = False
gameover = False

while not exit:
    ## 关闭界面
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN and player_yspeed == max_speed:
            if event.key == pygame.K_SPACE and not is_jumping and not gameover:  # 空格键跳跃
                is_jumping = True  # 初始向上速度
                speed_change = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and gameover:  # 按R键重新开始
              # 重置游戏状态
              i = k = j = 0
              player_yspeed = max_speed
              score = 0
              now_y = 630
              gameover = False
    
    if not gameover:
    ## 坐标
        obs_x = 1000 - 8*j

        ## 加载图片
        canvas.blit(bg,(-i,0))
        canvas.blit(bg,(frameRect.width-i,0))

        if player_yspeed < max_speed:
            now_y = now_y + player_yspeed
            canvas.blit(scaled_jump_player,(150,now_y))
        else:
            canvas.blit(frames[k % 14],(150,now_y))

        canvas.blit(scaled_obstacle,(frameRect.width - 8 * j,700))
        canvas.blit(scaled_obstacle,(frameRect.width - 8 * j + 800,700))
        canvas.blit(scaled_obstacle,(frameRect.width - 8 * j + 1600,700))
        canvas.blit(scaled_obstacle,(frameRect.width - 8 * j + 2400,700))
        canvas.blit(scaled_obstacle,(frameRect.width - 8 * j + 2900,700))
        canvas.blit(scaled_obstacle,(frameRect.width - 8 * j + 4000,700))
        
        ## 分数显示
        real_score = score // 13
        score_text = font.render(f"SCORE:{real_score} ",True,(255,0,0))
        canvas.blit(score_text,(500,200))

        ## 跳跃判断
        if is_jumping:
            player_yspeed = -max_speed
            now_y = 630
            is_jumping = False
        if player_yspeed < max_speed:
            player_yspeed += 1
        i = (i + 1) % frameRect.width
        k = k + 1
        j = (j + 1) % (frameRect.width / 2)

        ## 是否撞上障碍物
        # 扩大检测范围并增加容错
        if (any(100 <= (frameRect.width-8*j+offset) <= 250 for offset in [0,800,1600,2400,2900,4000]) 
             and (500 <= now_y <= 630) ):
             gameover = True
        if (any(150 <= (frameRect.width-8*j+offset) <= 250 for offset in [0,800,1600,2400,2900,4000]) 
             and not gameover ):
            score += 1
    else:
        canvas.blit(bg, (0, 0))

        text = font.render("游戏结束", True, (255, 255, 255))
        final_score = font.render(f"你一共跨过了{real_score}个跨栏！", True, (255, 255, 255))
        restart = pygame.font.SysFont('SimHei', 36).render("按R键重新开始", True, (255, 255, 255))
        canvas.blit(text, (450 - text.get_width()//2, 200))
        canvas.blit(final_score, (450 - final_score.get_width()//2, 300))
        canvas.blit(restart, (450 - restart.get_width()//2, 800))
    pygame.display.flip()
    
    ## xunhuan shijian 
    clock.tick(60)
