import curses
from curses import wrapper

LEVELS= [

    [
        "#####################",
        "#@#     #         # #",
        "# ### # ####### # # #",
        "#     #   #     #   #",
        "######### # ####### #",
        "#     # # # #   #   #",
        "### # # # # ### # ###",
        "#   #   # #   # # # #",
        "# ####### ### # # # #",
        "#             #    E#",
        "#####################",

    ],
    [
       "###############################",
        "#@  #           #             #",
        "### # # ####### # ##### #######",
        "# # # #     # # # #   #       #",
        "# # ####### # # # # # ####### #",
        "# #     #   # # #   #   # #   #",
        "# ##### # ### # ####### # # ###",
        "#   #   # #     # #       #   #",
        "# ### ### # ##### # ######### #",
        "# #   #   # #     #   #       #",
        "# # ### ### ##### ### # ##### #",
        "# #     # #     #     #   #   #",
        "# ####### ##### ######### # ###",
        "#                         #  E#",
        "###############################",
    ],

    [
        "#########################################",
        "#@      #         #     #       #       #",
        "####### # ####### # ### # ##### # ##### #",
        "#   # # #   #   #   #     #   # #     # #",
        "# # # # # # # # # ########### # ####### #",
        "# #   # # #   # # #     #     # #   #   #",
        "# ### # ##### # ### ### # ##### # # # # #",
        "# #   # #   # #     #   #       # # # # #",
        "# ##### # # ######### ### ####### # # # #",
        "#       # # #       #   #     #   #   # #",
        "# ####### # # ##### ### ##### # # ##### #",
        "# #     # # # #   #     # #   # #   # # #",
        "# # # # # # # # ######### # ####### # # #",
        "# # # # # # # #       #     #   #   #   #",
        "# ### # # # # ##### ### ##### # # ##### #",
        "# #   #   # #     #     #     # #     # #",
        "# # ####### ##### # ####### ### ##### # #",
        "#   #             #         #         #E#",
        "#########################################",
    ],
    [
        "#################################################",
        "#@#     #                   #     #           # #",
        "# # ### ##### ############# ### # ### ####### # #",
        "# # #   #   # #     #           #   #   #   #   #",
        "# # # ### # # ### # # ############# ### ### ### #",
        "#   # #   # #   # #     #   #     #   #   #   # #",
        "##### # ### ### # ####### # # ### ### # # ### # #",
        "#   # #   #     # #     # #   #   #   # #   #   #",
        "### # ### ####### # ### # ##### ##### ##### # ###",
        "#   #   #   #     # #   # #     #   # #     #   #",
        "# ##### # # ####### # ### # ##### # # # ####### #",
        "#   #   # # #   #   #     # #     # #   #       #",
        "### # ##### # # # ####### # # ##### ########### #",
        "#   # #     # #     #   # #       # #         # #",
        "# ### # # ### ####### # ### ##### # # ####### # #",
        "#   # # #         #   #   # #   # # #     #   # #",
        "### # ### ####### # ##### # # # ### ##### # ### #",
        "#   #   # #   #   # #   # # # # #   #     # # # #",
        "# # ### # # # ##### # ### # # # # ### ##### # # #",
        "# # #   # # #       #     # # # #       #   #   #",
        "# ### ##### ######### ####### # ######### ### ###",
        "#           #                 #           #    E#",
        "#################################################",
    ],
    [
       
        "#######################################################",
        "#@  #   #             #     #     #       #         # #",
        "### # # ######### # # # # # ### # # # ### # ####### # #",
        "# #   #         # # # # # #   # #   # #     #       # #",
        "# ############# # # # ### ### ####### ##### ####### # #",
        "#     #       # # # #   #   # #       #   # #     # # #",
        "# ##### # ##### # # ### ### # # ### ### # ### ### # # #",
        "# #     #       # #   #     #   #   #   #     #   # # #",
        "# # ############# ### ############# # ######### ### # #",
        "# #     # #         #   #   #     # #     # #   # #   #",
        "# ##### # # ####### ### # # # ### ####### # # ### ### #",
        "#       #   #     #   #   # #   #     #     # # #     #",
        "# ####### ### ### ####### # ### ##### # ##### # # #####",
        "#     # # # # # #   #   # #   #     #     #   # # #   #",
        "##### # # # # # ### # # ##### # ########### ### # # # #",
        "#     #     # #       # #   #   #           #     # # #",
        "# ########### # ####### # # ##### ########### ##### # #",
        "#   #     #   #   #   # # #   #   #     #   #     # # #",
        "### # ### # ####### # # # ### # ##### ### # ##### # # #",
        "# # # #   #     #   # #   #   #     # #   #       # # #",
        "# # # # ##### # # ### ##### ####### # # ########### # #",
        "# # # #     # #   #   # #   #     # #   #           # #",
        "# # # ##### ####### ### # ##### # # # ######### ##### #",
        "#     #             #           #   #           #    E#",
        "#######################################################",
    ],
]
VIEW =[ None, None ,None, 6,4 ]

def put(stdscr , y, x, text, attr=0):
   """Draw text , skip it if it would fall outside the window."""
   try:
      stdscr.addstr(y,x,text,attr)
   except curses.error:
      pass

def load_level(n):
    """"Turn level n's text into a grid find the start."""
    grid =[list(row) for row in LEVELS[n]]
    start = (1, 1)
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
           if ch == "■":
            start =(x ,y)
            grid[y][x] = " "
    return grid, start

def reveal(seen, grid, px, py, view):
   """Remember every square the player can currently see."""
   for y in range(len(grid)):
      for x in range(len(grid[0])):
         if view is None or (x-px)**2 +(y-py)**2 <= view**2:
            seen.add((x,y))

def play_level(stdscr , n):
   """Play one level., or None if the player quit."""
   grid, (px, py) = load_level(n)
   maze_h , maze_w= len(grid) ,len(grid[0]) 
   view =VIEW[n]
   seen = set()
   reveal (seen, grid, px, py,view)
   steps=0

   while True:
      stdscr.erase()
      rows , cols=stdscr.getmaxyx()

      need_cols, need_rows= maze_w*2+1 , maze_h+4 
      if rows <need_rows or cols<need_cols:
         put(stdscr,0,0,"window small!")
         put(stdscr, 1, 0,f"need {need_cols} columns x {need_rows} rows.")
         put(stdscr,2,0, "maxmize the window , then press a key. (q=quit)")
         key=stdscr.getch()
         if key==ord("q"):
            return None
         if key==curses.KEY_RESIZE:
            curses.resize_term(0,0)

      top=(rows- maze_h)//2
      left =(cols-maze_w*2)//2

      title= f"Level {n+1} of {len(LEVELS)} steps:{steps}"
      if view is not None:
         title += " ( FOG: you can only see nearby)"
      put (stdscr , top -2 , left , title)
      for y , row in enumerate(grid):
         for x, ch in enumerate(row):
            if(x,y) not in seen:
               continue 
            if ch=="#":
               put(stdscr, top+y, left+x*2, "  ",curses.color_pair(1))
            elif ch=="E":
               put(stdscr, top+y, left+x*2,"E", curses.color_pair (3) | curses.A_BOLD )


      put(stdscr, top+py, left+px*2 , "■" , curses.color_pair(2) | curses.A_BOLD)
      put(stdscr,top+maze_h +1, left, "Arrows/WASD move r restart q quit")






     
      key = stdscr.getch()
      dx = dy = 0
      if key==ord("q"):
         return None
      elif key== curses.KEY_RESIZE:
         curses.resize_term(0,0)
         continue
      elif key==ord("r"):
         grid,(px, py) = load_level(n)
         seen=set()
         reveal(seen,grid,px,py,view)
         steps =0
         continue
      elif key in (curses.KEY_UP, ord("w")):
         dy=-1
      elif key in (curses.KEY_DOWN, ord("s")):
         dy =1 
      elif key in (curses.KEY_LEFT, ord("a")):
         dx= -1
      elif key in (curses.KEY_RIGHT, ord ("d")):
         dx=1
      else:
         continue

      nx, ny = px+dx, py+dy
      if grid[ny][nx]!="#":
         px, py =nx, ny
         steps +=1
         reveal(seen,grid,px,py,view)
         if grid[py][px]=="E":
def show_message(stdscr, lines):
   stdscr.erase()
   rows,cols=stdscr.getmaxyx()
   top =max(0,rows//2-len(lines)//2)
   for i , line in enumerate(lines):
      put(stdscr,top+i, max(0, (cols-len(line))//2) , line)
   stdscr.getch() 



def main(stdscr):
   curses.curs_set(0)
   curses.start_color()
   curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
   curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
   curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)


   total=0
   for n in range(len(LEVELS)):
      result = play_level(stdscr , n)
      if result is None:
         return
      total+= result
      if n < len(LEVELS) -1 :
         lines=[f"Level {n+1} complete in {result} steps!"]
         if VIEW[n+1] is not None:
                 lines.append("WARNING :the next level has FOG. You can only see nearby")
         lines.append("Press any key for the next level")
         show_message(stdscr, lines)
        

   show_message(stdscr, [
      f" YAYAY YOU ESCAPED ALL {len(LEVELS)} MAZES!",
      f"Total steps:{total}",
      "Press any key to finish",
    ])

      
curses.wrapper(main)
