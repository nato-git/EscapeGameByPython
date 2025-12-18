import pygame as pg

class Character:
  def __init__(self, x, y):
    self.pos = pg.Vector2(x, y)
    self.size = pg.Vector2(1, 2)
    self.dir = 0
    charaImg = []
    for i in range(4):
      charaImg.append(pg.image.load(f'./image/character/characterSkin{i}.png'))
    self.charaImg = charaImg

  def draw(self, screen):  # 描画関数
    dot_size = 32
    screen.blit(self.charaImg[self.dir],
                (self.pos.x * dot_size, self.pos.y * dot_size))

  def can_move(self, after_pos, MapObject):  # 移動できるのか確認する関数
    for i in range(len(MapObject)):
      if ((0 <= after_pos.x < 40) and (0 <= after_pos.y < 40)) and (after_pos != MapObject[i].pos):
        answer = True
      else: return False
    return answer

  def move(self, MapObject):  # 移動関数
    Moving = [pg.Vector2(0, 0.5), pg.Vector2(-0.5, 0),
              pg.Vector2(0, -0.5), pg.Vector2(0.5, 0)]
    keys = pg.key.get_pressed()
    getkey = False
    if keys[pg.K_s]:
      self.dir = 0
      getkey = True
    elif keys[pg.K_a]:
      self.dir = 1
      getkey = True
    elif keys[pg.K_w]:
      self.dir = 2
      getkey = True
    elif keys[pg.K_d]:
      self.dir = 3
      getkey = True
    if self.can_move(self.pos + Moving[self.dir], MapObject) and getkey:
      self.pos += Moving[self.dir]

class MapObject:
  def __init__(self, x, y):
    self.pos = pg.Vector2(x, y)
    self.size = pg.Vector2(1, 1)
    self.img = {'test': pg.image.load(
        './image/object/test.png'), 'floor': pg.image.load('./image/object/floor.png')}

  def draw(self, screen, type):  # 描画関数
    dot_size = 32
    screen.blit(self.img[type],
                (self.pos.x * dot_size, self.pos.y * dot_size))

def main():
  pg.init()
  dot_size = 32
  map_size = pg.Vector2(25, 20)
  screen = pg.display.set_mode(
      (int(dot_size * map_size.x), int(dot_size * map_size.y)))
  clock = pg.time.Clock()
  exit_game = False
  MainCharacter = Character(5, 5)
  MapObj = [MapObject(10, 10), MapObject(11, 10), MapObject(12, 10),
            MapObject(10, 11), MapObject(11, 11), MapObject(12, 11)]
  Floor = []
  for x in range(25):
    for y in range(13):
      Floor.append(MapObject(x, 20 - y))

# ↓ゲームスクリプト
  while not exit_game:
    screen.fill((0, 0, 0))
    for event in pg.event.get():
      if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
        exit_game = True
    MainCharacter.move(MapObj)
    for obj in Floor:
      obj.draw(screen, 'floor')
    for obj in MapObj:
      obj.draw(screen, 'test')
    MainCharacter.draw(screen)
# ↑ゲームスクリプト
    pg.display.update()
    clock.tick(20)
  pg.quit()
  print('ゲームを終了しました。')
if __name__ == '__main__':
  main()
