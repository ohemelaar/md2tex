#!/usr/bin/python
# coding: utf-8

import mistune
import bs4
from bs4 import BeautifulSoup

input = open("input.md", "r")
output = open("converted.tex", "w")
md = input.read()
html = mistune.markdown(md)
soup = BeautifulSoup(html, "html.parser")

def tex_output(html_soup):
    result = ""
    for child in list(html_soup.children):
        tagname = child.name
        if tagname == None:
            result += unicode(child)
        elif tagname == "p":
            result += tex_output(child)
        elif tagname == "em":
            result += "\\textit{{{0}}}".format(tex_output(child))
        elif tagname == "strong":
            result += "\\textbf{{{0}}}".format(tex_output(child))

        elif tagname == "h1":
            # Here we assume there's only one level 1 title in the document!
            result += "\\part*{{{0}}}\\renewcommand{{\\contentsname}}{{Sommaire}}\\tableofcontents\\newpage\n".format(tex_output(child))
        elif tagname == "h2":
            result += "\\section{{{0}}}".format(tex_output(child))
        elif tagname == "h3":
            result += "\\subsection{{{0}}}".format(tex_output(child))
        elif tagname == "h4":
            result += "\\subsubsection{{{0}}}".format(tex_output(child))
        elif tagname == "h5":
            result += "\\paragraph{{{0}}}".format(tex_output(child))

        elif tagname == "ul":
            result += "\n\\begin{{itemize}}\n{0}\\end{{itemize}}\n".format(tex_output(child))
        elif tagname == "ol":
            result += "\n\\begin{{enumerate}}\n{0}\\end{{enumerate}}\n".format(tex_output(child))
        elif tagname == "li":
            result += "\\item {0}\n".format(tex_output(child))

        elif tagname == "code":
            result += "\\texttt{{{0}}}".format(tex_output(child))
        elif tagname == "pre":
            # A pre tag contains a code tag and no other formatting should occur to it, so we fetch it directly with no recursive call
            # TODO make listings
            result += "\\texttt{{{0}}}".format(child.find("code").string)
        elif tagname == "img":
            # TODO implement images as figures
            result += ""
    return(result)

output.write(tex_output(soup))
output.close()
