import curses
import random
import time

# Constants
GRID_WIDTH = 30
GRID_HEIGHT = 20
MOVE_INTERVAL = 0.2  # seconds

class Game:
    def __init__(self):
        self.worm = [{'x': 5, 'y': 10}, {'x': 4, 'y': 10}, {'x': 3, 'y': 10}]
        self.food = {'x': GRID_WIDTH // 2, 'y': GRID_HEIGHT // 2}
        self.score = 0
        self.game_over = False
        self.consecutive_collisions = 0
        self.start_time = time.time()
        self.last_move_time = time.time()

    def is_collision(self, x, y):
        # Check wall collision
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return True
        # Check self collision
        for segment in self.worm:
            if segment['x'] == x and segment['y'] == y:
                return True
        return False

    def move_worm(self):
        head = self.worm[0].copy()
        potential_directions = [
            {'x': 1, 'y': 0}, {'x': -1, 'y': 0}, 
            {'x': 0, 'y': 1}, {'x': 0, 'y': -1}
        ]

        safe_directions = []
        for d in potential_directions:
            new_x = head['x'] + d['x']
            new_y = head['y'] + d['y']
            if not self.is_collision(new_x, new_y):
                safe_directions.append(d)

        if safe_directions:
            chosen = random.choice(safe_directions)
            head['x'] += chosen['x']
            head['y'] += chosen['y']
            self.worm.insert(0, head)

            # Check if ate food
            if head['x'] == self.food['x'] and head['y'] == self.food['y']:
                self.score += 1
                # Reset food to center (as per original game logic)
                self.food = {'x': GRID_WIDTH // 2, 'y': GRID_HEIGHT // 2}
            else:
                self.worm.pop()
            
            self.consecutive_collisions = 0
        else:
            self.consecutive_collisions += 1
            if self.consecutive_collisions >= 3 and len(self.worm) > 5:
                self.game_over = True

    def move_food(self, dx, dy):
        new_x = self.food['x'] + dx
        new_y = self.food['y'] + dy
        
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            self.food['x'] = new_x
            self.food['y'] = new_y

def draw_board(stdscr, game):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    # Calculate offset to center the board
    offset_y = (h - GRID_HEIGHT - 2) // 2
    offset_x = (w - GRID_WIDTH * 2 - 2) // 2
    
    if offset_y < 0: offset_y = 0
    if offset_x < 0: offset_x = 0

    # Draw border
    # Top border
    stdscr.addstr(offset_y, offset_x, "+" + "-" * (GRID_WIDTH * 2) + "+")
    # Side borders
    for y in range(GRID_HEIGHT):
        stdscr.addstr(offset_y + y + 1, offset_x, "|")
        stdscr.addstr(offset_y + y + 1, offset_x + (GRID_WIDTH * 2) + 1, "|")
    # Bottom border
    stdscr.addstr(offset_y + GRID_HEIGHT + 1, offset_x, "+" + "-" * (GRID_WIDTH * 2) + "+")

    # Draw stats
    stats = f"Score: {game.score} | Length: {len(game.worm)} | Time: {int(time.time() - game.start_time)}s"
    stdscr.addstr(offset_y - 1, offset_x, stats[:w-1])
    stdscr.addstr(offset_y + GRID_HEIGHT + 2, offset_x, "Controls: Arrow Keys to move FOOD (*)")

    # Draw Food
    # x * 2 because terminal characters are usually twice as tall as wide
    food_screen_y = offset_y + 1 + game.food['y']
    food_screen_x = offset_x + 1 + (game.food['x'] * 2)
    try:
        stdscr.addstr(food_screen_y, food_screen_x, "()", curses.color_pair(2) | curses.A_BOLD)
    except curses.error:
        pass

    # Draw Worm
    for i, segment in enumerate(game.worm):
        screen_y = offset_y + 1 + segment['y']
        screen_x = offset_x + 1 + (segment['x'] * 2)
        
        char = "[]"
        color = curses.color_pair(1)
        if i == 0: # Head
            color = color | curses.A_BOLD
        
        try:
            stdscr.addstr(screen_y, screen_x, char, color)
        except curses.error:
            pass

    stdscr.refresh()

def main(stdscr):
    # Setup colors
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)  # Worm
    curses.init_pair(2, curses.COLOR_RED, -1)    # Food
    
    curses.curs_set(0) # Hide cursor
    stdscr.nodelay(True) # Non-blocking input
    stdscr.timeout(50) # Refresh every 50ms

    game = Game()

    while not game.game_over:
        # Input handling
        try:
            key = stdscr.getch()
        except:
            key = -1

        if key != -1:
            if key == curses.KEY_UP:
                game.move_food(0, -1)
            elif key == curses.KEY_DOWN:
                game.move_food(0, 1)
            elif key == curses.KEY_LEFT:
                game.move_food(-1, 0)
            elif key == curses.KEY_RIGHT:
                game.move_food(1, 0)
            elif key == 27: # ESC
                break

        # Game Logic
        current_time = time.time()
        if current_time - game.last_move_time > MOVE_INTERVAL:
            game.move_worm()
            game.last_move_time = current_time

        # Render
        draw_board(stdscr, game)

    # Game Over Screen
    stdscr.nodelay(False)
    h, w = stdscr.getmaxyx()
    msg = f"GAME OVER! Final Score: {game.score}"
    stdscr.addstr(h//2, (w - len(msg))//2, msg, curses.A_BOLD | curses.A_BLINK)
    stdscr.addstr(h//2 + 1, (w - 20)//2, "Press any key to exit")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
