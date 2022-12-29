def get_shape_coords(shape: str, y_tunnel_max: int, lm_coord: int):
    """Auxilary function to get the coordinates of a new shape.

    To use the function efficiently, I call it not to get the original starting
    cooordinates of the new shape (with its left edge 2 units away from the left wall
    ans its bottom edge three units above the highest rock) but instead to get the
    position after the shape has already fallen down until it's lowest position is
    1 level above the level where there must be at least 1 position filled with a rock.
    """
    if shape == "-":
        coords = {
            (lm_coord, y_tunnel_max + 1),
            (lm_coord + 1, y_tunnel_max + 1),
            (lm_coord + 2, y_tunnel_max + 1),
            (lm_coord + 3, y_tunnel_max + 1),
        }
    elif shape == "+":
        coords = {
            (lm_coord + 1, y_tunnel_max + 1),
            (lm_coord, y_tunnel_max + 2),
            (lm_coord + 1, y_tunnel_max + 2),
            (lm_coord + 2, y_tunnel_max + 2),
            (lm_coord + 1, y_tunnel_max + 3),
        }
    elif shape == "L":
        coords = {
            (lm_coord, y_tunnel_max + 1),
            (lm_coord + 1, y_tunnel_max + 1),
            (lm_coord + 2, y_tunnel_max + 1),
            (lm_coord + 2, y_tunnel_max + 2),
            (lm_coord + 2, y_tunnel_max + 3),
        }
    elif shape == "I":
        coords = {
            (lm_coord, y_tunnel_max + 1),
            (lm_coord, y_tunnel_max + 2),
            (lm_coord, y_tunnel_max + 3),
            (lm_coord, y_tunnel_max + 4),
        }
    elif shape == "box":
        coords = {
            (lm_coord, y_tunnel_max + 1),
            (lm_coord + 1, y_tunnel_max + 1),
            (lm_coord, y_tunnel_max + 2),
            (lm_coord + 1, y_tunnel_max + 2),
        }
    return coords
