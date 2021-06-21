import pygame
from random import *

# 레벨에 맞게 설정
def setup(level):
    global display_time

    # 얼마 동안 숫자를 보여줄지
    display_time = 5 - (level // 3)
    display_time = max(display_time, 1)

    number_count = (level // 3) + 5
    number_count = min(number_count, 20)

    shuffle_grid(number_count)

# 숫자 섞기
def shuffle_grid(number_count):
    rows = 5
    columns = 9

    cell_size = 130
    button_size = 110
    screen_left_margin = 55
    screen_top_margin = 20

    # 5 x 9 리스트 생성
    grid = [[0 for col in range(columns)] for row in range(rows)]

    number = 1 
    while number <= number_count:
        row_idx = int(randrange(0, rows))
        col_idx = int(randrange(0, columns))

        if grid[row_idx][col_idx] == 0:
            grid[row_idx][col_idx] = number
            number += 1

            # 현재 grid cell 위치 기준 x, y 위치 구함
            center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)

            # 숫자 버튼 만들기
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)

            number_buttons.append(button)

    




# 시작 화면
def display_start_screen():
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)

    msg = game_font.render(f"{curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=start_button.center)

    screen.blit(msg, msg_rect)

def check_buttons(pos):
    global start, start_ticks

    if start:
        chect_number_buttons(pos)
    elif start_button.collidepoint(pos):
        start = True
        start_ticks = pygame.time.get_ticks() # 타이머 시작


def chect_number_buttons(pos):
    global start, hidden, curr_level

    for button in number_buttons:
        if button.collidepoint(pos): # 올바른 숫자 클릭
            print("Corrent")
            del number_buttons[0]
            if not hidden:
                hidden = True # 숨김
        else: # 잘못된 숫자 클릭
            game_over()
        break
    # 다음 레벨로
    if len(number_buttons) == 0:
        start = False
        hidden = False
        curr_level += 1
        setup(curr_level)

# 게임 종료
def game_over():
    global running
    running =False

    msg = game_font.render(f"Your level is {curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=(screen_windth/2, screen_height/2))

    screen.fill(BLACK)
    screen.blit(msg, msg_rect)



# 게임 화면 보여주기
def display_game_screen():
    global hidden

    if not hidden:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        if elapsed_time > display_time:
            hidden = True
    for idx, rect in enumerate(number_buttons, start=1):
        if hidden:
            # 버튼 사각형 그리기
            pygame.draw.rect(screen, WHITE, rect)
        else:
            # 숫자 텍스트
            cell_text = game_font.render(str(idx), True, WHITE)
            text_rect = cell_text.get_rect(center=rect.center)
            screen.blit(cell_text, text_rect)

# 기본값
pygame.init()
screen_windth = 1280 # 가로 크기
screen_height = 720 # 세로 크기
screen = pygame.display.set_mode((screen_windth, screen_height))
pygame.display.set_caption("Memory Game")
game_font = pygame.font.Font(None, 120)

# 시작 버튼
start_button = pygame.Rect(0, 0, 120, 120)
start_button.center = (120, screen_height - 120)

# RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

# 유저가 클릭해야하는 버튼
number_buttons = [] 
# 현재 레벨
curr_level = 1
# 숫자를 보여주는 시간
display_time = None
# 시간 계산
start_ticks = None

# 게임 시작 여부
start = False
# 숫자 숨김 여부 (사용자가 1을 클릭했거나 시간 초과했을 때)
hidden = False

# 게임 시작 전에 설정 함수 실행
setup(curr_level)

# 게임 루프
running = True # 게임이 실행중인지
while running:
    click_pos = None

    # 이벤트
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 창이 닫히면
            running = False # 실행중 X
        elif event.type == pygame.MOUSEBUTTONUP: # 클릭시
            click_pos = pygame.mouse.get_pos()
            print(click_pos)
    # 화면 색
    screen.fill(BLACK)

    if start:
        display_game_screen() # 게임 화면
    else:
        display_start_screen() # 시작 화면
    
    # 클릭하면
    if click_pos:
        check_buttons(click_pos)
    
    # 화면 업데이트
    pygame.display.update()

# 5초 딜레이 후 종료
pygame.time.delay(5000)
pygame.quit()