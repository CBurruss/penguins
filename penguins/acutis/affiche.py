# Define the affiche() method and function
import polars as pl
import re
import math

"""
affiche extension for Polars DataFrames.

This module monkey-patches the affiche() method onto pl.DataFrame.
The patch is applied automatically when this module is imported.

Usage:
    df.affiche()
"""
# Define the affiche() method
def affiche(self, align="left", na_color="\033[91;3m", theme="newspaper"):
    """
    Display a Polars DataFrame with formatted table borders and styling.
    
    Args:
        self: the DataFrame instance
        align: text alignment ("left", "center", "right")
        na_color: ANSI color code for missing values
        theme: border theme ("newspaper")
    
    Usage:
        df.affiche()
    """
    
    df = self

    # Handle empty DataFrame
    if df.shape[1] == 0 or df.shape[0] == 0:
        msg = "That table doesn't exist!"
        width = len(msg)
        top = f"╔{'═' * (width + 2)}╗"
        mid = f"║ {msg} ║"
        bot = f"╚{'═' * (width + 2)}╝"
        print(f"{top}\n{mid}\n{bot}")
        return None

    # Border theme
    if theme == "newspaper":
        border = {
            "h": "═", "v": "║",
            "tl": "╔", "tr": "╗",
            "bl": "╚", "br": "╝",
            "jn": "╬",
            "l": "╠", "r": "╣",
            "t": "╦", "b": "╩"
        }
    else:
        raise ValueError("Theme not supported. Try 'newspaper'")

    reset = "\033[0m"

    # Handle color for unique NA types
    def color_na(x):
        if x is None:
            return f"{na_color}null{reset}"
        return str(x)

    # Width calculator (ignores ANSI codes)
    def display_width(s):
        clean = re.sub(r'\033\[[0-9;]*[mK]', '', str(s))
        return len(clean)

    # Prepare display data
    col_names = df.columns
    # Pull column types
    col_types = [str(dtype) for dtype in df.dtypes]
    
    # Abbreviate common type names
    type_abbrev = {
        "string": "str",
        "categorical": "cat",
        "boolean": "bool",
        "object": "obj",
        "decimal": "dec"
    }

    col_types = [type_abbrev.get(dtype.lower(), dtype) for dtype in col_types]
    
    # Column widths
    col_widths = []
    for i, col in enumerate(col_names):
        header_width = display_width(col)
        type_width = display_width(col_types[i])
        # Get column values and apply color_na
        col_values = [color_na(val) for val in df[col].to_list()]
        data_widths = [display_width(val) for val in col_values]
        col_widths.append(max([header_width, type_width] + data_widths))

    # Draw horizontal line
    def draw_hline(connector_left, connector_right, cross):
        line = connector_left
        for i, width in enumerate(col_widths):
            line += border["h"] * (width + 2) + cross
        line = line[:-1] + connector_right
        return line

    top_line = draw_hline(border["tl"], border["tr"], border["t"])
    mid_line = draw_hline(border["l"], border["r"], border["jn"])
    bot_line = draw_hline(border["bl"], border["br"], border["b"])

    # Header
    header_parts = [border["v"]]
    for i, name in enumerate(col_names):
        width = col_widths[i]
        pad_total = width - display_width(name)
    
        if align == "left":
            pad_left = 0
        elif align == "center":
            pad_left = math.floor(pad_total / 2)
        elif align == "right":
            pad_left = pad_total
        else:
            pad_left = 0

        pad_right = pad_total - pad_left
        header_parts.append(f" {' ' * pad_left}{name}{' ' * pad_right} {border['v']}")
    header = "".join(header_parts)

    # Type row
    type_parts = [border["v"]]
    for i, dtype in enumerate(col_types):
        dtype_formatted = f"\033[3m{dtype.lower()}{reset}"
        width = col_widths[i]
        pad_total = width - display_width(dtype)

        if align == "left":
            pad_left = 0
        elif align == "center":
            pad_left = math.floor(pad_total / 2)
        elif align == "right":
            pad_left = pad_total
        else:
            pad_left = 0

        pad_right = pad_total - pad_left
        type_parts.append(f" {' ' * pad_left}{dtype_formatted}{' ' * pad_right} {border['v']}")
    type_row = "".join(type_parts)

    # Data rows
    data_rows = []
    for row_idx in range(len(df)):
        row_parts = [border["v"]]
        for col_idx, col_name in enumerate(col_names):
            content = color_na(df[col_name][row_idx])
            width = col_widths[col_idx]
            pad_total = width - display_width(content)

            if align == "left":
                pad_left = 0
            elif align == "center":
                pad_left = math.floor(pad_total / 2)
            elif align == "right":
                pad_left = pad_total
            else:
                pad_left = 0

            pad_right = pad_total - pad_left
            row_parts.append(f" {' ' * pad_left}{content}{' ' * pad_right} {border['v']}")
        data_rows.append("".join(row_parts))

    # Print table
    print(top_line)
    print(header)
    print(type_row)
    print(mid_line)
    print("\n".join(data_rows))
    print(bot_line)

    return None

# Monkey-patch Polars DataFrame
pl.DataFrame.affiche = affiche

# Define the affiche() function
def affiche(align="left", na_color="\033[91;3m", theme="newspaper"):
    """
    Display a Polars DataFrame with formatted table borders and styling.
    
    Args:
        align: text alignment ("left", "center", "right")
        na_color: ANSI color code for missing values
        theme: border theme ("newspaper")
    
    Usage:
        df >> affiche()
    """
    def _affiche(df):

        # Handle empty DataFrame
        if df.shape[1] == 0 or df.shape[0] == 0:
            msg = "That table doesn't exist!"
            width = len(msg)
            top = f"╔{'═' * (width + 2)}╗"
            mid = f"║ {msg} ║"
            bot = f"╚{'═' * (width + 2)}╝"
            print(f"{top}\n{mid}\n{bot}")
            return None

        # Border theme
        if theme == "newspaper":
            border = {
                "h": "═", "v": "║",
                "tl": "╔", "tr": "╗",
                "bl": "╚", "br": "╝",
                "jn": "╬",
                "l": "╠", "r": "╣",
                "t": "╦", "b": "╩"
            }
        else:
            raise ValueError("Theme not supported. Try 'newspaper'")

        reset = "\033[0m"

        # Handle color for unique NA types
        def color_na(x):
            if x is None:
                return f"{na_color}null{reset}"
            return str(x)

        # Width calculator (ignores ANSI codes)
        def display_width(s):
            clean = re.sub(r'\033\[[0-9;]*[mK]', '', str(s))
            return len(clean)

        # Prepare display data
        col_names = df.columns
        # Pull column data types
        col_types = [str(dtype) for dtype in df.dtypes]
        
        # Abbreviate common type names
        type_abbrev = {
            "string": "str",
            "categorical": "cat",
            "boolean": "bool",
            "object": "obj",
            "decimal": "dec"
        }

        col_types = [type_abbrev.get(dtype.lower(), dtype) for dtype in col_types]
    
        # Column widths
        col_widths = []
        for i, col in enumerate(col_names):
            header_width = display_width(col)
            type_width = display_width(col_types[i])
            # Get column values and apply color_na
            col_values = [color_na(val) for val in df[col].to_list()]
            data_widths = [display_width(val) for val in col_values]
            col_widths.append(max([header_width, type_width] + data_widths))

        # Draw horizontal line
        def draw_hline(connector_left, connector_right, cross):
            line = connector_left
            for i, width in enumerate(col_widths):
                line += border["h"] * (width + 2) + cross
            line = line[:-1] + connector_right
            return line

        top_line = draw_hline(border["tl"], border["tr"], border["t"])
        mid_line = draw_hline(border["l"], border["r"], border["jn"])
        bot_line = draw_hline(border["bl"], border["br"], border["b"])

        # Header
        header_parts = [border["v"]]
        for i, name in enumerate(col_names):
            width = col_widths[i]
            pad_total = width - display_width(name)

            if align == "left":
                pad_left = 0
            elif align == "center":
                pad_left = math.floor(pad_total / 2)
            elif align == "right":
                pad_left = pad_total
            else:
                pad_left = 0

            pad_right = pad_total - pad_left
            header_parts.append(f" {' ' * pad_left}{name}{' ' * pad_right} {border['v']}")
        
        header = "".join(header_parts)

        # Type row
        type_parts = [border["v"]]
        for i, dtype in enumerate(col_types):
            dtype_formatted = f"\033[3m{dtype.lower()}{reset}"
            width = col_widths[i]
            pad_total = width - display_width(dtype)

            if align == "left":
                pad_left = 0
            elif align == "center":
                pad_left = math.floor(pad_total / 2)
            elif align == "right":
                pad_left = pad_total
            else:
                pad_left = 0

            pad_right = pad_total - pad_left
            type_parts.append(f" {' ' * pad_left}{dtype_formatted}{' ' * pad_right} {border['v']}")
        type_row = "".join(type_parts)

        # Data rows
        data_rows = []
        for row_idx in range(len(df)):
            row_parts = [border["v"]]
            for col_idx, col_name in enumerate(col_names):
                content = color_na(df[col_name][row_idx])
                width = col_widths[col_idx]
                pad_total = width - display_width(content)

                if align == "left":
                    pad_left = 0
                elif align == "center":
                    pad_left = math.floor(pad_total / 2)
                elif align == "right":
                    pad_left = pad_total
                else:
                    pad_left = 0

                pad_right = pad_total - pad_left
                row_parts.append(f" {' ' * pad_left}{content}{' ' * pad_right} {border['v']}")
            
            data_rows.append("".join(row_parts))

        # Print table
        print(top_line)
        print(header)
        print(type_row)
        print(mid_line)
        print("\n".join(data_rows))
        print(bot_line)
    
    return _affiche

# Export both for different use cases
__all__ = ['affiche']  # The function version for piping