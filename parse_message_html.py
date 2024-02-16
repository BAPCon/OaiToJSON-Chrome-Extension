from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

def parse_html_content_to_markdown(content: str) -> str:
    """
    Parses HTML content to Markdown, performing substitutions and formatting elements appropriately.

    Args:
    - content (str): The innerHTML of the `<div>` with class "markdown-content".

    Returns:
    - str: The content formatted in Markdown.
    """
    # Apply initial Markdown substitutions for simple HTML tags.
    content = apply_markdown_substitutions(content)

    # Parse the modified HTML content.
    soup = BeautifulSoup(content, 'html.parser')

    # Format top-level elements and collect them.
    return "\n".join([format_element_as_markdown(child) for child in soup.children])

def format_element_as_markdown(element: Tag) -> str:
    """
    Formats a BeautifulSoup Tag element as Markdown.

    Args:
    - element (Tag): The HTML element to be formatted.

    Returns:
    - str: The element formatted in Markdown.
    """
    prefix = ""
    suffix = ""
    is_code_block = False

    # Handle headers (h1, h2, etc.)
    if element.name.startswith('h'):
        prefix = "#" * int(element.name[1:]) + " "
    elif element.name == 'code':
        # Inline code formatting.
        prefix, suffix = "``", "``"
    elif "code-sample" in element.get('class', []):
        is_code_block = True
        code_block = element.find("code", class_=None)

        # Remove line numbers or any non-code elements.
        if code_block:
            code_block.decompose()

        # Attempt to identify the programming language used in the code block.
        language = determine_code_language(element)

        return f'```{language}\n{element.text.strip()}\n```'

    sections = [format_section_as_markdown(section) for section in element.contents if not is_code_block]

    return prefix + "".join(sections).strip() + suffix

def format_section_as_markdown(section) -> str:
    """
    Formats a section of content, handling both string and tag elements.

    Args:
    - section: A BeautifulSoup element or string to format.

    Returns:
    - str: The formatted content.
    """
    if isinstance(section, NavigableString):
        return section
    elif isinstance(section, Tag):
        return format_element_as_markdown(section)
    return ""

def determine_code_language(element: Tag) -> str:
    """
    Attempts to determine the programming language of a code block.

    Args:
    - element (Tag): The 'code-sample' classed element containing a code block.

    Returns:
    - str: The identified language or 'html' as a default.
    """
    try:
        code_block = element.find("code")
        language = code_block['class'][0].split('-')[-1]
    except KeyError:
        language = "html"

    return language

def apply_markdown_substitutions(content: str) -> str:
    """
    Replaces specific HTML tags with Markdown equivalents.

    Args:
    - content (str): The HTML content to transform.

    Returns:
    - str: The content with applied Markdown substitutions.
    """
    replacements = {
        "<strong>": "**",
        "</strong>": "**",
        "<em>": "*",
        "</em>": "*",
        "<li>": "- ",
        "</li>": "\n"
    }

    for html_tag, markdown in replacements.items():
        content = content.replace(html_tag, markdown)

    return content