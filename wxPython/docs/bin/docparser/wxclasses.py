import wx
import restconvert
html_heading = "<H3><font color=\"red\">%s</font></H3>"

import HTMLParser
class HTMLStripper(HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_fed_data(self):
        return ''.join(self.fed)

def stylesAsHtml(styles, extraStyles=False):
    heading = "Window styles"
    if extraStyles:
        heading = "Extra window styles"
        
    html = html_heading % heading
    html += """<table width="95%">"""
    for style in styles:
        html += "<tr><td>%s</td><td>%s</td>" % (style[0], style[1])
        
    html += "</table>"
    
    return html
    
def commentizeText(text, indent=4):
    outtext = ""
    midtext = text
    midtext = midtext.replace("\n\n\n", "\n\n")
    for line in midtext.split("\n"):
        outtext += (" " * indent) + "* " + line + "\n"
        
    return outtext
    
def stripExtraNewlines(text):
    outtext = text.strip()
    while len(outtext) > 1 and outtext[0] == "\n":
        outtext = outtext[1:]
        
    while len(outtext) > 1 and outtext[-1] == "\n":
        outtext = outtext[0:-1]

    return outtext 
    
class wxClass:
    def __init__(self, name, description="", derivedFrom=[], styles=[], extrastyles=[]):
        self.name = name
        self.description = description
        self.derivedFrom = derivedFrom
        self.styles = styles
        self.extrastyles = extrastyles
        self.methods = {}
        self.propConflicts = []
        self.props = []
        
    def asHtml(self):
        html = "<H1>%s</H1>" % self.name
        html += self.description
        if len(self.derivedFrom) > 0:
            html += html_heading % "Derived from"
            for der in self.derivedFrom:
                derurl = der.replace("wx.", "wx").lower()
                html += "<a href=\"wx_%s.html\">%s</a></br>" % (derurl, der)
                
        if len(self.styles) > 0:
            html += stylesAsHtml(self.styles)
            
        if len(self.extrastyles) > 0:
            html += stylesAsHtml(self.extrastyles, extraStyles=True)
            
        return html
        
    def asReST(self):
        restText = "DocStr(%s,\n" % (self.name)
        
        restText += ");"
        return restText
        
    def asDoxygen(self, indent=0):
        doxytext = "\n"
        doxytext += "\\class " + self.name + "\n\n"
        doxytext += self.description.strip() + "\n\n"
        
        doxytext = doxytext.replace("<P>", "\n")
        
        x = HTMLStripper()
        x.feed(doxytext)

        doxytext = "/**\n%s*/\n\n" % commentizeText(x.get_fed_data(), indent)  + (" " * indent)
        return doxytext
        
    def createProps(self):
        propsText = ""
        propList = self.props
        for conflict in self.propConflicts:
            if conflict in propList:
                propList.remove(conflict)
        
        basename = self.name.replace("wx", "")                
        for prop in propList:
            if prop != "":
                propname = prop
                if propname[0] == "3":
                    propname = "Three" + propname[1:]
                
                getter = "wx.%s.Get%s" % (basename, prop)
                setter = "wx.%s.Set%s" % (basename, prop)
                propsText += "wx.%s.%s = property(%s" % (basename, propname, getter) 
                hasSetter = eval("(\"%s\" in dir(wx.%s))" % ("Set" + prop, basename))
                if hasSetter:
                    propsText += ", %s" % setter
                propsText += ")\n"
        
        if propsText != "":
            propsText += "\n\n"
        
        return propsText
                
class wxMethod:
    def __init__(self, name, parent, prototypes=[], params={}, description="", remarks=""):
        self.name = name
        self.parent = parent
        self.prototypes = prototypes
        self.params = params
        self.description = description
        self.remarks = remarks
        self.pythonNote = ""
        self.pythonOverrides = []
        
    def asReST(self):
        restText = ""
        
        # The below code converts prototypes into ReST, but currently isn't 
        # needed. Left here in case we change approach later.
        
        #for proto in self.prototypes:
        #    restText += proto[1] + "("
        #    counter = 1
        #    for arg in proto[2]:
        #        restText += "%s %s" % (arg[0].replace("wx.", ""), arg[1])
        #        if counter < len(proto[2]):
        #            restText += ", "
        #        counter += 1
        #    if proto[0] != "":
        #        restText += "-> " + proto[0]
        #    restText += "\n"
        #restText += "\n"
        
        if len(self.params) > 0:
            
            for param in self.params:
                restText += "\n:param %s: %s" % (param[0], restconvert.htmlToReST(param[1]))
            restText += "\n\n"
        
        restText += restconvert.htmlToReST(self.description.strip())
        return restText
        
    def asHtml(self):
        anchorname = self.getAnchorName()
        retval = "<A name=\"%s\"></A>" % (anchorname)
        retval += "<H3>%s</H3>" % self.name
        if len(self.pythonOverrides) > 0:
            for myfunc in self.pythonOverrides:
                retval += "<p><b>%s</b></br>%s</p>" % (myfunc[0], myfunc[1])
        else:
            for proto in self.prototypes:
                retval += "<P><B>"
                if proto[0] != "":
                    retval += proto[0] + " "
                retval += proto[1] + "("
                counter = 1
                for arg in proto[2]:
                    retval += "%s <i>%s</i>" % (arg[0], arg[1])
                    if counter < len(proto[2]):
                        retval += ", "
                    counter += 1
                retval += ")</B></P>"
            
        if len(self.params) > 0:
            retval += "<table width=\"90%%\" cellspacing=\"10\">"
            for param in self.params:
                retval += "<tr><td align=\"right\"><i>%s</i></td><td bgcolor=\"#E3E3E3\">%s</td></tr>" % (param[0], param[1])
            retval += "</table>"
            
        retval += "<p>%s</p>" % self.description
        
        if self.remarks != "":
            retval += "<font color=\"red\">Remarks</font><h4>%s</h4></font>" % self.remarks
        
        return retval
        
    def asDoxygen(self, indent=4):
        doxytext = ""
        
        doxytext += self.description.strip() + "\n\n"
        for param in self.params:
            doxytext += "@param " + param[0] + " \n" + param[1] + "\n\n"
        
        #if len(self.prototypes) > 0:
        #    proto = self.prototypes[0]
        #    type = proto[0]
        #    type = type.replace("virtual ", "")
        #    if type.strip() == "void":
        #        type = ""
        #    if type != "":
        #        doxytext += "\n\\return " + proto[0]
        
        #doxytext += ""
        #    counter = 1
        #    for arg in proto[2]:
        #        doxytext += "%s %s" % (arg[0], arg[1])
        #        if counter < len(proto[2]):
        #            doxytext += ", "
        #        counter += 1
        #    doxytext += ");\n\n\n"
        
        doxytext = doxytext.replace("<P>", "\n")
        doxytext = doxytext.replace("\n\n\n", "\n")
        
        # TODO convert supported HTML tags before doing this
        x = HTMLStripper()
        x.feed(doxytext)
        
        doxytext = "/**\n%s%s*/" % (commentizeText(x.get_fed_data(), indent=indent), (" " * indent))
        return  doxytext
        
    def getAnchorName(self):
        anchorname = self.parent.name.lower() + self.name.lower()
        if self.parent.name == self.name:
            anchorname = self.name.lower()
            
        return anchorname
    
    def asString(self):
        retval = "method: " + self.name
        retval += "\n\nprototypes: "
        for proto in self.prototypes:
            retval += "\t%s" % `proto`
        retval += "\n\nparams: "
        for param in self.params:
            retval += "%s: %s" % (param, self.params[param])
            
        retval += "\n\ndescription: \n" + self.description
        
        retval += "remarks: \n" + self.remarks
        
        return retval
