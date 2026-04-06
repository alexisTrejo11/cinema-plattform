from enum import Enum

class TheaterType(str, Enum):
    TWO_D = '2D'
    THREE_D = '3D'
    IMAX = 'IMAX'
    FOUR_DX = '4DX'
    VIP = 'VIP'

class MovieGenre(str, Enum):
    ACTION = 'ACTION'
    COMEDY = 'COMEDY'
    DRAMA = 'DRAMA'
    ROMANCE = 'ROMANCE'
    THRILLER = 'THRILLER'
    SCI_FI = 'SCI_FI'

class MovieRating(str, Enum):
    G = 'G'
    PG = 'PG'
    PG_13 = 'PG_13'
    R = 'R'
    NC_17 = 'NC_17'
