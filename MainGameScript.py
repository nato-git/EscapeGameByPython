import pygame as pg
import sys

print(pg.font.get_fonts())

class Character:
  def __init__(self, x, y):
    self.pos = pg.Vector2(x, y)
    self.dir = 1  # 0:下, 1:左, 2:上, 3:右
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
    dot_size = 32
    if self.is_moving:
      self.anime_count += 0.2
      walk_index = (self.dir * 2) + (int(self.anime_count) % 2)
      current_img = self.charaWalkingImg[walk_index]
    else:
      self.anime_count = 0
      current_img = self.charaImg[self.dir]
    screen.blit(current_img, (self.pos.x * dot_size,
                self.pos.y * dot_size - dot_size))

  def can_move(self, after_pos, MapObjectList):
    if not (0 <= after_pos.x < 25 and 8 <= after_pos.y < 19):
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
    cls.images['floor'] = pg.image.load(
        './image/object/floor.png').convert_alpha()
    cls.images['bed'] = pg.image.load(
        './image/object/bed.png').convert_alpha()
    cls.images['door'] = pg.image.load(
        './image/object/door.png').convert_alpha()
    cls.images['deskR'] = pg.image.load(
        './image/object/desk_right.png').convert_alpha()
    cls.images['deskL'] = pg.image.load(
        './image/object/desk_left.png').convert_alpha()
    cls.images['wall'] = pg.image.load(
        './image/object/wall.png').convert_alpha()
    cls.images['Room_door_close'] = pg.image.load(
        './image/object/room_door_close.png').convert_alpha()

  def draw(self, screen, type):
    dot_size = 32
    screen.blit(self.images[type], (self.pos.x *
                dot_size, self.pos.y * dot_size))

# 調べたときのテキスト表示
def text_talk(screen, font, texts):
  pg.draw.rect(screen, (0, 0, 0), pg.Rect(0, 500, 800, 100))
  texts = font.render(texts, True, (255, 255, 255))
  screen.blit(texts, (30, 525))
  pg.display.update()
  pg.time.delay(1000)
# アイテム確認
def text_item(screen, font, item):
  pg.draw.rect(screen, (0, 0, 0), pg.Rect(0, 500, 800, 100))
  item_text = "所持品: " + ", ".join(item) if item else "所持品は何もない。"
  texts = font.render(item_text, True, (255, 255, 255))
  screen.blit(texts, (30, 525))
  pg.display.update()

def main():
  pg.init()
  screen = pg.display.set_mode((800, 600))
  pg.display.set_caption("家に帰りたい。")
  clock = pg.time.Clock()

  # 状態管理（0: タイトル, 1: ゲーム本編）
  state = 0
  # テキスト表示用変数
  text_i = 0
  # 所持品リスト
  item = []
  # アイテム確認用変数
  item_line = False

  MapObject.load_images()
  # プレイヤー
  player = Character(23, 18)
  # 床
  floors = [MapObject(x, y) for x in range(25) for y in range(8, 20)]
  # ベッド
  bed = MapObject(24, 17)
  # 玄関
  door = MapObject(15, 6)
  # 机
  deskR = MapObject(13, 18)
  deskL = MapObject(12, 18)
  desk = [deskR, deskL]
  # 仕切り壁
  walls = []
  for y in range(3, 19):
    if y != 13:
      walls.append(MapObject(11, y))
  # 部屋区切りドア
  RoomDoor = MapObject(11, 13)
  # フォント
  font_title = pg.font.SysFont('mspgothic', 50)
  font_text = pg.font.SysFont('mspgothic', 25)
  # ぶつかるオブジェクト
  Map_Object_Block = [bed] + [door] + desk + walls + [RoomDoor]

  while True:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        sys.exit()
      if event.type == pg.KEYDOWN:
        if state == 0 and event.key == pg.K_SPACE:
          state = 1  # ゲーム開始
        elif state == 1 and event.key == pg.K_SPACE:
          text_i += 1
          if text_i >= 6:
            state = 2  # ゲーム本編へ
            text_i = 0
        # ゲーム内の調べるキー行動
        elif state == 2 and event.key == pg.K_e:
            # ドアの判定
          if player.pos == pg.Vector2(15, 8) and player.dir == 2:
            if '玄関の鍵らしきもの' not in item:
              text_talk(screen, font_text, "鍵がかかっている。")
            # else: 脱出処理追加予定地
        # アイテム確認
        elif state == 2 and event.key == pg.K_q:
          item_line = not item_line
          # ゲーム終了
        if event.key == pg.K_ESCAPE:
          pg.quit()
          sys.exit()

    if state == 0:
      # スタート画面
      screen.fill((0, 0, 0))
      text = font_title.render("家に帰りたい。",
                               True, (255, 255, 255))
      explain = font_text.render(
          "Press SPACE to start", True, (255, 255, 255))
      screen.blit(text, (80, 200))
      screen.blit(explain, (300, 400))
    # 導入テキスト
    elif state == 1:
      screen.fill((0, 0, 0))
      texts = ['「ここは...？」',
               '太陽の光を感じて目が覚める。',
               '目を開けてみると、そこは見覚えのない部屋だった。',
               '(誘拐事件か...!?)',
               'どうやら今はこの部屋に誰もいないようだ',
               '(ここに俺を連れてきた犯人が帰ってくる前に脱出しなければ...)']
      text = font_text.render(texts[text_i], True, (255, 255, 255))
      screen.blit(text, (30, 200))
    elif state == 2:
      # ゲーム本編
      player.update(Map_Object_Block)
      screen.fill((150, 150, 150))
      for f in floors:
        f.draw(screen, 'floor')
      bed.draw(screen, 'bed')
      door.draw(screen, 'door')
      for d in desk:
        if d == deskR:
          d.draw(screen, 'deskR')
        else:
          d.draw(screen, 'deskL')
      for w in walls:
        w.draw(screen, 'wall')
      RoomDoor.draw(screen, 'Room_door_close')
      player.draw(screen)
      # 所持品表示
      if item_line == True:
        text_item(screen, font_text, item)
      # 確認用座標表示
      print(player.pos)

    pg.display.update()
    clock.tick(15)

if __name__ == '__main__':
  main()
