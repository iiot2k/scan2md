# Copyright 2021 Ocean (iiot2k@gmail.com) 
# All rights reserved.

import sys
import string
import os

# skip all whitespace character
def skipwhite(line, pos):
    while(pos < len(line)):
        if line[pos] in string.whitespace:
            pos += 1
        else:
            break
    return pos 

# scan until end of line
def findend(line, pos):
    while(pos < len(line)):
        if line[pos] == '\n' or line[pos] == '\r':
            break
        else:
            pos += 1
    return pos 

# skip up to blank character
def skiptoblank(line, pos):
    while(pos < len(line)):
        if line[pos] == ' ' or line[pos] == '\t':
            break
        else:
            pos += 1
    return pos

# look for tagname
def get_tagname(line):
    if len(line) == 0:
        return ""

    if line.find("@@") != -1:
        return "@"

    line = line.strip()

    pos = line.find("@")
    if pos == -1:
        return ""

    pos += 1
    pos2 = skiptoblank(line, pos)
    return line[pos: pos2]

# get param of tagname:
def get_param(line, tagname):
    line = line.strip()
    pos = line.find(tagname)
    pos += len(tagname)
    pos = skipwhite(line, pos);
    return line[pos:]

#class Markdown
class Markdown:
    def __init__(self, codetype):
        self.fo = None
        self.indent = ""

        # default is c
        if codetype == "":
            self.def_code = "c"
        else:
            self.def_code = codetype

        # set delimeter
        if self.def_code == "c" or self.def_code == "cpp" or self.def_code == "csharp" or self.def_code == "javascript":
            self.start_block = "/*!"
            self.end_block = "*/"
        elif self.def_code == "python":
            self.start_block = "'''!"
            self.end_block = "'''"

        self.init_function()

    # init storage for function
    def init_function(self):
        self.a_param = []
        self.a_return = []
        self.a_errreturn = []
        self.a_throw = []

    # open markdown file
    def open(self, fname):
        try:
            self.fo = open(fname, 'w', encoding="utf-8")
            return True 
        except:
            print("error on open file " + fname)
            return False 

    def close(self):
        self.fo.close()

    # write to markdown file
    def write_nl(self, line):
        try:
            self.fo.write(line + "\n")
        except:
            self.fo.close()
            print("error on write file " + self.fo.name)
            sys.exit()

    # write to markdown file with end <br>
    def write(self, line):
        self.write_nl(line + "<br>")

    # split text and bolds first element
    def bold_first(self, line):
        if len(line) == 0:
            return ""
        sline = line.split(" ", 1)
        if len(sline) == 1:
            return ' **' + sline[0] + '** '
        elif len(sline) == 2:
            return ' **' + sline[0] + '** ' + sline[1] 

    # scan all tags in comment block
    def scan_tags(self, block):
        pos = 0
        posend = 0
        code_block = False
        isfunction = False
        self.init_function()

        # scan block
        while pos < len(block):
            posend = findend(block, pos)
            line = block[pos: posend]

            #find tag
            tag = get_tagname(line)

            # handle @@
            if tag == "@":
                line = line.replace("@@", "@")
                tag = ""

            # normal text line ?
            if tag == "":
                # is code block ?
                if code_block:
                    self.write_nl(line)
                    pos = posend + 1;
                    continue

                #skip empty lines
                line = line.strip()
                if len(line) == 0:
                    pos = posend + 1
                    continue

                # special md text start with $
                if line[0] == "$":
                    self.write(line[1:])
                else:
                    self.write(self.indent + line)
                pos = posend + 1
                continue

            # end codeblock
            if code_block == True:
                self.write_nl("```")
                code_block = False

            #get tagname parameter
            tparam = get_param(line, tag)

            # @brief <text>
            if tag == "brief":
                self.write(tparam)

            # @fn <description>
            elif tag == "fn":
                self.write(self.indent + u"💠Function: " + tparam)
                isfunction = True

            # @param <name> <description>
            elif tag == "param":
                if isfunction == True:
                    self.a_param.append(tparam)

            # @return <description>
            elif tag == "return":
                if isfunction == True:
                    self.a_return.append(tparam)

            # @return[error] <description>
            elif tag == "return[error]":
                if isfunction == True:
                    self.a_errreturn.append(tparam)

            # @throw <description>
            elif tag == "throw":
                if isfunction == True:
                    self.a_throw.append(tparam)

            # @class <name> <description>
            elif tag == "class":
                self.write(self.indent + u"💎Class: " + self.bold_first(tparam))
                self.indent += ">"

            # @union <name> <description>
            elif tag == "union":
                self.write(self.indent + u"🔳Union: " + self.bold_first(tparam))
                self.indent += ">"

            # @struct <name> <description>
            elif tag == "struct":
                self.write(self.indent + u"🔲Struct: " + self.bold_first(tparam))
                self.indent += ">"

            # @interface <name> <description>
            elif tag == "interface":
                self.write(self.indent + u"🔑Interface: " + self.bold_first(tparam))
                self.indent += ">"

            # @namespace <name> <description>
            elif tag == "namespace":
                self.write(self.indent + u"📇Namespace: " + self.bold_first(tparam))

            # @typedef <name> <description>
            elif tag == "typedef":
                self.write(self.indent + u"🔨Typedef: " + self.bold_first(tparam))

            # @def <name> <description>
            elif tag == "def":
                self.write(self.indent + u"🔟Const: " + self.bold_first(tparam))

            # @enum <name> <description>
            elif tag == "enum":
                self.write(self.indent + u"🔢Enum: " + self.bold_first(tparam))

            # @var <name> <description>
            elif tag == "var":
                self.write(self.indent + u"✳️Variable: " + self.bold_first(tparam))

            # @global <name> <description>
            elif tag == "global":
                self.write(self.indent + u"🌐Global: " + self.bold_first(tparam))

            # @static <description>
            elif tag == "static":
                self.write(self.indent + u"🌲Static: " + tparam)

            # @public <description>
            elif tag == "public":
                self.write(self.indent + u"📢Public: " + tparam)

            # @private <description>
            elif tag == "private":
                self.write(self.indent + u"🔒Private: " + tparam)

            # @overload <description>
            elif tag == "overload":
                self.write(self.indent + u"⏬Overload: " + tparam)

            # @virtual <description>
            elif tag == "virtual":
                self.write(self.indent + u"👻Virtual: " + tparam)

            # @-- (horizontal line)
            elif tag == "--":
                self.write_nl("--- ")

            # @n (new line)
            elif tag == "n":
                self.write_nl("")

            # @b (break add <br>)
            elif tag == "b":
                self.write("")

            # @sa [>] (set indent)
            elif tag == "sa":
                if tparam == "":
                    self.indent = ""
                else: 
                    self.indent = tparam

            # @tablehead col1, col2, coln
            elif tag == "tablehead":
                firstline = ""
                secondline = ""
                tparam_split = tparam.split(",")
                for col in tparam_split:
                    col = col.strip()
                    firstline += "|" + col
                    secondline += "|---"
                firstline += "|"
                secondline += "|"
                self.write_nl(firstline)
                self.write_nl(secondline)

            # @table t1, t2, tn
            elif tag == "table":
                firstline = ""
                tparam_split = tparam.split(",")
                for col in tparam_split:
                    col = col.strip()
                    firstline += "|" + col
                firstline += "|"
                self.write_nl(firstline)

            # @file <filename> 
            elif tag == "file":
                self.write(u"💾 " +  tparam)

            # @copyright <description> 
            elif tag == "copyright":
                self.write(u"🧾 " +  tparam)

            # @date <date> 
            elif tag == "date":
                self.write(u"📆 " +  tparam)

            # @name <name> <description>
            elif tag == "name":
                self.write(">## " + self.bold_first(tparam))

            # @version <version> 
            elif tag == "version":
                self.write(u"⚙️ " + tparam)

            # @author <name> 
            elif tag == "author":
                self.write(u"✏️ " + tparam)

            # @todo <todo> 
            elif tag == "todo":
                self.write(u"❓ ToDo: " + tparam)

            # @warning <warning> 
            elif tag == "warning":
                self.write(u"⚠️ " + tparam)

            # @emoj <emojename> 
            elif tag == "emoj":
                self.write(":" + tparam + ":")

            # @mainpage <filename> [text] 
            elif tag == "mainpage":
                ap = tparam.split(" ", 1)
                if len(ap) == 1:
                    self.write(u"🏠 " + "[Main Page](" + ap[0] + ")")
                elif len(ap) == 2:
                    self.write(u"🏠 " + "[" + ap[1] + "](" + ap[0] + ")")

            # @link <filename> [text] 
            elif tag == "link":
                ap = tparam.split(" ", 1)
                if len(ap) == 1:
                    self.write(u"📌 " + "[Link](" + ap[0] + ")")
                elif len(ap) == 2:
                    self.write(u"📌 " + "[" + ap[1] + "](" + ap[0] + ")")

            # @image <filename> 
            elif tag == "image":
                self.write("![image](" + tparam + ")")

            # @code [codetype] 
            elif tag == "code":
                if tparam == "":
                    self.write_nl("```" + self.def_code)
                else:
                    self.write_nl("```" + tparam)
                code_block = True

            pos = posend + 1
        #while

        # on code block finish code
        if code_block == True:
            self.write_nl("```")

        # add new line
        self.write_nl("")

        return isfunction

    #write function block
    def write_function(self):
        # write parameters
        for tparam in self.a_param:
            self.write(self.indent + "- ▶️Param: " + self.bold_first(tparam))

        # write returns
        for tparam in self.a_return:
            self.write(self.indent + u"- ✅Return: "  + tparam)

        # write error returns
        for tparam in self.a_errreturn:
            self.write(self.indent + u"- ❌Return: "  + tparam)

        # write throws
        for tparam in self.a_throw:
            self.write(self.indent + u"- ⛔️Throw: " + tparam)

    # scan file
    def scan_file(self, file_out, sourcefile):
        # open output file 
        if self.open(file_out) == False:
            return

        # start on first pos
        pos = 0
        
        # scan file
        while pos < len(sourcefile):
            # find block start
            pos = sourcefile.find(self.start_block, pos)
            if pos == -1:
                break;
            
            #skip block start
            pos += len(self.start_block)

            # find end of block
            pos2 = sourcefile.find(self.end_block, pos)
            if pos2 == -1:
                break

            # get tags whithin block
            isfunction = self.scan_tags(sourcefile[pos: pos2])
            
            #skip end block
            pos = pos2 + len(self.end_block)

            # if a function, next line must be a function declaration
            if isfunction == True:
                if pos < len(sourcefile):
                    pos = skipwhite(sourcefile, pos)
                    pos2 = findend(sourcefile, pos)
                    line = sourcefile[pos: pos2]
                    pos = pos2 + 1

                    # look for a function
                    if line.find("(") != -1 and line.find(")") != -1:
                        self.write_nl("```" + self.def_code + " ")
                        self.write_nl(line)
                        self.write_nl("```")
                        self.write_function()

        #close file
        self.close()

# program entrty point
def main():
    #check param
    if len(sys.argv) != 3:
        print("usage: python scan2md <inputfile.ext> <outputfile.md>")
        return

    #get parameter
    file_in = sys.argv[1]
    file_out = sys.argv[2]

    # read input file
    try:
        fin = open(file_in, 'r')
        sourcefile = fin.read()
        fin.close()
    except:
        print("error on read file " + file_in)
        return
    
    # default code type c
    codetype = "c"

    # get extension
    basename, ext = os.path.splitext(file_in)

    # set code type from input file
    if ext == ".cpp" or ext == ".hpp":
        codetype = "cpp"
    if ext == ".cs":
        codetype = "csharp"
    elif ext == ".py":
        codetype = "python"
    elif ext == ".js":
        codetype = "javascript"

    # init markdown file
    markdown = Markdown(codetype)
  
    # scan input and write to markdown file
    markdown.scan_file(file_out, sourcefile)

if __name__ == "__main__":
    main()





