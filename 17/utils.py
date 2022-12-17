def get_shape_coords(shape: str, y_tunnel_max: int, lm_coord: int):

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
