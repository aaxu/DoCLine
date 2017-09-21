import os
import re
import sys
import subprocess
import colorama
from reppy.robots import Robots

USER_AGENT = 'DoCLine Parser (http://github.com/aaxu/docline)'
INDENTATION = " " * 4
ROWS, COLUMNS = [int(dim) for dim in
                 (os.popen('stty size', 'r').read().split())]
MARGIN_RIGHT = 3

def check_website_policy(url):
    """
    Args:
        url: The URL of the website you are trying to check.

    Returns:
        True if the website's policy allows you to scrape. Otherwise False.
    """
    robot_url = Robots.robots_url(url)
    robot = Robots.fetch(robot_url)
    return robot.allowed(url, USER_AGENT)

def blue_text(text):
    """
    Args:
        text: The string you want to print in blue.

    Returns:
        The same string, but will be blue when printed.
    """
    return color_text(text, colorama.Fore.BLUE)

def yellow_text(text):
    """
    Args:
        text: The string you want to print in yellow.

    Returns:
        The same string, but will be yellow when printed.
    """
    return color_text(text, colorama.Fore.LIGHTYELLOW_EX)

def color_text(text, color):
    """
    Args:
        text: The string that you want to print in color.
        color: The color that you want the string to print in.
               This should be a colorama foreground color.

    Returns:
        A string that will be in color when printed.
    """
    return color + text + colorama.Style.RESET_ALL

def format_text_colors(text):
    # Make the header of each function yellow.
    # This regex matches anything of the forms
    # func_name(...) or func_name(self) or func_name(self, ...)
    text = re.sub(r'(\w+\((?:\.{3}|self.*)\))', yellow_text(r'\1'), text)
    # Make all constant names blue.
    text = re.sub(r'(\s[A-Z0-9_\-]*\s=)', blue_text(r'\1'), text)
    return text

def format_line_wrap(line):
    """
    Args:
        line: The line you want to format.

    Returns:
        A list of strings that you can print consecutively to output
        a nicely formatted text.
    """
    def format_line_with_indents(line, indent):
        """
        Args:
            line: The line you want to format.
            line_indent: The string indentation that a line should
                              take when the line wraps around the screen.

        Returns:
            A list of strings that you can print consecutively to output
            a nicely formatted text.
        """
        output = []
        next_line_indent = ''
        # Don't strip the first line, since it may be already formatted.
        if indent:
            line = line.strip()
        else:
            # Set the indentation for the wraparound text.
            current_line_indent = re.match(r'^\s*', line).group()
            next_line_indent = current_line_indent + INDENTATION
        # Keep empty lines as they are used to space out sections in the text.
        if not line:
            return [""]
        line = indent + line
        if len(line) <= COLUMNS - MARGIN_RIGHT:
            return [line]
        break_line_at_index = COLUMNS - MARGIN_RIGHT
        while (not line[break_line_at_index].isspace() and
               break_line_at_index >= len(indent)):
            break_line_at_index -= 1
        # Case for one really long word
        if break_line_at_index < len(indent):
            break_line_at_index = COLUMNS - MARGIN_RIGHT
        output.append(line[:break_line_at_index])
        leftover_string = line[break_line_at_index:]
        output.extend(format_line_with_indents(leftover_string,
                                               next_line_indent))
        return output
    return format_line_with_indents(line, '')

def main():
    """
    Main logic of the program.

    Returns:
        None.
    """
    command = sys.argv
    sys.argv[0] = 'pydoc'
    output = subprocess.check_output(command)
    output = re.sub(r'\|', r' ', output)
    lines = output.split('\n')
    formatted_text = []
    for line in lines:
        formatted_text.extend(format_line_wrap(line))
    output = "\n".join(formatted_text)
    output = format_text_colors(output)
    print '\n', output

if __name__ == '__main__':
    colorama.init()
    main()
