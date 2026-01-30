import pygame
import sys
import skyscraper
import pathlib
import interference
import numpy as np
import subprocess


root = pathlib.Path(__file__).parent.resolve()
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Skyscraper LIVE")
pygame.display.set_icon(pygame.image.load(root / "icon.png"))
clock = pygame.time.Clock()
running = True
x = -4200
y = 0
x_speed = 0
y_speed = 0
gravity = 980
jump_strength = 314
skyscraper_color = (100, 100, 255)
background_color = (135, 206, 235)
player_color = (255, 0, 0)
player_radius = 50
scale = 0.25
skyscraper_polygon = skyscraper.taipei_101()
time = 0.0
started = False
font = pygame.font.Font(str(root / "Ubuntu.ttf"), 24)
spectator_mode = False
key_move = True
physical_strength = 100.0
strength_consumed = False
last_jump_time = pygame.time.get_ticks()
hand_reach = 40
timewarp = 1.0
allow_timewarp = False
video_path = root / "skyscraper-live.mp4"
print(f"Saving video to: {video_path}")


def start_ffmpeg(out_path: str):
    w = screen.get_width()
    h = screen.get_height()
    fps = 48
    # fmt: off
    cmd = [
        "ffmpeg",
        "-y",                          # 覆蓋輸出
        "-f", "rawvideo",              # 輸入是 raw frames
        "-vcodec", "rawvideo",
        "-pix_fmt", "rgb24",           # 我們餵給它 RGB
        "-s", f"{w}x{h}",              # 影像尺寸
        "-r", str(fps),                # 輸入 fps（很重要）
        "-i", "-",                     # 從 stdin 讀
        "-an",                         # 不錄音
        "-vcodec", "libx264",
        "-pix_fmt", "yuv420p",         # 兼容性最好
        "-preset", "ultrafast",        # 越快壓縮越爛但省 CPU
        "-crf", "23",                  # 品質：數字越小越清晰/檔越大
        out_path
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)


def frame_from_pygame_screen(screen) -> np.ndarray:
    # pygame.surfarray.array3d -> (W, H, 3) 要轉成 (H, W, 3)
    frame = pygame.surfarray.array3d(screen)
    frame = np.transpose(frame, (1, 0, 2))  # -> (H, W, 3)
    return frame


def save_frame():
    frame = frame_from_pygame_screen(screen)
    ffmpeg_process.stdin.write(frame.tobytes())


def draw_object(points):
    size = screen.get_size()
    rel_points = [(int((px - x) * scale + size[0] // 2), int((y - py) * scale + size[1] // 2)) for (px, py) in points]
    pygame.draw.polygon(screen, skyscraper_color, rel_points)


def collide(player_pos, points):
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        if line_circle_collision(p1, p2, player_pos, player_radius):
            return True
    return False


def line_circle_collision(p1, p2, center, radius):
    # Vector from p1 to p2
    line_vec = (p2[0] - p1[0], p2[1] - p1[1])
    # Vector from p1 to center
    p1_to_center = (center[0] - p1[0], center[1] - p1[1])
    # Project point onto line
    line_len_sq = line_vec[0] ** 2 + line_vec[1] ** 2
    t = max(0, min(1, (p1_to_center[0] * line_vec[0] + p1_to_center[1] * line_vec[1]) / line_len_sq))
    closest_point = (p1[0] + t * line_vec[0], p1[1] + t * line_vec[1])
    # Distance from closest point to center
    dist_sq = (closest_point[0] - center[0]) ** 2 + (closest_point[1] - center[1]) ** 2
    return dist_sq <= radius**2


def touching_skyscraper():
    for poly in skyscraper_polygon:
        if collide((x, y + player_radius), poly):
            return True
    return False


def touching_ground():
    if y <= 0:
        return True
    # global y
    # touch_a = touching_skyscraper()
    # y += 1
    # touch_b = touching_skyscraper()
    # y -= 2
    # touch_c = touching_skyscraper()
    # y += 1
    # return touch_a and (not touch_b or not touch_c)
    return touching_skyscraper()


def can_jump():
    global player_radius
    raw_radius = player_radius
    player_radius -= 1
    for _ in range(21):
        player_radius += 1
        touch = touching_ground()
        if touch:
            break
    player_radius = raw_radius
    return touch


def jump():
    global y_speed, physical_strength, strength_consumed, last_jump_time
    current_time = pygame.time.get_ticks()
    jump_delay = current_time - last_jump_time
    if can_jump():
        physical_strength -= 0.1 if jump_delay > 500 else jump_delay / 5000.0
        strength_consumed = True
        if physical_strength > 0:
            last_jump_time = current_time
            if jump_delay > 500:
                y_speed = max(jump_strength, y_speed)
            else:
                y_speed = max(jump_strength * (jump_delay / 500.0), 128, y_speed)


def holding_skyscraper():
    global y, player_radius
    raw_y = y
    raw_radius = player_radius
    y -= 1
    player_radius -= 1
    for _ in range(hand_reach + 1):
        y += 1
        player_radius += 1
        if touching_skyscraper():
            y = raw_y
            player_radius = raw_radius
            return True
    y = raw_y
    player_radius = raw_radius
    return False


def move():
    global x, y, x_speed, y_speed, physical_strength, strength_consumed, scale, timewarp
    strength_consumed = False
    keys = pygame.key.get_pressed()
    btns = pygame.mouse.get_pressed()
    x_speed = interference.wind(y, 50800, t=time) * 10
    speed = 100
    move_strength = 0.1
    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
        speed = 50
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        speed = 30
    y_speed -= gravity * dt
    holding = bool(keys[pygame.K_DOWN])
    if holding and holding_skyscraper():
        strength_consumed = True
        if physical_strength > 0:
            physical_strength -= 0.4 * dt
            y_speed = 0
    else:
        if touching_ground():
            y_speed = 0
    if keys[pygame.K_SPACE] or btns[1] or keys[pygame.K_UP]:
        jump()
    if key_move:
        if keys[pygame.K_LEFT]:
            if physical_strength > 0:
                x_speed -= speed
            physical_strength -= move_strength * dt
            strength_consumed = True
        if keys[pygame.K_RIGHT]:
            if physical_strength > 0:
                x_speed += speed
            physical_strength -= move_strength * dt
            strength_consumed = True
    else:
        if btns[0]:
            if physical_strength > 0:
                x_speed -= speed
            physical_strength -= move_strength * dt
            strength_consumed = True
        if btns[2]:
            if physical_strength > 0:
                x_speed += speed
            physical_strength -= move_strength * dt
            strength_consumed = True
    if not strength_consumed:
        physical_strength += 0.3 * dt
        if physical_strength > 100.0:
            physical_strength = 100.0
    if physical_strength < 0.0:
        physical_strength = 0.0
    if keys[pygame.K_KP_PLUS]:
        scale *= 2**dt
    if keys[pygame.K_KP_MINUS]:
        scale /= 2**dt
    if keys[pygame.K_HOME]:
        scale = 0.25
    if allow_timewarp:
        if keys[pygame.K_COMMA]:
            timewarp /= 2**dt
        if keys[pygame.K_PERIOD]:
            timewarp *= 2**dt
        if keys[pygame.K_SLASH]:
            timewarp = 1.0
    move_x(x_speed * dt)
    move_y(y_speed * dt)
    timer()


def move_simple():
    global x, y, scale
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 50
    if keys[pygame.K_RIGHT]:
        x += 50
    if keys[pygame.K_UP]:
        y += 50
    if keys[pygame.K_DOWN]:
        y -= 50
    if keys[pygame.K_KP_PLUS]:
        scale *= 1.01
    if keys[pygame.K_KP_MINUS]:
        scale /= 1.01


def move_x(dx):
    global x
    if dx == 0:
        return
    ddx = dx // abs(dx)
    for _ in range(int(abs(dx))):
        x += ddx
        if touching_skyscraper():
            x -= ddx
            return
    x += dx - int(dx)
    if touching_skyscraper():
        x -= dx - int(dx)


def move_y(dy):
    global y, y_speed, running
    if dy == 0:
        return
    ddy = dy // abs(dy)
    for _ in range(int(abs(dy))):
        y += ddy
        if y <= 50:
            if (x_speed**2 + y_speed**2) ** 0.5 >= 1800:
                running = False
                return
        if touching_skyscraper():
            y -= ddy
            if (x_speed**2 + y_speed**2) ** 0.5 >= 1800:
                running = False
            y_speed = 0
            return
    y += dy - int(dy)
    if touching_skyscraper():
        y -= dy - int(dy)
        if (x_speed**2 + y_speed**2) ** 0.5 >= 1800:
            running = False
        y_speed = 0


def timer():
    global time, started
    if not started and y > 0 and time == 0.0:
        started = True
    if started and int(y) == 50800 and abs(x) < 20:
        started = False
        pygame.image.save(screen, root / "honnald_selfie.png")
    if not started:
        return
    time += dt


def timestamp(t):
    hours = int(t // 3600)
    minutes = int((t % 3600) // 60)
    seconds = int(t % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def now_pos():
    if y <= 0:
        return "Ground"
    if y >= 50800:
        return "Top"
    if y <= 11250:
        return "Base"
    if y <= 40050:
        knot_level = (y - 11250) // 3600 + 1
        return f"Knot {int(knot_level)}"
    if y <= 45450:
        return "Spire"
    if y <= 47700:
        return "Damper"
    return "Lightning Rod"


def draw():
    screen.fill(background_color)

    size = screen.get_size()
    for poly in skyscraper_polygon:
        draw_object(poly)
    namefont = pygame.font.Font(str(root / "Ubuntu.ttf"), max(int(96 * scale + 0.5), 5))
    name = namefont.render("Alex Honnold", True, (0, 0, 0))
    pygame.draw.circle(screen, player_color, (size[0] // 2, size[1] // 2 - int(player_radius * scale)), int(player_radius * scale))
    screen.blit(name, (size[0] // 2 - name.get_width() // 2, size[1] // 2 - int(player_radius * scale) * 2 - 120 * scale - name.get_height()))
    current_frame = screen.copy()

    screen.fill(background_color)
    shake = lambda: interference.shake(y, 50800, t=time) * scale * 3.14
    screen.blit(current_frame, (shake(), shake()))

    time_text = font.render(timestamp(time), True, (0, 0, 0))
    move_method = ["Mouse Buttons", "Arrow Keys"]
    helper_text = font.render(f"{move_method[key_move]}: Move, Space: Jump, Arrow Down: Hold", True, (0, 0, 0))
    strength_text = font.render(f"{int(physical_strength)}%", True, (0, 0, 0))
    screen.blit(time_text, (10, 10))
    screen.blit(helper_text, (size[0] // 2 - helper_text.get_width() // 2, size[1] - 10 - helper_text.get_height()))
    screen.blit(strength_text, (size[0] - 10 - strength_text.get_width(), 10))
    floor = max(min(int(y // 450) + 1, 101), 1)
    pygame.display.set_caption(f"Skyscraper LIVE - {floor}F - {int(y / 508)}% Completed - On {now_pos()} - Time {timestamp(time)}")
    save_frame()


ffmpeg_process = start_ffmpeg(str(video_path))
while running:
    dt = clock.tick(48) / 1000.0 * timewarp
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.mod & pygame.KMOD_CTRL:
                if event.key == pygame.K_s:
                    spectator_mode = not spectator_mode
                if event.key == pygame.K_m:
                    key_move = not key_move
                if event.key == pygame.K_t:
                    allow_timewarp = not allow_timewarp
    if spectator_mode:
        move_simple()
    else:
        move()
    draw()
    pygame.display.flip()


pygame.quit()
sys.exit()
