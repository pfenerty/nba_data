def year_num_to_str(year_num: int) -> str:
    next_year = year_num + 1
    next_year_offset = str(next_year)[-2:]
    return f'{year_num}-{next_year_offset}'

def format_game_id(game_id: [int, str]) -> str:
    gid_str = str(game_id)
    while len(gid_str) < 10:
        gid_str = f'0{gid_str}'
    return gid_str