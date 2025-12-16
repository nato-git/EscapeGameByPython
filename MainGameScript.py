import pygame as pg

class Character:
  def __init__(self, x, y):
    self.pos = pg.Vector2(x, y)
    self.size = pg.Vector2(50, 50)
    self.dir = 0
    charaImg = []
    for i in range(4):
      charaImg.append(pg.image.load(f'img_path{i}.png'))
    self.charaImg = charaImg[0]

  def draw(self, screen):  # 描画関数
    screen.blit(self.charaImg[self.dir], (self.pos.x, self.pos.y))

  def can_move(self, after_pos):  # 移動できるのか確認する関数
    if (0 <= after_pos.x <= 300) and (0 <= after_pos.y <= 300):
      return True

  def move(self):  # 移動関数
    Moving = [pg.Vector2(0, -1), pg.Vector2(-1, 0),
              pg.Vector2(0, 1), pg.Vector2(1, 0)]
    for event in pg.event.get():
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_w:
          self.dir = 2
          if self.can_move(self.pos + Moving[self.dir]):
            self.pos += Moving[self.dir]
        if event.key == pg.K_d:
          self.dir = 3
          if self.can_move(self.pos + Moving[self.dir]):
            self.pos += Moving[self.dir]
        if event.key == pg.K_s:
          self.dir = 0
          if self.can_move(self.pos + Moving[self.dir]):
            self.pos += Moving[self.dir]
        if event.key == pg.K_a:
          self.dir = 1
          if self.can_move(self.pos + Moving[self.dir]):
            self.pos += Moving[self.dir]

def main():
  pg.init()
  dot_size = 32
  map_size = pg.Vector2(40, 40)
  screen = pg.display.set_mode(
      (int(dot_size * map_size.x), int(dot_size * map_size.y)))
  clock = pg.time.Clock()
  exit = False

  while not exit:
    for event in pg.event.get():
      if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
        exit = True
    MainCharacter = Character(5, 5)
    MainCharacter.move()
    pg.display.update()
    clock.tick(20)
  pg.quit()
  print('ゲームを終了しました。')
