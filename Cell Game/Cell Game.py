import pygame as pg
import numpy as np
import pygame.time

# Константы основного алгоритма
cell_size = 7

# Экран
size = w, h = 1600, 800
flags = pg.FULLSCREEN | pg.DOUBLEBUF
screen = pg.display.set_mode(size, flags)
pg.display.set_caption('Cell Machine')

# Цвета
black = pg.Color(0, 0, 0)
white = pg.Color(255, 255, 255)
dead = pg.Color(224, 255, 255)
alive = pg.Color(0, 139, 139)

# Шрифт
font = 'monospace'
font_size = 50


class GameOfLife:
    def __init__(self):
        self.surface = screen
        self.width = w
        self.height = h
        self.scale = cell_size
        self.alive = alive
        self.dead = dead
        self.columns = int(h / cell_size)
        self.rows = int(w / cell_size)
        self.status = np.random.randint(0, 2, size=(self.rows, self.columns), dtype=bool)

    def run(self):
        # Обновляем и рендерим поле
        self.take_grid()
        self.update_grid()

    def take_grid(self):
        # Рисуем клетку
        for row in range(self.rows):
            for col in range(self.columns):
                if self.status[row, col]:  # Если статус 1 - рисуем живую
                    pygame.draw.rect(self.surface, self.alive,
                                     [row * self.scale, col * self.scale, self.scale,
                                      self.scale])
                else:  # Если статус 0 - рисуем мертвую
                    pygame.draw.rect(self.surface, self.dead,
                                     [row * self.scale, col * self.scale, self.scale,
                                      self.scale])

    def random_generate_cells(self):
        # Радномное заполнение поля
        self.clear()
        for row in range(self.rows):
            for col in range(self.columns):
                self.status = np.random.randint(0, 2, size=(self.rows, self.columns), dtype=bool)
                if self.status[row, col]:  # Если статус 1 - рисуем живую
                    pygame.draw.rect(self.surface, self.alive,
                                     [row * self.scale, col * self.scale, self.scale,
                                      self.scale])
                else:  # Если статус 0 - рисуем мертвую
                    pygame.draw.rect(self.surface, self.dead,
                                     [row * self.scale, col * self.scale, self.scale,
                                      self.scale])

    def click_change(self, x, y):
        row = int(x / cell_size)
        col = int(y / cell_size)
        self.status[row, col] = not self.status[row, col]
        if self.status[row, col]:  # Если статус 1 - рисуем живую
            pygame.draw.rect(self.surface, self.alive,
                             [row * self.scale, col * self.scale, self.scale,
                              self.scale])
        else:  # Если статус 0 - рисуем мертвую
            pygame.draw.rect(self.surface, self.dead,
                             [row * self.scale, col * self.scale, self.scale,
                              self.scale])
        pg.display.update()

    def clear(self):
        for row in range(self.rows):
            for col in range(self.columns):
                self.status[row][col] = 0
                pygame.draw.rect(self.surface, self.dead,
                                 [row * self.scale, col * self.scale, self.scale,
                                  self.scale])

    def update_cell(self, x, y):
        # Получаем следующее поколение клеток(поля)
        current_state = self.status[x, y]
        alive_neighbors = 0

        # Get to how many alive neighbors
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if i == 0 and j == 0:
                        continue
                    elif self.status[x + i, y + j]:
                        alive_neighbors += 1
                except:
                    continue

        # Updating the cell's state
        if current_state and alive_neighbors < 2:  # dies as if by underpopulation
            return False
        elif current_state and (alive_neighbors == 2 or alive_neighbors == 3):  # lives to the next generation
            return True
        elif current_state and alive_neighbors > 3:  # dies as if by overpopulation
            return False
        elif ~current_state and alive_neighbors == 3:  # becomes alive as if by reproduction
            return True
        else:
            return current_state

    def update_grid(self):
        # обновляем поле
        updated_grid = self.status.copy()
        for row in range(updated_grid.shape[0]):  # shape() выводит колличество клеток  в строках/столбцах
            for col in range(updated_grid.shape[1]):
                updated_grid[row, col] = self.update_cell(row, col)

        self.status = updated_grid


class Buttons:  # Класс кнопки
    def __init__(self, x, y, background_color, width, height):
        self.x = x
        self.y = y
        self.color = background_color
        self.width = width
        self.height = height
        self.rect = (x, y, width, height)

    def create_panel(self):  # Создание заднего фона для кнопки
        panel = pygame.Surface((self.width, self.height))
        panel.fill(black)
        panel.set_alpha(128)
        return panel

    def set_title(self, title):  # Получаем надпись которая будет на кнопке
        my_font = pygame.font.SysFont(font, font_size)
        text_surface = my_font.render(title, True, white)
        return text_surface

    def render_panel(self, panel):  # Добавляем на экран полученную кнопку
        panel.fill(black)
        panel.set_alpha(128)
        pygame.draw.rect(screen, black, self.rect, 1)
        screen.blit(panel, (self.x, self.y))

    def render(self, title, panel):
        self.render_panel(panel)
        screen.blit(title, (self.x, self.y))

    def animate(self):
        pygame.draw.rect(screen, white, self.rect, 2)
        pygame.display.update()

    def pause_change(self, pause):
        pause = not pause
        return pause



# Главная функция
def main() -> None:
    pg.init()
    pygame.font.init()
    clock = pg.time.Clock()
    # Создание отображения состояние pause play
    button = Buttons(0, 0, black, 150, 60)
    play_pause_button = button.create_panel()
    pause_title = button.set_title('Pause')
    play_title = button.set_title('Play')

    button2 = Buttons(150, 0, black, 150, 60)
    reset_button = button2.create_panel()
    reset_title = button.set_title('Reset')

    button3 = Buttons(0, 660, black, 150, 60)
    quit_button = button3.create_panel()
    quit_title = button3.set_title('Quit')

    game = GameOfLife()
    game.random_generate_cells()
    pause = True
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # Закрытие игрового окна на esc
                    running = False
                if event.key == pg.K_SPACE:  # Пауза/отжатие паузы на пробел
                    pause = not pause
                if event.key == pg.K_d:  # На D очистка поля
                    game.clear()
                if event.key == pg.K_r:
                    game.random_generate_cells()
            if event.type == pg.MOUSEBUTTONDOWN:
                mx, my = pg.mouse.get_pos()
                game.click_change(mx, my)
                if 150 < mx <= 300 and 0 < my <= 60:
                    game.random_generate_cells()
                    button2.animate()
                if 0 < mx <= 150 and 0 < my <= 60:
                    pause = button.pause_change(pause)
                    button.animate()
                if 0 < mx <= 150 and 660 < my <= 720:
                    button3.animate()
                    running = False

        if pause:
            game.take_grid()
            button.render(pause_title, play_pause_button)
            button2.render(reset_title, reset_button)
            button3.render(quit_title, quit_button)
            pg.display.update()
        else:
            game.run()
            button.render(play_title, play_pause_button)
            button2.render(reset_title, reset_button)
            button3.render(quit_title, quit_button)
            pg.display.update()
        clock.tick(10)
    pg.quit()


if __name__ == '__main__':
    main()
