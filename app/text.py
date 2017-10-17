import os
import re
import colorama

INDENTATION = " " * 4
MARGIN_LEFT = 0
MARGIN_RIGHT = 2
ROWS, COLUMNS = [int(dim) for dim in
                 (os.popen('stty size', 'r').read().split())]

class Text:
    """
    This class is used to take in a text and outputs it nicely on the terminal
    such that function signatures and function names are colored and long lines
    should wrap around the terminal without breaking in the middle of words.
    """

    def __init__(self, text='', indentation=INDENTATION,
                 margin_left=MARGIN_LEFT, margin_right=MARGIN_RIGHT):
        """
        Args:
            text (string): The text you want to format.
            indentation (string): The amount of indentation that you
                                  want wraparounds to have.
            margin_left (int): The amount of empty space on the left side
                               of the screen you want the text to leave.
            margin_right (int): The amount of empty space on the right side
                                of the screen you want the text to leave.
        """
        self.text = text
        self.indentation = indentation
        self.margin_right = margin_right
        self.margin_left = margin_left
        self.function_regex = re.compile(r'^([\s\|]*)([\w_\.]+\s*(?:=|->|=>)?\s*[\w_\.]+\([^\)]*\))(\s*)$')
        self.constant_regex = re.compile(r'^([\s\|]*)([A-Z0-9_\-]+)(\s*)=')
        self.section_regex1 = re.compile(r'^([\s\|]*)([A-Z_]+[A-Z_ \t\d]*)(\s*)$')
        self.section_regex2 = re.compile(r'^([\s\|]*)(.+)(:)$')

    @classmethod
    def color_text(cls, text, color):
        """
        Args:
            text (string): The string that you want to print in color.
            color (string): The color that you want the string to print in.
                            This should be a colorama foreground color.

        Returns:
            A string that will be in color when printed.
        """
        return color + text + colorama.Style.RESET_ALL

    @classmethod
    def yellow_text(cls, text):
        """
        Args:
            text (string): The string you want to print in yellow.

        Returns:
            The same string, but will be yellow when printed.
        """
        return Text.color_text(text, colorama.Fore.LIGHTYELLOW_EX)

    @classmethod
    def blue_text(cls, text):
        """
        Args:
            text (string): The string you want to print in blue.

        Returns:
            The same string, but will be blue when printed.
        """
        return Text.color_text(text, colorama.Fore.LIGHTBLUE_EX)

    @classmethod
    def magenta_text(cls, text):
        """
            Args:
                text (string): The string you want to print in magenta.

            Returns:
                The same string, but will be magenta when printed.
        """
        return Text.color_text(text, colorama.Fore.LIGHTMAGENTA_EX)

    def __format_line_wrap(self, line):
        """
        Args:
            line (string): The line you want to format.

        Returns:
            A list of strings that you can print consecutively to
            output a nicely formatted text.
        """

        def format_line_with_indents(line, indent):
            """
            Args:
                line: The line you want to format.
                indent: The string indentation that a line should
                        take when the line wraps around the screen.

            Returns:
                A list of strings that you can print consecutively to
                output a nicely formatted text.
            """
            # Don't strip the first line, since it may be already formatted.
            if indent:
                line = line.strip()
            # Keep empty lines as they are used to space out sections in the text.
            if not line:
                return [""]
            current_indent = " " * self.margin_left + indent
            line = current_indent + line
            if len(line) <= COLUMNS - self.margin_right:
                return [line]
            break_line_at_index = COLUMNS - self.margin_right
            while (not line[break_line_at_index].isspace() and
                   break_line_at_index >= len(current_indent)):
                break_line_at_index -= 1
            # Case for one really long word
            if break_line_at_index < len(current_indent):
                break_line_at_index = COLUMNS - self.margin_right
            # Set the indentation for the wraparound text.
            if indent:
                next_indent = indent
            else:
                current_indent = (re.match(r'^\s*[^\w\s]*\s*', line).group())
                next_indent = (current_indent[self.margin_left:] +
                               self.indentation)
            first_line = line[:break_line_at_index]
            if not first_line.strip():
                return [line[break_line_at_index:]]
            rest_of_lines = format_line_with_indents(line[break_line_at_index:],
                                                     next_indent)
            return [first_line] + rest_of_lines

        return format_line_with_indents(line, '')

    def __format_line_colors(self, line):
        """
        Takes in a string colors it depending on whether
        it is a function, section header, or constant definition.
        Args:
            line (string): The line you want to check.

        Returns:
            The string but colored if printed.
        """
        function_match = self.is_function_header(line)
        constant_match = self.is_constant_definition(line)
        section_match = self.is_section_header(line)
        if function_match:
            function_text = function_match.group(2)
            return line.replace(function_text, Text.yellow_text(function_text))
        elif constant_match:
            constant_text = constant_match.group(2)
            return line.replace(constant_text, Text.blue_text(constant_text))
        elif section_match:
            section_text = section_match.group(2)
            return line.replace(section_text, Text.magenta_text(section_text))
        return line

    def get_formatted_text(self):
        """
        Returns:
            The text (string) in this object such that it wraps
            around the terminal and has colors when printed.
        """
        lines = self.text.split('\n')
        formatted_text = []
        for line in lines:
            split_lines = self.__format_line_wrap(line)
            formatted_line = '\n'.join(split_lines)
            colored_line = self.__format_line_colors(formatted_line)
            formatted_text.append(colored_line)
        nice_text = '\n'.join(formatted_text)
        return nice_text

    def get_text(self):
        """
        Returns:
            The raw text inside this Text object.
        """
        return self.text

    def is_function_header(self, text):
        """
        This regex matches anything of the forms
        func_name(...) or func_name(self) or func_name(self, ...)

        Args:
            text (string): The text you want to check.

        Returns:
            The regex match object if the text is a function header.
            Otherwise, None.
        """
        return self.function_regex.search(text)

    def is_constant_definition(self, text):
        """
        This regex checks if the line starts with a word
        in all caps and assigns a value to it.

        Args:
            text (string): The text you want to check.

        Returns:
            The regex match object if the text is a constant definition.
            Otherwise, None.
        """
        return self.constant_regex.search(text)

    def is_section_header(self, text):
        """
        This regex checks if text is a section header that starts with
        a word that is all caps, or beings with "Help on".
        Args:
            text (string): The text you want to check.

        Returns:
            The regex match object if the text is a section header.
            Otherwise, None.
        """
        return (self.section_regex1.search(text) or
                self.section_regex2.search(text))


    def set_text(self, text):
        """
        Args:
            text (string): The new string to put into this Text object.

        Returns:
            None.
        """
        self.text = text

    def __str__(self):
        """
        Returns:
            Returns a formatted version of this object's text.
        """
        return self.get_formatted_text()
