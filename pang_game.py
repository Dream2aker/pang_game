# 1. 모든 공을 없애면 게임 종료 (성공)
# 2. 캐릭터는 공에 닿으면 게임 종료 (실패)
# 3. 시간 제한 99추 초과 시 게임 종료 (실패)

import os
import pygame
########################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init() 

# 화면 크기 설정
screen_width = 640 # 가로 크기
screen_height = 480 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height)) # pygame.display.set_mode는 pygame을 사용하기 위해 반드시 필요한 사항

# 화면 타이틀 설정
pygame.display.set_caption("Bubble Star") # 게임 이름 display.set_caption pygame 관련 필수 사항

# FPS
clock = pygame.time.Clock()
########################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 폰트, 속도 등)
current_path = os.path.dirname(__file__) # 현재 파일 (frame_background_stage_character.py)의 위치 반환
image_path = os.path.join(current_path, "images") # images 폴더 위치 반환. # 이미지 위치를 지정해준 것. 

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "back.png"))

# stage 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # stage의 높이 위에 캐릭터를 두기 위해 사용.

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 5

# 무기 만들기

weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기의 이동 속도
weapon_speed = 10

# 공 만들기
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),        
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]
# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3에 해당하는 값. 즉, 0은 balloon1, 1d은 balloon2 ...
# 위로 올라가는 효과를 위해 위와 같이 - y 값이 사용.

# 공들
balls = []

balls.append({
    "pos_x" : 50, # 공의 x 좌표
    "pos_y" : 50, # 공의 y 좌표
    "img_idx" : 0, # 공의 이미지 인덱스, balloon 1-4, 0은 ballon 1이지
    "to_x": 3, # x축 이동 방향, -3이면 왼쪽으로, 3이면 오른쪽으로
    "to_y": -6, # y축 이동 방향,
    "init_spd_y": ball_speed_y[0]}) # y 최초 속도.

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# Font 정의
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks() # 시작 시간 정의

# 게임 종료 메시지
# Timeout(시간 초과 실패)
# Mission Complete(성공)
# Game Over(캐릭터 공에 맞음, 실패)
game_result = "Game over"

# 이벤트 루프 (위 만든 화면이 프로그램 종료 후 사라지는 것을 방지하기 위함)
running = True 
while running:
    dt = clock.tick(30)  

    # 2. 이벤트 처리 (키보드, 마우스 등) 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT: # 캐릭터를 오른쪽으로
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: # 무기 발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 케릭터 위치 정의 
    character_x_pos += character_to_x

    if character_x_pos < 0: 
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    
    #무기 위치 조정
    # 100, 200, -> 180, 160, 140 .... x축은 무기를 쏜 곳 그대로고, y축은 위로 올라가야하니까 변경 필요.
    # 500, 200 -> 180, 160, 140 ... 다음 x축의 위치는 그대로, y축 변경
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] # 무기 위치를 위로 이동.
    # weapons list에 있는 w값들을 하나씩불러와서 w를 통해 처리(w[0], w[1]에서 speed를 뺀 값)함. 그 값을 다시 weapons에 넣음.
    
    # 천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0] # y 축 값이 0 보다 큰 경우에만 보이라. 0에 천장에 닿는거니까 그 전부터는 보이지 않게.

    # 공 위치 정의 
    for ball_idx, ball_val in enumerate(balls): # enumerate을 이용해 balls dictionary에 있는 index (0, 1..)와 corresponding value 값을 하나씩 가져옴
        ball_pos_x = ball_val["pos_x"] # balls의 value 값을 가져와서 새로 정의
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"] 

        ball_size = ball_images[ball_img_idx].get_rect().size # ball이 총 4개가 있으니 index에 따른 다른 ball을 가져오기 위함.
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로벽에 닿았을 때 공 이동 위치 변경 (튕겨 나오는 효과)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1 # x 축 방향에서 -를 곱해 방향을 전환해주어 공이 튕겨 반대 방향으로 가는 효과를 줌.
        
        # 세로 위치 
        # 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"] # ball 이 스테이지에 팅겨 올라갈때는 속도는 최초속도 즉, -18이지.
        else:
            ball_val["to_y"] += 0.5 # 스테이지에 닿아 초기 속도 후에는 -18부터 점점 속도가 줄면서 올르다가, 어느 순간 +가 되어 다시 내려와 포물선 효과를 줌.
  
        ball_val["pos_x"] += ball_val["to_x"] # 볼에 대한 위치 처리.
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. 충돌 처리

    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls): # enumerate을 이용해 balls dictionary에 있는 index (0, 1..)와 corresponding value 값을 하나씩 가져옴
        ball_pos_x = ball_val["pos_x"] # balls의 value 값을 가져와서 새로 정의
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"] 

        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 캐릭터 충돌 체크
        if character_rect.colliderect(ball_rect):
            running = False
            break
        
        # 공과 무기들 충돌처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            #무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx # 해당 공 없애기 위한 값 설정

                #가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if ball_img_idx < 3: # 공이 0, 1, 2, 3이 있고, 가장 작은 3보다 큰 공들이라면
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect() # 큰 공 다음 공을 가져와야하니 index에 +1 하는 것
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # 공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y 좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스 +1, balloon 1-4, 1은 ballon 2이지
                        "to_x": -3, # x축 이동 방향, -3이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y": -6, # y축 이동 방향,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]}) # y ball_img_idx의 +1한 값의 속도

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # 공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y 좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스 +1, balloon 1-4, 1은 ballon 2이지
                        "to_x": 3, # x축 이동 방향, -3이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y": -6, # y축 이동 방향,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]}) # y ball_img_idx의 +1한 값의 속도

                break
        else: #계속 게임을 진행
            continue # 안쪽 for문 조건이 맞지 않으면 continue. 바깥 for 문 계속 수행
        break # 안쪽 for 문에서 break를 만나면 여기로 진입 가능. 2중 for문을 한번에 탈출.

    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove] # ball_to_remove초기 값은 -1로 이 값이 충돌시에는 -1를 초과함. 이때 관련 index에 해당하는 버블을 제거
        ball_to_remove = -1 # 다시 값 초기화 그래야 다음 프레임시 초기화된 값이 있어야 위 루프를 탐

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤 경우 게임 종료 (성공)
    if len(balls) == 0: # balls list의 length가 0이면 볼이 없을때지.
        game_result = "Mission Complete"
        running = False

    # 5. 화면에 그리기
    screen.blit(background, (0 , 0))    

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos)) #backround 바로 다음으로 위치하여 weapon의 모습이 stage와 character뒤에서 나오도록 조정. 
    
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 시간 초과했다면
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False
    
    pygame.display.update()

# 게임 오버 메시지
msg = game_font.render(game_result, True, (255, 255, 0)) #노란색
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height /2))) # 화면 정 중앙에 글씨 출력
screen.blit(msg, msg_rect) # 메시지를 msg_rect 위치에 출력
pygame.display.update() 

# 2초 대기
pygame.time.delay(2000) 

pygame.quit()  