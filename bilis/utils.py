def html_color_to_int(color):
    #strip possible leading hash symbol
    if not is_hex(color[0]):
        color = color[1:]
    return int(color,16)
    
def int_to_html_color(value):
    color = "#"+hex(value)
    return "#{:06X}".format(value)
    
def is_hex(x):
    try:
        int(x,16)
        return True
    except ValueError:
        return False