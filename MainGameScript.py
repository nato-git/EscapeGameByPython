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

  def can_move(self, after_pos):  # 移動できるのか確認する関数
    if (0 <= after_pos.x < 40) and (0 <= after_pos.y < 40):
      return True
    return False

  def move(self, event):  # 移動関数
    Moving = [pg.Vector2(0, 1), pg.Vector2(-1, 0),
              pg.Vector2(0, -1), pg.Vector2(1, 0)]
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_s:
        self.dir = 0
      elif event.key == pg.K_a:
        self.dir = 1
      elif event.key == pg.K_w:
        self.dir = 2
      elif event.key == pg.K_d:
        self.dir = 3
      if self.can_move(self.pos + Moving[self.dir]):
        self.pos += Moving[self.dir]

def main():
  pg.init()
  dot_size = 32
  map_size = pg.Vector2(20, 15)
  screen = pg.display.set_mode(
      (int(dot_size * map_size.x), int(dot_size * map_size.y)))
  clock = pg.time.Clock()
  exit_game = False
  MainCharacter = Character(5, 5)

# ↓ゲームスクリプト
  while not exit_game:
    screen.fill((0, 0, 0))
    for event in pg.event.get():
      if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
        exit_game = True
      MainCharacter.move(event)
    MainCharacter.draw(screen)
# ↑ゲームスクリプト
    pg.display.update()
    clock.tick(20)
  pg.quit()
  print('ゲームを終了しました。')
if __name__ == '__main__':
  main()
