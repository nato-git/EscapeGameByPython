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
    objs = ['floor', 'bed', 'door', 'wall',
            'freezer', 'chair', 'bookstand',
            'dustbox', 'kitchen1', 'kitchen2',
            'kitchen3', 'door_desk', 'paper',
            'mirror', 'calender', 'TV', 'moneybox',
            'closet']
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
  pg.time.delay(1000)

def item_look(screen, font, items):
  rect_h = 120
  pg.draw.rect(screen, (0, 0, 0), pg.Rect(
      0, SCREEN_H - rect_h, SCREEN_W, rect_h))
  pg.draw.rect(screen, (255, 255, 255), pg.Rect(
      0, SCREEN_H - rect_h, SCREEN_W, rect_h), 2)
  item_msg = font.render(
      f"持っているアイテム: {', '.join(items) if items else '持っているアイテムはない。'}", True, (255, 255, 255))
  screen.blit(item_msg, (30, SCREEN_H - rect_h + 30))
  pg.display.update()

def number(screen, font, texts, event):
  input_text = "".join(texts) if isinstance(texts, list) else str(texts)
  if event.type == pg.KEYDOWN:
    if event.key == pg.K_BACKSPACE:
      input_text = input_text[:-1]
    elif len(input_text) < 4 and event.unicode.isdigit():
      input_text += event.unicode
    elif event.key == pg.K_RETURN:
      return input_text
  input_done = False
  while not input_done:
    rect_h = 120
    pg.draw.rect(screen, (0, 0, 0), pg.Rect(
        0, SCREEN_H - rect_h, SCREEN_W, rect_h))
    pg.draw.rect(screen, (255, 255, 255), pg.Rect(
        0, SCREEN_H - rect_h, SCREEN_W, rect_h), 2)
    number_msg = font.render(f"{input_text}", True, (255, 255, 255))
    screen.blit(number_msg, (30, SCREEN_H - rect_h + 30))
    pg.display.update()
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        sys.exit()
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_RETURN:
          input_done = True
        elif event.key == pg.K_BACKSPACE:
          input_text = input_text[:-1]
        elif len(input_text) < 4 and event.unicode.isdigit():
          input_text += event.unicode

  return input_text


def main():
  pg.init()
  screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
  pg.display.set_caption("家に帰りたい。")
  clock = pg.time.Clock()

  state = 0
  text_i = 0
  text_j = 0
  item = []
  item_condi = False
  Door_condi = False
  closet_condi = False
  money_number = []
  small_box = []
  money_box_condi = False
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
  freezer = MapObject(0, 4)  # 冷蔵庫
  kitchen1 = MapObject(2, 5)  # キッチン
  kitchen2 = MapObject(3, 5)
  kitchen3 = MapObject(4, 5)
  TV = MapObject(8, 14)  # テレビ
  closet = MapObject(8, 6)  # クローゼット
  moneybox = MapObject(0, 14)  # 金庫

  exit_door = MapObject(13, 3)  # 玄関ドア
  bookbox = [MapObject(19, 4), MapObject(18, 4)]
  bed = MapObject(19, 13)  # 右下のベッド
  door_desk = MapObject(12, 5)  # 机上のドア
  dustbox = [MapObject(17, 5), MapObject(1, 5)]  # ゴミ箱
  paper = MapObject(12.2, 5)  # 机上の紙
  mirror = MapObject(15, 4)  # 鏡
  calender = MapObject(19, 10)  # カレンダー

  # プレイヤー初期位置
  player = Character(18, 14)

  # 衝突リスト
  Map_Object_Block = walls + \
      [RoomDoor, exit_door, chair, deskL, deskR, door_desk, TV, moneybox] + \
      dustbox + \
      [MapObject(19, 5), MapObject(18, 5)] + \
      [kitchen1, kitchen2, kitchen3] + \
      [MapObject(15, 5)] + \
      [MapObject(8, 7), MapObject(8, 6)] + \
      [MapObject(0, 5)] + \
      [MapObject(19, 14), MapObject(19, 13)]

  font_title = pg.font.SysFont('mspgothic', 50)
  font_text = pg.font.SysFont('mspgothic', 24)

  while True:
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
          if event.key == pg.K_q:
            item_condi = not item_condi
          if event.key == pg.K_e:
            # ベッド
            if player.pos == pg.Vector2(18, 14) and player.dir == 3:
              text_talk(screen, font_text, "ベッドだ。なぜかここで寝ていた。")
            elif (player.pos == pg.Vector2(18, 13) and player.dir == 3) or (player.pos == pg.Vector2(19, 12) and player.dir == 0):
              if "棒磁石" not in item:
                text_talk(screen, font_text, "棒磁石が落ちている。棒磁石を手に入れた。")
                item.append("棒磁石")
              else:
                text_talk(screen, font_text, "もう何もない。")
            # カレンダー
            elif player.pos == pg.Vector2(19, 10) and player.dir == 3:
              text_talk(screen, font_text, "カレンダーだ。知らない元号が書いてある。")
              text_talk(screen, font_text, "私の誕生日はクリスマスだったので、ひとつにまとめられていたな。")
            # 本棚
            elif player.pos == pg.Vector2(18, 6) and player.dir == 2:
              if "部屋の鍵" not in item:
                text_talk(screen, font_text, "本棚の隙間に何かある。部屋の鍵を手に入れた。")
                item.append("部屋の鍵")
              else:
                text_talk(screen, font_text, "もう何もない。")
            elif player.pos == pg.Vector2(19, 6) and player.dir == 2:
              if Door_condi == True:
                text_talk(screen, font_text, "私好みの小説がおいてある。気味が悪い。")
              else:
                text_talk(screen, font_text, "左から、赤、緑、紫、茶色の背表紙の本が入ってある。")
            # ゴミ箱1
            elif (player.pos == pg.Vector2(17, 6) and player.dir == 2) or (player.pos == pg.Vector2(16, 5) and player.dir == 3):
              text_talk(screen, font_text, "ゴミ箱だ。薬のゴミとティッシュが入っている。")
            # 鏡
            elif (player.pos == pg.Vector2(15, 6) and player.dir == 2) or (player.pos == pg.Vector2(14, 5) and player.dir == 3) or (player.pos == pg.Vector2(16, 5) and player.dir == 1):
              if money_box_condi == False:
                text_talk(screen, font_text, "鏡だ。今は見る必要がない。")
              else:
                text_talk(screen, font_text, "鏡の裏を見てみると、箱がおいてある。")
                text_talk(screen, font_text, "箱を開けると、鍵が入っていた。")
                state = 3
            # 机上の紙
            elif (player.pos == pg.Vector2(12, 6) and player.dir == 2) or (player.pos == pg.Vector2(13, 5) and player.dir == 1) or (player.pos == pg.Vector2(11, 5) and player.dir == 3):
              text_talk(screen, font_text, "メモのようだ。「〇月×日 病院に行く」と書かれている。")
            # 玄関
            elif player.pos == pg.Vector2(13, 5) and player.dir == 2:
              text_talk(screen, font_text, "鍵がかかっている。")
            # 仕切りドア
            elif player.pos == pg.Vector2(10, 8) and player.dir == 1 and Door_condi == False:
              if "部屋の鍵" in item:
                text_talk(screen, font_text, "扉が開いた。")
                Door_condi = True
                item.remove("部屋の鍵")
                if RoomDoor in Map_Object_Block:
                  Map_Object_Block.remove(RoomDoor)
              else:
                text_talk(screen, font_text, "鍵がかかっている。")
            # クローゼット
            elif (player.pos == pg.Vector2(7, 6) or player.pos == pg.Vector2(7, 7)) and player.dir == 3:
              if closet_condi == False:
                text_talk(screen, font_text, "南京錠で閉じられている。")
                if "小さな鍵" in item:
                  text_talk(screen, font_text, "小さな鍵で南京錠を開けた。")
                  closet_condi = True
                  item.remove("小さな鍵")
              else:
                if player.pos == pg.Vector2(7, 6):
                  text_talk(screen, font_text, "クローゼットだ。私好みの服が多くかかっている。気持ち悪い。")
                else:
                  text_talk(screen, font_text,
                            "クローゼットだ。赤色の服が4着、青色のジーンズが3着、革の上着が1着入っている。")
            # 流し
            elif player.pos == pg.Vector2(2, 6) and player.dir == 2:
              text_talk(screen, font_text, "流しに洗い物がたまっている。")
            # コンロ
            elif (player.pos == pg.Vector2(5, 5) and player.dir == 1) or (player.pos == pg.Vector2(4, 6) and player.dir == 2):
              text_talk(screen, font_text, "奥に何か光っているが取れない。")
              if "棒磁石" in item:
                text_talk(screen, font_text, "棒磁石を使って光っているものを引っ張った。小さな鍵を手に入れた。")
                item.append("小さな鍵")
                item.remove("棒磁石")
            # 冷蔵庫
            elif player.pos == pg.Vector2(0, 6) and player.dir == 2:
              text_talk(screen, font_text, "冷蔵庫だ、一部腐っているものもある。")
              text_talk(screen, font_text, "食べられそうなのはキャベツが2つとブロッコリーが4つだけだ")
            # ゴミ箱2
            elif player.pos == pg.Vector2(1, 6) and player.dir == 2:
              text_talk(screen, font_text, "ゴミ箱だ。薬のごみとティッシュが入っている。")
              if small_box != "1224":
                text_talk(screen, font_text, "ゴミ箱の隣に小箱がおいてある。番号で開くようだ。")
                small_box = number(screen, font_text, small_box, event)
                if small_box == "1224":
                  text_talk(screen, font_text, "鍵が開いた。")
                  text_talk(screen, font_text, "中にはアメジストのついたネックレスが入っていた。")
                else:
                  text_talk(screen, font_text, "間違っているようだ。")
              else:
                text_talk(screen, font_text, "アメジストのネックレスが入っている。")
            # 机
            elif (player.pos == pg.Vector2(2, 11) and player.dir == 3) or (player.pos == pg.Vector2(3, 12) and player.dir == 2) or (player.pos == pg.Vector2(4, 12) and player.dir == 2) or (player.pos == pg.Vector2(5, 11) and player.dir == 1) or (player.pos == pg.Vector2(4, 10) and player.dir == 0) or (player.pos == pg.Vector2(3, 10) and player.dir == 0):
              text_talk(screen, font_text, "白色の錠剤が3つおかれている。")
            # 金庫
            elif (player.pos == pg.Vector2(0, 13) and player.dir == 0) or (player.pos == pg.Vector2(1, 14) and player.dir == 1):
              if money_number != "4611":
                text_talk(screen, font_text, "金庫だ、暗証番号が必要らしい。")
                money_number = number(screen, font_text, money_number, event)
                if money_number == "4611":
                  text_talk(screen, font_text, "鍵が開いた。")
                  text_talk(screen, font_text, "「鏡の裏」と書かれた紙と財布が入っていた。")
                  money_box_condi = True
                else:
                  text_talk(screen, font_text, "間違っているようだ。")
              else:
                text_talk(screen, font_text, "鏡の裏と書かれた紙と財布が入っている。")
            elif (player.pos == pg.Vector2(7, 14) and player.dir == 3) or (player.pos == pg.Vector2(8, 13) and player.dir == 0):
              text_talk(screen, font_text, "テレビだ、ついていない。")
        elif state == 3 and event.key == pg.K_SPACE:
          text_j += 1
          if text_j >= 9:
            pg.quit()
            sys.exit()
        if event.key == pg.K_ESCAPE:
          pg.quit()
          sys.exit()

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

      # 描画
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
      door_desk.draw(screen, 'door_desk')
      paper.draw(screen, 'paper')
      for d in dustbox:
        d.draw(screen, 'dustbox')
      freezer.draw(screen, 'freezer')
      kitchen1.draw(screen, 'kitchen1')
      kitchen2.draw(screen, 'kitchen2')
      kitchen3.draw(screen, 'kitchen3')
      mirror.draw(screen, 'mirror')
      TV.draw(screen, 'TV')
      closet.draw(screen, 'closet')
      moneybox.draw(screen, 'moneybox')
      calender.draw(screen, 'calender')
      if Door_condi == False:
        RoomDoor.draw(screen, 'Room_door_close')
      else:
        RoomDoor.draw(screen, 'Room_door_open')
      player.draw(screen)

      if item_condi == True:
        item_look(screen, font_text, item)

    elif state == 3:
      screen.fill((0, 0, 0))
      texts = [
          '「こんな近くに置いてあったのか、犯人が返ってくる前に早く出よう。」',
          'そう思い、顔を上げるとそこには知らない顔の老人がいた',
          '驚いて後ろにコケるとひどく腰が痛んだ',
          '脳が理解しようとしない、こいつは誰なんだ',
          'わかっている、わかっているんだ',
          'この老人は紛れもなく俺なのだろうと',
          '絶望で目の前が暗くなるのを感じる',
          '遠くでガチャッという音が聞こえた気がした。',
          '──Thanks for Playing──'
      ]
      screen.blit(font_text.render(
          texts[text_j], True, (255, 255, 255)), (80, 300))

    pg.display.update()
    clock.tick(12)

if __name__ == '__main__':
  main()
