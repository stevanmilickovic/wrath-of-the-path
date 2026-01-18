from __future__ import annotations

# App
APP_TITLE = "Wrath of the Path"
FPS = 60

# Grid
GRID_W = 50
GRID_H = 50
CELL_SIZE = 14
CELL_GAP = 1

# UI layout
PANEL_W = 260
MARGIN = 12

WINDOW_W = MARGIN * 2 + (GRID_W * (CELL_SIZE + CELL_GAP) - CELL_GAP) + PANEL_W
WINDOW_H = MARGIN * 2 + (GRID_H * (CELL_SIZE + CELL_GAP) - CELL_GAP)

# Gameplay (start/goal)
START_POS = (1, 1)
GOAL_POS = (GRID_W - 2, GRID_H - 2)

# Animation / Visualization (milliseconds)
SEARCH_STEP_DELAY_MS = 8
PLAYER_STEP_DELAY_MS = 35

# Maze generation
MAZE_SEED = None
