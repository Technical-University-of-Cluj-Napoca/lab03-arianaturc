# ui.py - User Interface Manager
import pygame
from utils import *
from searching_algorithms import *


class Button:


    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: tuple, hover_color: tuple):

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.active_color = COLORS['BUTTON_ACTIVE']
        self.is_hovered = False
        self.is_active = False

    def draw(self, win: pygame.Surface, font: pygame.font.Font) -> None:

        color = self.active_color if self.is_active else (self.hover_color if self.is_hovered else self.color)
        pygame.draw.rect(win, color, self.rect, border_radius=5)
        pygame.draw.rect(win, COLORS['GREY'], self.rect, 2, border_radius=5)

        text_surface = font.render(self.text, True, COLORS['TEXT'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class UI:


    def __init__(self, win: pygame.Surface, grid_width: int, window_width: int, window_height: int):

        self.win = win
        self.grid_width = grid_width
        self.window_width = window_width
        self.window_height = window_height
        self.panel_width = window_width - grid_width


        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)


        self.button_width = 160
        self.button_height = 40
        self.button_x = grid_width + 20
        self.button_spacing = 10
        self.start_y = 20


        self.algorithms = [
            ("BFS", bfs, None),
            ("DFS", dfs, None),
            ("A*", astar, None),
            ("DLS", dls, 1000),
            ("UCS", ucs, None),
            ("Dijkstra", dijkstra, None),
            ("IDDFS", iddfs, 1000),
            ("IDA*", ida, None)
        ]


        self.algo_buttons = []
        for i, (name, func, param) in enumerate(self.algorithms):
            button = Button(
                self.button_x,
                self.start_y + i * (self.button_height + self.button_spacing),
                self.button_width,
                self.button_height,
                name,
                COLORS['BUTTON_BG'],
                COLORS['BUTTON_HOVER']
            )
            self.algo_buttons.append((button, func, name, param))


        self.reset_button = Button(
            self.button_x,
            self.start_y + len(self.algorithms) * (self.button_height + self.button_spacing) + 20,
            self.button_width,
            self.button_height,
            "Clear Grid",
            COLORS['PINK'],
            (200, 60, 80)
        )


        self.selected_algorithm = None
        self.selected_algo_name = "None"
        self.selected_algo_param = None

    def draw_panel(self) -> None:

        panel_rect = pygame.Rect(self.grid_width, 0, self.panel_width, self.window_height)
        pygame.draw.rect(self.win, COLORS['PANEL_BG'], panel_rect)

        for button, func, name, param in self.algo_buttons:
            button.draw(self.win, self.small_font)


        self.reset_button.draw(self.win, self.font)


        selection_y = self.reset_button.rect.bottom + 30
        sel_text = self.small_font.render(f"Selected: {self.selected_algo_name}", True, COLORS['WHITE'])
        self.win.blit(sel_text, (self.button_x, selection_y))



    def handle_events(self, event: pygame.event.Event) -> dict:

        for button, func, name, param in self.algo_buttons:
            if button.handle_event(event):
                self.selected_algorithm = func
                self.selected_algo_name = name
                self.selected_algo_param = param

                for btn, _, _, _ in self.algo_buttons:
                    btn.is_active = False
                button.is_active = True
                return {
                    'type': 'algorithm_selected',
                    'algorithm': func,
                    'name': name,
                    'param': param
                }


        if self.reset_button.handle_event(event):
            return {'type': 'reset'}


        for button, _, _, _ in self.algo_buttons:
            button.handle_event(event)
        self.reset_button.handle_event(event)

        return {'type': None}

    def get_selected_algorithm(self) -> tuple:
        return self.selected_algorithm, self.selected_algo_name, self.selected_algo_param

    def is_click_on_grid(self, pos: tuple[int, int]) -> bool:
        return pos[0] < self.grid_width