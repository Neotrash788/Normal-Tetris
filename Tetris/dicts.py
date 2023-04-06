col_dict = {
   0 : (100, 100, 100),
   1 : (150, 150, 0 ),
   2 : (150, 80, 0),
   3 : (0, 0, 150),
   4 : (0, 150, 0),    
   5 : (150, 0, 0),
   6 : (0, 150, 150),
   7 : (150, 0, 150),
   8 : (50, 50, 50)
}

# Consts for pygame keys
key_time_dict = {
   1073741903 : 0,
   1073741904 : 0,
   1073741905 : 0
}

senceitivity_dict = {
   "ARR" : 1.2,
   "DAS" : 4.5,
   "DCD" : 1,
   "SDF" : -1
}

shape_dict = {
   "o" : ["u", "r", "d"],
   "l" : ["l", "r", "r", "u"],
   "j" : ["r", "l", "l", "u"],
   "s" : ["l", "r", "u", "r"],
   "z" : ["r", "l", "u", "l"],
   "i" : ["l", "r", "r", "r"],
   "t" : ["l", "r", "u", "d", "r"]
}

shape_id_dict = {
   "o" : 1,
   "l" : 2,
   "j" : 3,
   "s" : 4,
   "z" : 5,
   "i" : 6,
   "t" : 7
}

t_spin_offset_dict = {   
   "u" : [(-1, -1), (1, -1)],
   "d" : [(-1, 1), (1, 1)],
   "l" : [(-1, -1), (-1, 1)],
   "r" : [(1, -1), (1, 1)]
}

offset_dict = {
   "u" : (0, -1),
   "d" : (0, 1),
   "l" : (-1, 0),
   "r" : (1, 0)
}

rotate_cw_dict = {
   "u" :  "r",
   "d" :  "l",
   "l" :  "u",
   "r" :  "d"
}

rotate_ccw_dict = {
   "u" : "l",
   "d" : "r",
   "l" : "d",
   "r" : "u"
}

clear_type_dict = {
   1 : "SINGLE",
   2 : "DOUBBLE",
   3 : "TRIPPLE",
   4 : "TETRIS"
}

spin_type_dict = {
   0 : "None",
   1 : "Mini",
   2 : "Full"
}

kick_cw_dict = {
   "u" : [(0,0), (-1,0), (-1,-1), ( 0,2), (-1,2)],
   "d" : [(0,0), (1,0), (1,-1), ( 0,2), (1,2)],
   "l" : [(0,0), (-1,0), (-1,1), ( 0,-2), (-1,-2)],
   "r" : [(0,0), (1,0), (1,1), ( 0,-2), (1,-2)]
}

kick_ccw_dict = {
   "u" : [(0,0), (1,0), (1,-1), (0,2), (1,2)],
   "d" : [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],
   "l" : [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
   "r" : [(0,0), (1,0), (1,1), (0,-2), (1,-2)]
}

kick_i_cw_dict = {
   "u" : [(0,0), (-2,0), (1,0), (-2,1), (1,-2)],
   "r" : [(0,0), (-1,0), (2,0), (-1,-2), (2,1)],
   "d" : [(0,0), (2,0), (-1,0), (2,-1), (-1,2)],
   "l" : [(0,0), (1,0), (-2,0), (1,2), (-2,-1)]
}

kick_i_ccw_dict = {
   "u" : [(0,0), (-1,0), (2,0), (-1,-2), (2,1)],
   "l" : [(0,0), (-2,0), (1,0), (-2,1), (1,-2)],
   "d" : [(0,0), (1,0), (-2,0), (1,2), (-2,-1)],
   "r" : [(0,0), (2,0), (-1,0), (2,-1), (-1,2)]
}