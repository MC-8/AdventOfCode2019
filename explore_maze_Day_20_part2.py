from copy import deepcopy
""" Maze exploration for day 20 """

char_maze =  ["                     ",
              "          A          ",
              "          A          ",
              "   #######.######### ",
              "   #######.........# ",
              "   #######.#######.# ",
              "   #######.#######.# ",
              "   #######.#######.# ",
              "   #####  B    ###.# ",
              " BC...##  C    ###.# ",
              "   ##.##       ###.# ",
              "   ##...DE  F  ###.# ",
              "   #####    G  ###.# ",
              "   #########.#####.# ",
              " DE..#######...###.# ",
              "   #.#########.###.# ",
              " FG..#########.....# ",
              "   ###########.##### ",
              "              Z      ",
              "              Z      ",
              "                     "] # padded maze with spaces
# char_maze = ["                                     ",
#              "                    A                ",
#              "                    A                ",
#              "   #################.#############   ",
#              "   #.#...#...................#.#.#   ",
#              "   #.#.#.###.###.###.#########.#.#   ",
#              "   #.#.#.......#...#.....#.#.#...#   ",
#              "   #.#########.###.#####.#.#.###.#   ",
#              "   #.............#.#.....#.......#   ",
#              "   ###.###########.###.#####.#.#.#   ",
#              "   #.....#        A   C    #.#.#.#   ",
#              "   #######        S   P    #####.#   ",
#              "   #.#...#                 #......VT ",
#              "   #.#.#.#                 #.#####   ",
#              "   #...#.#               YN....#.#   ",
#              "   #.###.#                 #####.#   ",
#              " DI....#.#                 #.....#   ",
#              "   #####.#                 #.###.#   ",
#              " ZZ......#               QG....#..AS ",
#              "   ###.###                 #######   ",
#              " JO..#.#.#                 #.....#   ",
#              "   #.#.#.#                 ###.#.#   ",
#              "   #...#..DI             BU....#..LF ",
#              "   #####.#                 #.#####   ",
#              " YN......#               VT..#....QG ",
#              "   #.###.#                 #.###.#   ",
#              "   #.#...#                 #.....#   ",
#              "   ###.###    J L     J    #.#.###   ",
#              "   #.....#    O F     P    #.#...#   ",
#              "   #.###.#####.#.#####.#####.###.#   ",
#              "   #...#.#.#...#.....#.....#.#...#   ",
#              "   #.#####.###.###.#.#.#########.#   ",
#              "   #...#.#.....#...#.#.#.#.....#.#   ",
#              "   #.###.#####.###.###.#.#.#######   ",
#              "   #.#.........#...#.............#   ",
#              "   #########.###.###.#############   ",
#              "            B   J   C                ",
#              "            U   P   P                ",
#              "                                     "]

char_maze = ["                                                                                                                                   ",
"                                          M     V       Z   Z         L T     J E     W                                            ",
"                                          L     M       J   Z         C R     Y E     F                                            ",
"   #######################################.#####.#######.###.#########.#.#####.#.#####.#########################################   ",
"   #...#.#.#.#.#.#.#...#.....#...#.....#.....#.#.....#...#...#.....#...#...#.....#.#.................#...#.#...#...#.#.....#.#.#   ",
"   ###.#.#.#.#.#.#.###.#####.#.#.###.#####.###.#.#.#####.#.#.###.#.###.###.#.#####.###.###.#######.#.#.###.###.#.###.###.#.#.#.#   ",
"   #.#.#.....#...#.#.#.#...#...#.#.........#.....#.#.#...#.#...#.#.......#.#...#.#.#.#.#.....#.#.#.#.........#.#.....#...#.#...#   ",
"   #.#.#####.###.#.#.#.#.#####.#.#.#.#.###.###.#.###.###.#.###.#.#.###.###.#.###.#.#.###.#####.#.#############.#.###.###.###.#.#   ",
"   #.......#.......#.....#...#.#...#.#...#...#.#.....#.....#...#.#.#...#...#.#.....#.#.#...........#.#.#...#.....#.#.#.......#.#   ",
"   #######.###.###.#####.#.#####.#####.###.#####.###.#######.#.#.#.#######.#.#.###.#.#.###.###.#####.#.###.#.#.###.#####.#####.#   ",
"   #...#.....#...#.#.......#...#.#.....#.#.#...#.#.....#.....#.#.#.#.......#.....#.#...#.#.#.#.........#.....#...#.#.#.......#.#   ",
"   ###.###.#######.###.###.###.#.#######.#.#.###.#######.#######.#######.#####.###.###.#.#.#.#.#.#.#####.###.#####.#.###.#.#####   ",
"   #...................#.......#.#...#.#.#...#.#.......#.....#.#.#.#.#.....#...#.#.#.#.......#.#.#.#.#.....#.#.......#...#...#.#   ",
"   ###.#.#####.#.###.#.#####.#######.#.#.#.###.#.#######.#.#.#.#.#.#.###.#.###.#.#.#.#.###.#######.#.###.#####.###########.###.#   ",
"   #.#.#...#...#.#...#.#...#.#...#...........#...#.#...#.#.#.#.......#.#.#...#.#...#.....#.....#...........#...#...#.........#.#   ",
"   #.###.#########.###.###.#.###.###.#.#.#######.#.###.#.#####.###.###.#.#########.#.#########.#######.#######.#.#######.#.###.#   ",
"   #.#...#.......#.#...#.............#.#.....#.......#.#.....#.#...#...#.....#.....#.#.#.....#...#.#...#.........#.#...#.#.....#   ",
"   #.#####.#.###.#######.#.#.#######.#####.###.###.#.#.#.###.###.###.###.#.#######.#.#.###.#######.###.###.#.#.#.#.###.###.#####   ",
"   #.....#.#.#.#...#.....#.#...#...#.#.......#.#...#.#...#.#.#.........#.#.......#.#...............#.#.#...#.#.#.#...#.......#.#   ",
"   ###.#.#.###.#.#.#######.#####.###.###.#.#######.###.#.#.#######.#####.#.#.#####.#.#.#.#.###.#.###.#.###.###.###.###.#.###.#.#   ",
"   #...#.#.#.#.#.#.#...#...#.#.#.#...#.#.#.#.....#...#.#.......#...#.#...#.#.#.#.#.#.#.#.#...#.#.#...#...#.#.#...#.#.#.#.#.#.#.#   ",
"   #.#######.#.###.#.#####.#.#.#.###.#.#.#######.#.#####.###.###.###.#####.###.#.#.###.###########.#########.#.###.#.#.###.###.#   ",
"   #.......#.............#.#.#...#.#.#.....#.#.#.....#...#.#.#.......#.#.....#...#.#.......#...#.#...#.#...#.#.#.#.#.....#.....#   ",
"   ###.#######.###.###.#####.#.#.#.#####.#.#.#.#.#####.#.#.#######.###.###.#.#.#.#.###.#####.###.#.###.#.###.#.#.#.###.###.#.###   ",
"   #.#.....#.#.#.#...#...#.#.#.#.#.#.....#.#.........#.#...#.#.#.....#...#.#.#.#...#.#.................#...................#.#.#   ",
"   #.#.###.#.#.#.#.###.###.#.###.#.###.#.#####.#.###.#####.#.#.#.#####.###.###.#####.###.#####.#####.#######.###.#.###.#######.#   ",
"   #.....#.#.#.#.#.#...#...#.....#.#.#.#.....#.#.#.....#.#.....#.........#.#...#.#.#.....#...#.....#.#...#.....#.#...#.#...#...#   ",
"   ###.#.###.###.###.#.###.#.#.#.#.#.#####.###.#.###.###.#####.#.###.#.###.#.###.#.#.#.#####.#########.###.#.#####.###.#.###.#.#   ",
"   #.#.#.#.#.....#...#.#.#...#.#.....#.....#...#.#.#.#.........#.#...#...#.#.#.....#.#.........#.#...#.....#.#.....#.#.#.#.#.#.#   ",
"   #.#.###.###.#######.#.#.###.#####.###.#######.#.#.###.#.###.#######.###.#.#.#.###.#####.#.###.###.###.#.#####.###.###.#.#.###   ",
"   #.#...#.....#.......#...#.....#.#...#.#.....#.#.....#.#...#.#.........#.#...#...#.....#.#.#.#.#.#...#.#.#...#.....#.......#.#   ",
"   #.###.#####.#######.#######.###.#.###.#.###.#####.###.#.#####.#####.###.#####.###.#.#####.#.#.#.#.#########.#.#####.#####.#.#   ",
"   #.....#.....#.#.......#.#...#...........#.#.#.......#.#.#...#.#.......#.#.....#...#.#...#.#.#...#...#...#.#...#.#.#...#.#.#.#   ",
"   ###.#.#####.#.#####.###.#.#####.###.#######.#######.#.#.#.#.#######.###.###.#####.###.#.###.#.###.###.#.#.###.#.#.#.###.###.#   ",
"   #.#.#.........#...#...#.#.#.#.#...#...#...#.....#.#.#.#.#.#.#.#.#.....#.#...#...#...#.#.#.#.....#.#...#.#.........#.#...#.#.#   ",
"   #.###.###.###.#.###.#.#.###.#.#.#.#.#####.#.#.###.#.#.###.###.#.###.#.#.#.###.#####.#.###.###.###.#.#######.#.#####.###.#.#.#   ",
"   #...#.#.#.#...#.#...#.#...#...#.#.#.#.......#...#...#.....#.........#.#.#.......#.......#.....#.#.....#...#.#.#.....#.....#.#   ",
"   #.#####.#.###.#.###.###.#####.#############.#####.#######.###.#########.###.#.#######.#####.###.###.#.#.#.###.###.#####.###.#   ",
"   #.#...#.#.#.......#...#.#...#...#.#        V     B       G   X         Y   V L       P    #.#...#...#.#.#.....#.#...#.#...#.#   ",
"   #.###.#.#####.#####.###.#.###.###.#        M     P       Q   M         C   O C       K    #.###.###.#######.###.#.###.#.###.#   ",
"   #.#.#.............#.#.......#.#...#                                                       #.#.......#........................MW ",
"   #.#.#####.#.#######.###.#####.#.###                                                       #.###.#.#####.#.###.###.#.#.###.###   ",
"   #.#...#...#.....#.......#.........#                                                     NC......#...#...#...#...#.#.#.#.....#   ",
"   #.#.#######.#######.###.#.#######.#                                                       #####.#.###.###.#.#####.#.###.#####   ",
"   #...#.#.#...#.........#.#.....#....QS                                                     #.....#.......#.#.....#.#.#...#.#.#   ",
"   #.#.#.#.#.###########.#.#.#########                                                       #########.#.#.###.#############.#.#   ",
"   #.#.#...#.......#.....#...#.#...#.#                                                       #...#...#.#.#...#.#.#.#.#.#........BX ",
"   ###.#.###.#####.#.###.#.#.#.#.###.#                                                       ###.###.###.#.#.###.#.#.#.###.###.#   ",
" EL..........#...#...#.#.#.#.#.....#.#                                                       #.........#.#.#...#.....#...#.#...#   ",
"   #.###########.#####.#######.#####.#                                                       ###.#.###########.#####.###.###.###   ",
"   #.#...........................#....KO                                                   ZL....#.#...#.....#.#.#.#.......#...#   ",
"   ###.#.#.###.###.#.#.###.###.###.###                                                       #####.###.#.#######.#.#.#.#.#####.#   ",
"   #...#.#...#...#.#.#.#...#.....#...#                                                       #.#.#...................#.#.......#   ",
"   #.#.#.#.###.###.###.###.#########.#                                                       #.#.#############.#.#.###.#########   ",
"   #.#.#.#...#.#.#.#...#...#.......#.#                                                       #.....#.#.......#.#.#.#.#.#.#.....#   ",
"   #.#.###.#.###.#####.###.#.#.###.#.#                                                       ###.###.#.#.#.###.#####.###.#.###.#   ",
" UF..#...#.#.#.....#...#.#...#.#.....#                                                       #...#.....#.#...#...#.....#.....#..QS ",
"   #.#.#####.###.#######.#############                                                       #.#.#####.#.#.#.#####.###.#.###.#.#   ",
"   #.#.#.#.#.#...........#.........#.#                                                     DT..#.....#.#.#.#.#.#...#.....#.#.#.#   ",
"   #####.#.###########.#.#.###.#.#.#.#                                                       #.#.#.#.#.#.#.#.#.###.#######.#####   ",
" FU..#.#.....#.#...#...#.#...#.#.#...#                                                       #.#.#.#...#.#.#.......#.#...#.....#   ",
"   #.#.###.###.#.#####.#.###.#####.#.#                                                       #####.###.#.#####.#####.#.#####.###   ",
"   #...#...#.#.#...#...#...#...#...#..EL                                                     #...#.#.#.#.#.....#.......#.#.....#   ",
"   ###.#.#.#.#.#.###.#####.#.#.###.###                                                       ###.###.###.#####.###.#.#.#.#.#.###   ",
"   #.#...#...........#.#.#...#.#.#.#.#                                                     BX....#...#.#.#.#.#.#...#.#.....#.#.#   ",
"   #.###########.#####.#.#######.###.#                                                       #.#####.#.###.#.#.###.#######.###.#   ",
"   #...........#.#...#...........#...#                                                       #.............#.#.#.......#...#.#..RB ",
"   #.#.###.###.#####.###.###.###.#.#.#                                                       #.#.###.#.#####.#####.#####.###.#.#   ",
" XM..#.#.....#.#...#.#.#...#...#.#.#..TR                                                     #.#...#.#.............#...#.......#   ",
"   #.#.#.#.#.#.#.#.#.#.###.#####.#.###                                                       #############.#########.###.#####.#   ",
"   #.#.#.#.#.#...#.#.........#...#...#                                                     MW........#.#.#.....#.......#...#.#.#   ",
"   #.#####.#####.###.#.#.###.###.###.#                                                       #######.#.#.#########.#.#######.###   ",
"   #.#...#.#.........#.#.#.#.#.......#                                                       #.........#.....#.....#.....#...#.#   ",
"   ###.###.###.###.#.#####.#####.#####                                                       #.#########.#########.#####.#.#.#.#   ",
"   #...#.#.#.#...#.#.......#...#.#...#                                                       #.#.....#.....#.#...#.....#...#....ZL ",
"   #.#.#.###.#######.#########.###.###                                                       #.#.###.###.#.#.###.#####.#####.###   ",
"   #.#...#...#...#.#.#.....#.......#.#                                                       #.....#.....#.............#...#...#   ",
"   #.###.###.###.#.#.###.#####.###.#.#                                                       ###########.#.#.###########.#######   ",
" BP..#.............#.#...#...#...#...#                                                     FU..#...#...#.#.#.#.#...#.#.........#   ",
"   #####.#.#.###.#######.###.###.###.#                                                       #.###.#.#########.#.###.###.#.#.#.#   ",
"   #.#.#.#.#.#.#...................#..RT                                                     #...........................#.#.#..VO ",
"   #.#.#.#.###.#####################.#                                                       #####.#############.#####.#########   ",
"   #...#.#.#.................#.....#.#                                                     WF..#...#.......#.#.....#.#...#...#..AA ",
"   #.#.#.#####.#####.###.###.#.###.###                                                       #.#####.#.###.#.#######.#######.#.#   ",
"   #.#.#.#...#.....#...#.#...#.#...#.#                                                       #.#...#.#.#.........#.#.....#.#...#   ",
"   #.#.###.#####.###.#######.#.#.###.#                                                       #.###.#.#.###.#####.#.#.#.###.#.###   ",
"   #.#.#.....#.#...#...#.#.....#.#....JY                                                     #...#...#.#.......#...#.#.....#....DT ",
"   #.#.#.#.#####.#######.#.#.#.#.###.#                                                       #.#.#.#.#.#.###.###.#.#.#.#.#.###.#   ",
" RT..#...#.......#.#.......#.#.#.....#                                                       #.#...#.#.#.#...#...#...#.#.#.....#   ",
"   ###.###.#.###.#.#########.###.#.#.#      Z       S       M     E         R     U          ###.#.#########.###.#.#######.###.#   ",
"   #.....#.#.#...........#...#.#.#.#.#      J       C       L     E         B     F          #...#.....#.#.....#.#.....#.....#.#   ",
"   ###.#.###.###.#.#########.#.#####.#######.#######.#######.#####.#########.#####.#############.#######.#.###.###.#.###.#####.#   ",
"   #...#.#.#.#.#.#.#.....#.......#.....#.#...#...#.#...#.......#.....#.......#.#.........#.....#.....#...#.#.#...#.#...#.#.....#   ",
"   ###.###.#.#.#.#####.#.###.#.#.#.#.#.#.###.#.#.#.#.#.#######.#.#######.###.#.#####.#.#####.#####.#.###.#.#.#######.###.###.###   ",
"   #...#...#.#.........#.#.#.#.#.#.#.#...#.#...#.#...#...#...#.#.......#...#.#.#.#...#.#...#.....#.#...#.........#.#...#.#.....#   ",
"   #.#.###.###.#.###.#.###.#.###.###.#.###.#.#########.###.#.#.#####.#.###.###.#.###.###.#######.#.#####.#####.###.#.#####.###.#   ",
"   #.#.#.#.....#...#.#...#.....#.#...#.#.#.........#.#...#.#.....#...#.#.........#...#.#.#.#.#.........#.#.#.....#...#...#...#.#   ",
"   #.###.#.#####.###.#.#.#####.#.#.#.###.#.#.###.###.#.#####.#.###.#####.#####.#####.#.#.#.#.#####.#######.###.###.#####.#.#.#.#   ",
"   #...#...#...#...#.#.#.#.#...#.#.#.#.#...#.#.....#...#.....#...#.#...#...#.#...#...............#.......#...#.#.....#.....#.#.#   ",
"   #.###.#####.#.###.#.###.###.#######.#######.###.###.#.#.#######.#.#.###.#.#######.#####.###.#####.###.#.###.###.#.#####.###.#   ",
"   #.#.....#.......#.#.......#...#.....#...#...#.....#.#.#.#.#...#...#.#.#.....#...#...#.....#...#...#.#.....#.#...#...#.....#.#   ",
"   #####.#.#.#####.###.###.###.#.#####.###.#####.#####.#.###.#.#######.#.#####.#.#.#.#########.#####.#.#.#.#.###.###.#.###.#.###   ",
"   #.#...#.#...#.....#.#.#.#...#.#.................#.#.#.#.#.......#...#...#...#.#.#.......#.#...#.....#.#.#.#.#.#...#.#...#...#   ",
"   #.###.###.#.###.###.#.#####.#.###.#######.#######.#.#.#.#####.#.#.#####.#.###.#.#.#.#.#.#.#######.#####.###.#####.###.#.#.###   ",
"   #.......#.#...#.#.......#.#.#...#.#.#.#.#.#.....#...#.......#.#...#.#.#.....#.#...#.#.#...#.#.#.....#...........#...#.#.#.#.#   ",
"   ###.#.###.#.#.#####.#####.#########.#.#.#.#.#.#####.###.#####.#####.#.#####.#.###.###.#.###.#.###.#####.#.###.###.#####.###.#   ",
"   #...#.#...#.#...#...#.......................#...#.#.#...#.#.............#...#.#.#...#.#...#...#.....#.#.#...#.#...#.#.......#   ",
"   #####.#.#.#.#####.#####.#.#.#.#######.###.#.#.###.#.#.#.#.###.#.###.#####.###.#.#######.#####.#####.#.#.#.#.#####.#.#.#####.#   ",
"   #.#...#.#.#.....#.#.#...#.#.#.#.......#...#.#...#...#.#...#.#.#.#.......#...#.#.#...#.............#...#.#.#.#.....#.#.#.#...#   ",
"   #.#####.###.###.#.#.#######.###.#######.#.###.#####.#.#####.###.###.#.#####.#.#.#.###.###.###.###.#########.#####.#.###.#.#.#   ",
"   #.........#...#.#...#.#.#.....#.#.......#...#...#...#.....#...#.#...#...#...#.......#.#.....#...#.#.......#.#.#.....#...#.#.#   ",
"   #.###.###.#######.###.#.#.#########.#####.#.#.###.###.#.#####.#####.#######.#.###.#######.#####.###.###.#.###.#.###.#.###.###   ",
"   #.#.#...#.#.#...#.#.......#.....#.....#.#.#.#...#...#.#.#.#.#.#...#...#.....#...#.#.#...#.....#.......#.#.....#.#.....#.....#   ",
"   #.#.#.#.#.#.###.#.###.#.#.###.#####.###.###.#.#.###.#.#.#.#.#.###.#.#####.###.#####.#.#.#######.###.#.#.#.###.#######.#.#.#.#   ",
"   #.#...#.#.......#.#.#.#.#.#.........#...#.#.#.#...#.#.#.#.........#.....#...#.#.#.....#.#.#.#.....#.#.#.#...#.......#.#.#.#.#   ",
"   #.###.#####.#######.#########.#########.#.#####.###.#.###.###.#.###.#.###.###.#.###.#####.#.###.###############.#.#####.#.###   ",
"   #...#...#...........#.#.....#.#.............#.....#.#...#.#...#.....#.#.#...#.#.#.#.#...#...#.#.#.............#.#...#...#.#.#   ",
"   #.#.#.###.#.###.#####.#####.###############.#.#####.###.###.#.#.###.#.#.#.###.#.#.#.###.#.###.#.#.#####.#.#######.#####.#.#.#   ",
"   #.#.#...#.#.#.........#.#.#...#...#.#...........#.#.#.#...#.#.#...#.#.#.....#.......#.......#.#.......#.#.#.#.#.#.....#.#...#   ",
"   #.#####.#######.###.###.#.###.###.#.#.###.#.#.#.#.#.#.#.#####.#############.#######.#.#######.#####.#.#####.#.#.#.#.###.#.###   ",
"   #.#.#.#.#...#...#...#.......#.#.#.#...#...#.#.#.#...#.....#.#.........#.#.....#.....#.........#...#.#.........#.#.#.#.#.#...#   ",
"   #.#.#.#####.#.###.#####.#.#.#.#.#.#######.###.###.###.#####.#.#.###.###.#.#.#####.###.###.###.#.#######.#.###.#.#####.###.###   ",
"   #...#...#.#...#...#.....#.#...#.#.#.....#...#.#...#.........#.#.#...#.#.#.#.#.#.#...#...#.#.....#.....#.#.#...........#.....#   ",
"   ###.###.#.#.#####.#.#######.###.#.#.#####.#.#####.#########.#######.#.#.###.#.#.###.#.###########.#######.###.#####.###.###.#   ",
"   #.....#.........#.#.#.....................#.....#.#...........#.......#.......#.........................#...#.....#...#.#...#   ",
"   ###############################################.#.###.###########.#######.#######.###########################################   ",
"                                                  K G   N           P       S       Y                                              ",
"                                                  O Q   C           K       C       C                                              ",
"                                                                                                                                   "]

start_pos = None
goal_pos = None
visited = {} # cell : previous cell
good_path = []
portals = {} # {'portalname': [[p1 r, p1 c],[p2 r, p2 c]]} p1 <-> p2
MAX_DEPTH = 25
# Parse maze
for r in range(len(char_maze[:])):
    for c in range(len(char_maze[0])):
        if char_maze[r][c] == '.':
            good_path.append((r,c))
        # Parse portals. Read them from left to right and from top to bottom
        # Also, get door coordinate
        if char_maze[r][c].isalpha():
            l1 = char_maze[r][c]   # letter 1
            l2 = None
            gate_coord = []
           
            if char_maze[r+1][c].isalpha():
                l2 = char_maze[r+1][c] # letter 2
                if char_maze[r+2][c] == '.': gate_coord = [r+1,c] # Letter 2 is the gate
                elif char_maze[r-1][c] == '.': gate_coord = [r,c] # Letter 1 is the gate
                else:
                    assert(False,"Can't find door")

            if char_maze[r][c+1].isalpha():
                l2 = char_maze[r][c+1] # letter 2
                if char_maze[r][c+2] == '.': gate_coord = [r,c+1] # Letter 2 is the gate
                elif char_maze[r][c-1] == '.': gate_coord = [r,c] # Letter 1 is the gate
                else:
                    assert(False,"Can't find door")

            if l2: # Yep, it's a new portal
                # If it already exists, link it (unless is a starting / goal point)
                portal_name = l1+l2
                if portal_name not in ['AA','ZZ']:
                    if portal_name in portals:
                        portals[portal_name][1] = gate_coord
                    else:
                        portals[portal_name] = [gate_coord, None]
                else:
                    if portal_name == 'AA':
                        start_pos = tuple([*gate_coord,0])
                    if portal_name == 'ZZ':
                        goal_pos = tuple([*gate_coord,0])
                good_path.append(tuple(gate_coord))
# Create a dictionary of portal from -> to
gates_from_to = {}
gates_from_to[start_pos[0:2]] = list(start_pos)
gates_from_to[goal_pos[0:2]] = list(goal_pos)
for p in portals.values():
    # Inner from, outer_to
    if 30 < p[0][0] < 100 and 30 < p[0][1] < 100:
        level_direction = 1
    else:
        level_direction = -1
    gates_from_to[tuple(p[0])] = deepcopy(p[1])
    gates_from_to[tuple(p[0])].append(level_direction)
    gates_from_to[tuple(p[1])] = deepcopy(p[0])
    gates_from_to[tuple(p[1])].append(-level_direction)

good_path.append(start_pos)
good_path.append(goal_pos)

frontier = [start_pos]
visited[r,c,0] = (r,c,0) # Add dimensions!!

# Backtracking algorithm
while (frontier and goal_pos not in visited):
    f = frontier.pop(0)
    up =  (f[0]-1,f[1], f[2])
    down = (f[0]+1,f[1], f[2])
    left = (f[0],f[1]-1, f[2])
    right = (f[0],f[1]+1, f[2])
    
    # Todo add warp logic (inner outer etc)

    # Warp the next cell if enter in a portal, and update level
    if up[0:2] in gates_from_to:
        # warp
        up_coord =  gates_from_to[up[0:2]][0:2]
        up_level = up[2] + gates_from_to[up[0:2]][2]
        up = (*up_coord, up_level)
        if up_level < 0 or up_level >= MAX_DEPTH: up = (0,0,0)
    
    if down[0:2] in gates_from_to:
        # warp
        down_coord =  gates_from_to[down[0:2]][0:2]
        down_level = down[2] + gates_from_to[down[0:2]][2]
        down = (*down_coord, down_level)
        if down_level < 0 or down_level >= MAX_DEPTH: down = (0,0,0)

    if left[0:2] in gates_from_to:
        # warp
        left_coord =  gates_from_to[left[0:2]][0:2]
        left_level = left[2] + gates_from_to[left[0:2]][2]
        left = (*left_coord, left_level)
        if left_level < 0 or left_level >= MAX_DEPTH: left = (0,0,0)

    if right[0:2] in gates_from_to:
        # warp
        right_coord =  gates_from_to[right[0:2]][0:2]
        right_level = right[2] + gates_from_to[right[0:2]][2]
        right = (*right_coord, right_level)
        if right_level < 0 or right_level >= MAX_DEPTH: right = (0,0,0)


    if (up    not in visited) and (up[0:2]    in good_path): 
        visited[up]    = f
        frontier.append(up)    # Add key, and from where it came from
    if (down  not in visited) and (down[0:2]  in good_path): 
        visited[down]  = f
        frontier.append(down)  # Add key, and from where it came from
    if (left  not in visited) and (left[0:2]  in good_path): 
        visited[left]  = f
        frontier.append(left)  # Add key, and from where it came from
    if (right not in visited) and (right[0:2] in good_path): 
        visited[right] = f
        frontier.append(right) # Add key, and from where it came from

# Backtrack
pos = goal_pos
solution = 0
path_back = []
if goal_pos not in visited:
    solution = 0
else:
    while pos != start_pos:
        pos = visited[pos]
        path_back.append(pos)
        if pos[0:2] not in gates_from_to and pos[0:2] not in (start_pos, goal_pos): # Don't count gate spaces (letters)
            solution += 1
solution -=2 # Start and End position are calculated as from the gates (letters A and Z) but the entrace and exit are in the white space after the letters
print(f"{solution=}")