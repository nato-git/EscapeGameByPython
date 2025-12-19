import pygame as pg
import sys

print(pg.font.get_fonts())

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
    if not (0 <= after_pos.x < 25 and 0 <= after_pos.y < 20):
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
    cls.images['test'] = pg.image.load(
        './image/object/test.png').convert_alpha()
    cls.images['floor'] = pg.image.load(
        './image/object/floor.png').convert_alpha()

  def draw(self, screen, type):
    dot_size = 32
    screen.blit(self.images[type], (self.pos.x *
                dot_size, self.pos.y * dot_size))

def main():
  pg.init()
  screen = pg.display.set_mode((800, 600))
  pg.display.set_caption("家に帰りたい。")
  clock = pg.time.Clock()

  # 状態管理（0: タイトル, 1: ゲーム本編）
  state = 0

  MapObject.load_images()
  player = Character(22, 18)
  map_objs = [MapObject(10, 10), MapObject(11, 10), MapObject(12, 10)]
  floors = [MapObject(x, y) for x in range(25) for y in range(8, 20)]
  font = pg.font.SysFont('mspgothic', 60)
  while True:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        sys.exit()
      if event.type == pg.KEYDOWN:
        if state == 0 and event.key == pg.K_SPACE:
          state = 1  # ゲーム開始
        if event.key == pg.K_ESCAPE:
          pg.quit()
          sys.exit()
    if state == 0:
      # スタート画面
      screen.fill((0, 0, 0))
      text = font.render("家に帰りたい。", True, (255, 255, 255))
      screen.blit(text, (100, 250))
    elif state == 1:
      # ゲーム本編
      player.update(map_objs)
      screen.fill((255, 255, 255))
      for f in floors:
        f.draw(screen, 'floor')
      for obj in map_objs:
        obj.draw(screen, 'test')
      player.draw(screen)

    pg.display.update()
    clock.tick(13)

if __name__ == '__main__':
  main()
