#!/usr/bin/python
# coding: utf-8

import hashlib
import mistune
import bs4
from bs4 import BeautifulSoup
import urllib
import os.path

input = open("input.md", "r")
output = open("converted.tex", "w")
md = input.read()
html = mistune.markdown(md)
soup = BeautifulSoup(html, "html.parser")

def latex_escape(text):
    text = text.replace("\\", "\\textbackslash")
    text = text.replace("&", "\\&")
    text = text.replace("%", "\\%")
    text = text.replace("$", "\\$")
    text = text.replace("#", "\\#")
    text = text.replace("_", "\\_")
    text = text.replace("{", "\\{")
    text = text.replace("}", "\\}")
    text = text.replace("~", "\\textasciitilde")
    text = text.replace("^", "\\textasciicircum")
    return text

def tex_output(html_soup):
    result = ""
    for child in list(html_soup.children):
        tagname = child.name
        if tagname == None:
            result += latex_escape(unicode(child).encode("utf-8"))
        elif tagname == "p":
            result += tex_output(child)
        elif tagname == "em":
            result += "\\textit{{{0}}}".format(tex_output(child))
        elif tagname == "strong":
            result += "\\textbf{{{0}}}".format(tex_output(child))

        elif tagname == "h1":
            # Here we assume there's only one level 1 title in the document!
            result += "\\part*{{{0}}}\n\\renewcommand{{\\contentsname}}{{Sommaire}}\\tableofcontents\\newpage\n".format(tex_output(child))
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
            lstlisting_format = "\n\\begin{{lstlisting}}\n{0}\n\\end{{lstlisting}}\n"
            result += lstlisting_format.format(child.find("code").string)

        elif tagname == "img":
            src = child["src"]
            # We use hases to make sure two images with the same name won't conflict
            src_hash = hashlib.md5(src).hexdigest()
            extension = src.split(".")[-1]
            img_path = "img/" + src_hash + "." + extension
            try:
                if not os.path.isfile(img_path):
                    print("An image has to be downloaded.")
                    urllib.urlretrieve(src, img_path)
                else:
                    print("Image already exists, not downloading it again.")
            except IOError:
                print("Downloading the image failed")
            else:
                alt = child["alt"]
                image_format = "\n\\begin{{figure}}[h]\n\\centering\n\\includegraphics[width=0.7\\linewidth]{{{0}}}\n\\caption{{{1}}}\n\\end{{figure}}\n"
                result += image_format.format(img_path, alt)
    return(result)

output.write(tex_output(soup))
output.close()
