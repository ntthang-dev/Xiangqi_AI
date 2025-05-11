
# Xử lý logic di chuyển Tướng/Sĩ trong Cửu Cung

def is_in_palace(position, color):
    """Check if the position is within the palace of the given color."""
    row, col = position
    
    # Palace boundaries
    if color == 'black':
        return 0 <= row <= 2 and 3 <= col <= 5
    else:  # black
        return 7 <= row <= 9 and 3 <= col <= 5
