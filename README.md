# Markdown to LaTeX converter

This piece of python script will convert a markdown file to a LaTeX file.

## Why?

I made this script for my own use during college. We would take a lot of notes during classes using hackmd.io with other students. Sometimes, we had to turn in a correctly formatted report using those notes, so the idea of making a markdown to latex converter came to mind.

## Doesn't it already exist?

Yes it does, and it's probably implemented in a better way out there. But I wanted to be able to specifically design how the conversions would happen for each tag.

## How is it done?

The input markdown is parsed into HTML using mistune (https://github.com/lepture/mistune). We then navigate the HTML output using BeautifulSoup (https://www.crummy.com/software/BeautifulSoup/) in order to distinguish each tag and apply the correct LaTeX conversion to it.

## How to use it?
For now, just running the script takes the input.md file and outputs the conversion in the converted.tex file.
