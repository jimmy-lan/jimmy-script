from models.position import Interval


def arrows_under_string(text: str, interval: Interval, arrow_line_padding: int = 0) -> str:
    pos_start = interval.start
    pos_end = interval.end

    # Following code taken from git repository:
    # https://github.com/davidcallanan/py-myopl-code/blob/master/ep4/strings_with_arrows.py
    # Modified slightly to fit the definition of my modules
    result = ''

    # Calculate indices
    idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0:
        idx_end = len(text)

    # Generate each line
    line_count = pos_end.row - pos_start.row + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n'
        result += ' ' * (col_start + arrow_line_padding) + '^' * (col_end - col_start)

        # Re-calculate indices
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0:
            idx_end = len(text)

    return result.replace('\t', '')
