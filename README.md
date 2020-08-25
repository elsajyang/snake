# snake
we all like to start with the snake game

## Big Picture
- A window screen with buttons, instructions, the snake game + other display stuff
- Read user keystrokes
- Snake game: a snake that grows in length as it consumes food which pop up at random times and random places. Objective is to survive by not crashing into itself or outside walls.


## UI
- Display screen on browser vs software window
  - Browser, html5: cross-platform, quick and easy to deploy (abstracts away from hardware differences). Can be as secure as native apps
  - Native: built ro run on a specific OS platform (iOS, Android, Windows). built for performance meaning they optimize hardware usage
- Start game window
    - Play
- Game window: redraw just enough times for smooth rendering
    - Score
        - 10 points per apple
        - length?
    - Snake head: blue square
    - Apple/food: red circle
    - "Press arrow key in any direction to start": poll for an arrow key

## Game State + Transitions
- Poll for arrow keystrokes
- Move one step in direction, render
- Upon reading a valid arrow keystroke:
    Change snake direction
    Move one step in direction
    Render
- Upon head reaching food:
    Make food disappear, head supplants food position
    Increase length <- just add tile where head/old food pos is at to simulate this
    Update Score
    Generate a new food (not on areas covered by snake)
    Render
- Upon head reaching wall or itself:
    Freeze for a few sec
    End game
    Render "End game"


### Board
- Position, coordinates
- time
- space: really just needs snake and food.
    - matrix: can't really keep track of "order" of snake traversal
    - linked list waozers. add/remove to head and tail

### Snake
- direction
- linked list repres. length, order

### Food
- position = generate random on tile != snake

