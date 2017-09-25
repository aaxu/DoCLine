import os
import re
import colorama

INDENTATION = " " * 4
MARGIN_LEFT = 0
MARGIN_RIGHT = 3
ROWS, COLUMNS = [int(dim) for dim in
                 (os.popen('stty size', 'r').read().split())]

class Text:

    def __init__(self, text, indentation=INDENTATION,
                 margin_left=MARGIN_LEFT, margin_right=MARGIN_RIGHT):
        """
        Args:
            text: The text you want to format.
            indentation: The amount of indentation that you
                         want wraparounds to have.
            margin_left: The amount of empty space on the left side
                         of the screen you want the text to leave.
            margin_right: The amount of empty space on the right side
                          of the screen you want the text to leave.
        """
        self.text = text
        self.indentation = indentation
        self.margin_right = margin_right
        self.margin_left = margin_left

    def __blue_text(self, text):
        """
        Args:
            text: The string you want to print in blue.

        Returns:
            The same string, but will be blue when printed.
        """
        return self.__color_text(text, colorama.Fore.LIGHTBLUE_EX)

    def __yellow_text(self, text):
        """
        Args:
            text: The string you want to print in yellow.

        Returns:
            The same string, but will be yellow when printed.
        """
        return self.__color_text(text, colorama.Fore.LIGHTYELLOW_EX)

    def __color_text(self, text, color):
        """
        Args:
            text: The string that you want to print in color.
            color: The color that you want the string to print in.
                   This should be a colorama foreground color.

        Returns:
            A string that will be in color when printed.
        """
        return color + text + colorama.Style.RESET_ALL

    def __format_text_colors(self, text):
        # Make the header of each function yellow.
        # This regex matches anything of the forms
        # func_name(...) or func_name(self) or func_name(self, ...)
        text = re.sub(r'(\s\w+\((?:\.{3}|self.*)\)\s)',
                      self.__yellow_text(r'\1'), text)
        # Make all constant names blue.
        text = re.sub(r'(\s[A-Z0-9_\-]+\s*)(=)', self.__blue_text(r'\1') + r'\2', text)
        return text

    def __format_line_wrap(self, line):
        """
        Args:
            line: The line you want to format.

        Returns:
            A list of strings that you can print consecutively to
            output a nicely formatted text.
        """

        def format_line_with_indents(line, indent):
            """
            Args:
                line: The line you want to format.
                line_indent: The string indentation that a line should
                                  take when the line wraps around the screen.

            Returns:
                A list of strings that you can print consecutively to
                output a nicely formatted text.
            """
            list_of_lines = []
            next_line_indent = ''
            # Don't strip the first line, since it may be already formatted.
            if indent:
                line = line.strip()
            # Keep empty lines as they are used to space out sections in the text.
            if not line:
                return [""]
            margin_left_str = " " * self.margin_left
            line = margin_left_str + indent + line
            if len(line) <= COLUMNS - self.margin_right:
                return [line]
            break_line_at_index = COLUMNS - self.margin_right
            while (not line[break_line_at_index].isspace() and
                   break_line_at_index >= len(indent) + self.margin_left):
                break_line_at_index -= 1
            # Case for one really long word
            if break_line_at_index < len(indent) + self.margin_left:
                break_line_at_index = COLUMNS - self.margin_right
            list_of_lines.append(line[:break_line_at_index])
            leftover_string = line[break_line_at_index:]
            # Set the indentation for the wraparound text.
            if indent:
                next_line_indent = self.indentation
            else:
                current_line_indent = re.match(r'^\s*', line).group()
                num_indents = len(current_line_indent) - self.margin_left -\
                              len(indent)
                next_line_indent = num_indents * ' '
            list_of_lines.extend(format_line_with_indents(leftover_string,
                                                          next_line_indent))
            return list_of_lines

        return format_line_with_indents(line, '')

    def get_formatted_text(self):
        """
        Returns:
            The text in this object such that it wraps around the terminal
            and has colors when printed.
        """
        nice_text = re.sub(r'\|', r' ', self.text)
        lines = nice_text.split('\n')
        formatted_text = []
        for line in lines:
            split_lines = self.__format_line_wrap(line)
            # # TODO: Use these to highlight function signatures that wrap.
            # for i, segment in enumerate(split_lines):
            formatted_text.extend(split_lines)
        nice_text = '\n'.join(formatted_text)
        nice_text = self.__format_text_colors(nice_text)
        return nice_text

    def __str__(self):
        """
        Returns:
            Returns a formatted version of this object's text.
        """
        return self.get_formatted_text()
