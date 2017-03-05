def color_map(errand_id, piece_id):
    red = (errand_id % 10) * 5 + (piece_id % 10) * 5
    green = (errand_id % 15) * 10 + (piece_id % 5) * 30
    blue = (errand_id % 5) * 40 + (piece_id % 15) * 15

    return "rgba( " + str(red % 255) + " , " + str(green % 255) + ", " + str(blue % 255) + ", 1)"
