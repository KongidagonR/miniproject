def checkmate(board):
    """
    รับ board เป็น string หนึ่งก้อน (หลายบรรทัดคั่นด้วย \\n)
    แล้ว print "Success" ถ้า King โดน "check" (มีตัวหมากอื่นกินได้)
    หรือ print "Fail" ถ้าไม่โดน
    ถ้า input ผิดปกติ (undefined behavior) จะไม่ print อะไรเลย แล้ว return กลับไปเฉยๆ
    """

    # 1) board ต้องเป็น string เท่านั้น
    if not isinstance(board, str):
        return

    # 2) แตกเป็นแต่ละแถว (แต่ละบรรทัด)
    rows = board.split("\n")

    # ตัดบรรทัดว่างท้ายๆ ออก (เผื่อมี \n เกินมาตอนจบ string)
    while len(rows) > 0 and rows[-1] == "":
        rows.pop()

    # กระดานต้องไม่ว่างเปล่า
    if len(rows) == 0:
        return

    size = len(rows)

    # 3) กระดานต้องเป็นสี่เหลี่ยมจัตุรัส -> ทุกแถวต้องยาวเท่ากับจำนวนแถว
    for row in rows:
        if len(row) != size:
            return

    # 4) หา King ต้องมีตัวเดียวเท่านั้น
    king_row = None
    king_col = None
    king_count = 0

    for r in range(size):
        for c in range(size):
            if rows[r][c] == 'K':
                king_count += 1
                king_row = r
                king_col = c

    if king_count != 1:
        return

    # 5) ไล่ดูทุกช่อง ถ้าเป็นตัวหมากฝ่ายตรงข้าม เช็คว่ากิน King ได้ไหม
    in_check = False

    for r in range(size):
        for c in range(size):
            piece = rows[r][c]

            # ตัวอักษรที่ไม่ใช่ P B R Q ถือว่าเป็นช่องว่างทั้งหมด (K ก็ข้ามไปเพราะเป็นตัวเดียวกับ King เอง)
            if piece not in "PBRQ":
                continue

            if can_attack_king(rows, size, r, c, piece, king_row, king_col):
                in_check = True

    if in_check:
        print("Success")
    else:
        print("Fail")


def can_attack_king(rows, size, r, c, piece, king_row, king_col):
    """
    เช็คว่าตัวหมากที่อยู่ (r, c) กิน King ที่ (king_row, king_col) ได้หรือไม่
    """

    # --- Pawn: กินได้แค่ทแยงมุม "ขึ้นไปหนึ่งช่อง" ซ้ายหรือขวา ---
    if piece == 'P':
        target_row = r - 1
        left_col = c - 1
        right_col = c + 1
        if target_row == king_row and (left_col == king_col or right_col == king_col):
            return True
        return False

    # --- Rook / Bishop / Queen: เดินเป็นเส้นตรงไปเรื่อยๆ จนกว่าจะเจอตัวหมากตัวแรก ---
    directions = []

    if piece == 'R':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    elif piece == 'B':
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    elif piece == 'Q':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dr, dc in directions:
        nr = r + dr
        nc = c + dc

        while 0 <= nr < size and 0 <= nc < size:
            if nr == king_row and nc == king_col:
                return True

            # ถ้าเจอตัวหมากอื่นขวางก่อนถึง King แปลว่าทางนี้ตันแล้ว ไปทิศต่อไป
            if rows[nr][nc] in "PBRQ":
                break

            nr += dr
            nc += dc

    return False