def save_bookmark(user, idNum, bookmark):
    if idNum == 1:
        user.bookmark1_id = bookmark
    if idNum == 2:
        user.bookmark2_id = bookmark
    if idNum == 3:
        user.bookmark3_id = bookmark
    if idNum == 4:
        user.bookmark4_id = bookmark
    if idNum == 5:
        user.bookmark5_id = bookmark

def delete_bookmark(user, idNum):
    if idNum == 1:
        user.bookmark1_id = None
    if idNum == 2:
        user.bookmark2_id = None
    if idNum == 3:
        user.bookmark3_id = None
    if idNum == 4:
        user.bookmark4_id = None
    if idNum == 5:
        user.bookmark5_id = None