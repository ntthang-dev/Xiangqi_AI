
# Kiểm tra điều kiện qua sông cho Tốt và Tượng 

def is_across_river(position, color):
    """Check if the position is across the river for the given color."""
    row, col = position
    
    if color == 'black':
        return row >= 5  # Red pieces cross river when row >= 5
    else:  # red
        return row <= 4  # Black pieces cross river when row <= 4
