from utils import *
from grid import Grid
from ui import UI
import pygame

if __name__ == "__main__":

    pygame.init()
    # setting up how big will be the display window
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    # set a caption for the window
    pygame.display.set_caption("Path Visualizing Algorithm")

    ROWS = 50  # number of rows
    COLS = 50  # number of columns
    grid = Grid(WIN, ROWS, COLS, GRID_WIDTH, HEIGHT)
    ui = UI(WIN, GRID_WIDTH, WIDTH, HEIGHT)

    start = None
    end = None

    # flags for running the main loop
    run = True
    started = False

    while run:

        WIN.fill(COLORS['BACKGROUND'])
        ui.draw_panel()

        for row in grid.grid:
            for spot in row:
                spot.draw(WIN)
        grid.draw_grid_lines()

        pygame.display.update()

        #grid.draw()  # draw the grid and its spots
        for event in pygame.event.get():
            # verify what events happened
            if event.type == pygame.QUIT:
                run = False
                continue

            ui_action = ui.handle_events(event)

            if ui_action["type"] == "reset":
                start = None
                end = None
                grid.reset()
                started = False
                continue

            if ui_action["type"] == "algorithm_selected":
                algorithm = ui_action["algorithm"]
                algo_param = ui_action["param"]

                if not start or not end:
                    continue

                for row in grid.grid:
                    for spot in row:
                        spot.update_neighbors(grid.grid)

                started = True
                if algo_param is not None:
                    algorithm(lambda: grid.draw(), grid, start, end, algo_param)
                else:
                    algorithm(lambda: grid.draw(), grid, start, end)
                started = False
                continue


            if started:
                # do not allow any other interaction if the algorithm has started
                continue  # ignore other events if algorithm started

            if pygame.mouse.get_pressed()[0]:  # LEFT CLICK
                pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(pos)

                if row >= ROWS or row < 0 or col >= COLS or col < 0:
                    continue  # ignore clicks outside the grid

                spot = grid.grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT CLICK
                pos = pygame.mouse.get_pos()
                if ui.is_click_on_grid(pos):
                    row, col = grid.get_clicked_pos(pos)
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        spot = grid.grid[row][col]
                        spot.reset()
                        if spot == start:
                            start = None
                        elif spot == end:
                            end = None




            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid.reset()
                    started = False

                '''if event.key == pygame.K_SPACE and not started:
                    # run the algorithm
                    for row in grid.grid:
                        for spot in row:
                            spot.update_neighbors(grid.grid)
                    # here you can call the algorithms
                    #bfs(lambda: grid.draw(), grid, start, end)
                    #dfs(lambda: grid.draw(), grid, start, end)
                    #astar(lambda: grid.draw(), grid, start, end)
                    #dls(lambda: grid.draw(), grid, start, end, 1000)
                    #ucs(lambda: grid.draw(), grid, start, end)
                    #dijkstra(lambda: grid.draw(), grid, start, end)
                    #iddfs(lambda: grid.draw(), grid, start, end, 1000)
                    #ida(lambda: grid.draw(), grid, start, end)
                    started = False

                if event.key == pygame.K_c:
                    print("Clearing the grid...")
                    start = None
                    end = None
                    grid.reset()'''
    pygame.quit()
