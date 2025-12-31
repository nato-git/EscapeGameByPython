import pygame as pg
import sys

# --- 設定定数 ---
DOT_SIZE = 48
MAP_WIDTH = 20
MAP_HEIGHT = 15
SCREEN_W = DOT_SIZE * MAP_WIDTH   # 960
SCREEN_H = DOT_SIZE * MAP_HEIGHT  # 720

class Character:
  def __init__(self, x, y):
    self.pos = pg.Vector2(x, y)
    self.dir = 0  # 0:下, 1:左, 2:上, 3:右
    self.is_moving = False
    self.anime_count = 0.0
    self.charaImg = []
    for i in range(4):
      self.charaImg.append(pg.image.load(
          f'./image/character/characterSkin{i}.png').convert_alpha())
    self.charaWalkingImg = []
    for j in range(8):
      self.charaWalkingImg.append(pg.image.load(
          f'./image/character/characterWalking{j}.png').convert_alpha())

  def draw(self, screen):
    if self.is_moving:
      self.anime_count += 0.2
      walk_index = (self.dir * 2) + (int(self.anime_count) % 2)
      current_img = self.charaWalkingImg[walk_index]
    else:
      self.anime_count = 0
      current_img = self.charaImg[self.dir]

    draw_x = self.pos.x * DOT_SIZE
    draw_y = self.pos.y * DOT_SIZE - (current_img.get_height() - DOT_SIZE)
    screen.blit(current_img, (draw_x, draw_y))

  def can_move(self, after_pos, MapObjectList):
    if not (0 <= after_pos.x < MAP_WIDTH and 5 <= after_pos.y < MAP_HEIGHT):
      return False
    for obj in MapObjectList:
      if after_pos == obj.pos:
        return False
    return True

  def update(self, MapObjectList):
    MoveVec = [pg.Vector2(0, 1), pg.Vector2(-1, 0),
               pg.Vector2(0, -1), pg.Vector2(1, 0)]
    keys = pg.key.get_pressed()
    self.is_moving = False
    target_dir = -1
    if keys[pg.K_s]: target_dir = 0
    elif keys[pg.K_a]: target_dir = 1
    elif keys[pg.K_w]: target_dir = 2
    elif keys[pg.K_d]: target_dir = 3

    if target_dir != -1:
      self.dir = target_dir
      next_pos = self.pos + MoveVec[self.dir]
      if self.can_move(next_pos, MapObjectList):
        self.pos = next_pos
        self.is_moving = True

class MapObject:
  images = {}

  def __init__(self, x, y):
    self.pos = pg.Vector2(x, y)

  @classmethod
  def load_images(cls):
    objs = ['floor', 'bed', 'door', 'wall', 'freezer', 'chair', 'bookstand']
    for o in objs:
      cls.images[o] = pg.image.load(
          f'./image/object/{o}.png').convert_alpha()
    cls.images['deskR'] = pg.image.load(
        './image/object/desk_right.png').convert_alpha()
    cls.images['deskL'] = pg.image.load(
        './image/object/desk_left.png').convert_alpha()
    cls.images['Room_door_close'] = pg.image.load(
        './image/object/room_door_close.png').convert_alpha()
    cls.images['Room_door_open'] = pg.image.load(
        './image/object/room_door_open.png').convert_alpha()

  def draw(self, screen, type):
    screen.blit(self.images[type], (self.pos.x *
                DOT_SIZE, self.pos.y * DOT_SIZE))

def text_talk(screen, font, texts):
  rect_h = 120
  pg.draw.rect(screen, (0, 0, 0), pg.Rect(
      0, SCREEN_H - rect_h, SCREEN_W, rect_h))
  pg.draw.rect(screen, (255, 255, 255), pg.Rect(
      0, SCREEN_H - rect_h, SCREEN_W, rect_h), 2)
  msg = font.render(texts, True, (255, 255, 255))
  screen.blit(msg, (30, SCREEN_H - rect_h + 40))
  pg.display.update()
  pg.time.delay(800)

def main():
  pg.init()
  screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
  pg.display.set_caption("家に帰りたい。")
  clock = pg.time.Clock()

  state = 0
  text_i = 0
  item = []
  Door_condi = True
  MapObject.load_images()

  # マップオブジェクト配置
  # 床
  floors = []
  for x in range(20):
    for y in range(5, 15):
      floors.append(MapObject(x, y))
  walls = []
  for y in range(1, 15):
    if y != 8:
      walls.append(MapObject(9, y))
  # 中央ドア
  RoomDoor = MapObject(9, 8)

  deskL = MapObject(3, 11)
  deskR = MapObject(4, 11)  # 中央の机
  chair = MapObject(3.5, 10)  # 椅子

  exit_door = MapObject(13, 3)  # 玄関ドア
  bookbox = [MapObject(19, 4), MapObject(18, 4)]
  bed = MapObject(19, 13)  # 右下のベッド

  # プレイヤー初期位置
  player = Character(14, 8)

  # 衝突リスト
  Map_Object_Block = walls + [RoomDoor, exit_door, bed, chair,
                              deskL, deskR]

  font_title = pg.font.SysFont('mspgothic', 50)
  font_text = pg.font.SysFont('mspgothic', 24)

  while True:
    print(player.pos)
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        sys.exit()
      if event.type == pg.KEYDOWN:
        if state == 0 and event.key == pg.K_SPACE:
          state = 1
        elif state == 1 and event.key == pg.K_SPACE:
          text_i += 1
          if text_i >= 6:
            state = 2
            text_i = 0
        elif state == 2:
          if event.key == pg.K_e:
            # 玄関
            if player.pos == pg.Vector2(13, 1) and player.dir == 2:
              text_talk(screen, font_text, "鍵がかかっている。")
            # 仕切りドア
            if player.pos == pg.Vector2(10, 8) and player.dir == 1 and Door_condi:
              text_talk(screen, font_text, "扉が開いた。")
              Door_condi = False
              if RoomDoor in Map_Object_Block: Map_Object_Block.remove(
                  RoomDoor)
        if event.key == pg.K_ESCAPE: pg.quit(); sys.exit()

    if state == 0:
      screen.fill((0, 0, 0))
      screen.blit(font_title.render("家に帰りたい。", True,
                  (255, 255, 255)), (SCREEN_W // 2 - 150, 250))
      screen.blit(font_text.render("Press SPACE to start", True,
                  (255, 255, 255)), (SCREEN_W // 2 - 120, 400))
    elif state == 1:
      screen.fill((0, 0, 0))
      texts = ['「ここは...？」', '太陽の光を感じて目が覚める。', '見覚えのない部屋だ。',
               '(誘拐か...？)', '誰もいないようだ。', '(犯人が来る前に逃げよう。)']
      screen.blit(font_text.render(
          texts[text_i], True, (255, 255, 255)), (80, 300))
    elif state == 2:
      player.update(Map_Object_Block)
      screen.fill((100, 100, 100))
      for f in floors:
        f.draw(screen, 'floor')
      for w in walls:
        w.draw(screen, 'wall')
      deskL.draw(screen, 'deskL')
      deskR.draw(screen, 'deskR')
      chair.draw(screen, 'chair')
      exit_door.draw(screen, 'door')
      bed.draw(screen, 'bed')
      for b in bookbox:
        b.draw(screen, 'bookstand')

      if Door_condi:
        RoomDoor.draw(screen, 'Room_door_close')
      else:
        RoomDoor.draw(screen, 'Room_door_open')
      player.draw(screen)

    pg.display.update()
    clock.tick(12)

if __name__ == '__main__':
  main()
