import pygame as pg
import sys

class Character:
  def __init__(self, x, y):
    self.pos = pg.Vector2(x, y)
    self.dir = 0  # 0:下, 1:左, 2:上, 3:右
    self.is_moving = False
    self.anime_count = 0.0  # アニメーションのコマ送り用
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
    screen.blit(current_img, (self.pos.x * dot_size, self.pos.y * dot_size))

  def can_move(self, after_pos, MapObjectList):
    # 画面範囲内かチェック
    if not (0 <= after_pos.x < 25 and 0 <= after_pos.y < 20):
      return False
    # 障害物との衝突チェック
    for obj in MapObjectList:
      if after_pos == obj.pos:
        return False
    return True

  def update(self, MapObjectList):
    # 方向と移動量の対応表
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
  def __init__(self, x, y):
    self.pos = pg.Vector2(x, y)
    self.img = {
        'test': pg.image.load('./image/object/test.png').convert_alpha(),
        'floor': pg.image.load('./image/object/floor.png').convert_alpha()
    }

  def draw(self, screen, type):
    dot_size = 32
    screen.blit(self.img[type], (self.pos.x *
                dot_size, self.pos.y * dot_size))

def main():
  pg.init()
  dot_size = 32
  map_size = pg.Vector2(25, 20)
  screen = pg.display.set_mode(
      (int(dot_size * map_size.x), int(dot_size * map_size.y)))
  pg.display.set_caption("Walking Animation Example")
  clock = pg.time.Clock()

  # オブジェクト生成
  MainCharacter = Character(5, 5)
  MapObj = [
      MapObject(10, 10), MapObject(11, 10), MapObject(12, 10),
      MapObject(10, 11), MapObject(11, 11), MapObject(12, 11)
  ]
  Floor = []
  for x in range(25):
    for y in range(20):
      Floor.append(MapObject(x, y))

  running = True
  while running:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        running = False
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
          running = False
    MainCharacter.update(MapObj)
    screen.fill((255, 255, 255))
    for f in Floor:
      f.draw(screen, 'floor')
    for obj in MapObj:
      obj.draw(screen, 'test')
    MainCharacter.draw(screen)
    pg.display.update()
    clock.tick(13)

  pg.quit()
  sys.exit()

if __name__ == '__main__':
  main()
