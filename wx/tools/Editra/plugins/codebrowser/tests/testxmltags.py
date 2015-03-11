###############################################################################
# Name: testxmltags.py
# Purpose: Unittest for xmltag.py
# Author: Rudi Pettazzi <rudi.pettazzi@gmail.com>
# Copyright: (c) 2008 Cody Precord <staff@editra.org>
# License: wxWindows License
###############################################################################

__author__ = "Rudi Pettazzi <rudi.pettazzi@gmail.com>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import unittest
import StringIO
import os
import sys

sys.path.insert(0, os.path.abspath('../codebrowser/gentag'))

import xmltags

#-----------------------------------------------------------------------------#

class TestXmlTags(unittest.TestCase):
    def setUp(self):
        self.buf = []

    def tearDown(self):
        self.buf = []

    def testEmptyDocument(self):
        """Test empty document"""
        txt = ''
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = ""
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testWellFormed1(self):
        """Test eclipse plugin.xml subset"""
        txt = '''<?xml version="1.0" encoding="UTF-8"?>
                 <feature>
                   <description>%description</description>
                   <copyright>%copyright</copyright>
                   <license url="%licenseURL">%license</license>
                </feature>
                '''
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = "(feature(description)(copyright)(license))"
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testWellFormed2(self):
        """Test well formed doc with cdata"""
        txt = '''<?xml version="1.0"?>
                 <!DOCTYPE whatever SYSTEM "whatever.dtd">
                 <root>
                  <code id="aaaa"><![CDATA[
                    function foobar(a, b) {
                        return a > b;
                    }
                ]]></code>
                </root>'''
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = "(root(code))"
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testWellFormed3(self):
        """Test well formed wsdl document """
        txt = '''<?xml version="1.0" encoding="UTF-8"?>
        <wsdl:definitions targetNamespace="urn:ec.europa.eu:taxud:vies:services:checkVat"
            xmlns="http://schemas.xmlsoap.org/wsdl/"
            xmlns:apachesoap="http://xml.apache.org/xml-soap"
            xmlns:impl="urn:ec.europa.eu:taxud:vies:services:checkVat"
            xmlns:intf="urn:ec.europa.eu:taxud:vies:services:checkVat"
            xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/"
            xmlns:tns1="urn:ec.europa.eu:taxud:vies:services:checkVat:types"
            xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
            xmlns:wsdlsoap="http://schemas.xmlsoap.org/wsdl/soap/"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema">
            <documentation>omissis ... </documentation>
            <wsdl:types>
                <schema targetNamespace="urn:ec.europa.eu:taxud:vies:services:checkVat:types"
                        xmlns="http://www.w3.org/2001/XMLSchema">
                    <element name="checkVat">
                        <complexType>
                            <sequence>
                                <element name="dummyreq" type="xsd:string"/>
                            </sequence>
                        </complexType>
                    </element>
                </schema>
            </wsdl:types>
            <wsdl:message name="checkVatRequest">
                <wsdl:part element="tns1:checkVat" name="parameters"/>
            </wsdl:message>
            <wsdl:portType name="checkVatPortType">
                <wsdl:operation name="checkVat">
                    <wsdl:input message="impl:checkVatRequest" name="checkVatRequest"/>
                    <wsdl:output message="impl:checkVatResponse" name="checkVatResponse"/>
                </wsdl:operation>
            </wsdl:portType>
            <wsdl:binding name="checkVatPortSoapBinding" type="impl:checkVatPortType">
                <wsdlsoap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
                <wsdl:operation name="checkVat">
                    <wsdlsoap:operation soapAction=""/>
                    <wsdl:input name="checkVatRequest">
                        <wsdlsoap:body use="literal"/>
                    </wsdl:input>
                </wsdl:operation>
            </wsdl:binding>
            <wsdl:service name="checkVatService">
                <wsdl:port binding="impl:checkVatPortSoapBinding" name="checkVatPort">
                    <wsdlsoap:address location="http://ec.europa.eu/taxation_customs/vies/api/checkVatPort"/>
                </wsdl:port>
            </wsdl:service>
        </wsdl:definitions>
        '''
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))

        s1 = "(wsdl:definitions" \
             "(documentation)" \
             "(wsdl:types(schema(element(complexType(sequence(element))))))" \
             "(wsdl:message(wsdl:part))" \
             "(wsdl:portType(wsdl:operation(wsdl:input)(wsdl:output)))" \
             "(wsdl:binding(wsdlsoap:binding)(wsdl:operation(wsdlsoap:operation)(wsdl:input(wsdlsoap:body))))" \
             "(wsdl:service(wsdl:port(wsdlsoap:address)))" \
             ")"
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testWellFormed4(self):
        """Test web.xml subset"""
        txt = '''<?xml version="1.0" encoding="UTF-8"?>
                <web-app id="wa" version="2.4"
                    xmlns="http://java.sun.com/xml/ns/j2ee"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="http://java.sun.com/xml/ns/j2ee http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd">
                <filter>
                    <filter-name>struts</filter-name>
                    <filter-class>org.apache.struts2.dispatcher.FilterDispatcher</filter-class>
                    <init-param>
                        <param-name>actionPackages</param-name>
                        <param-value>com.zzz.yyy.kkk</param-value>
                    </init-param>
                </filter>
                <filter-mapping>
                    <filter-name>struts</filter-name>
                    <url-pattern>/*</url-pattern>
                </filter-mapping>
                </web-app>
                '''
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = "(web-app(filter(filter-name)(filter-class)(init-param" \
             "(param-name)(param-value)))(filter-mapping(filter-name)(url-pattern)))"
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testWellFormed5(self):
        """Test shortest tag names"""
        txt = '<a><b><c></c></b></a>'
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = '(a(b(c)))'
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testWellFormed6(self):
        """Test xslt document"""
        txt = '''<?xml version="1.0"?>
                 <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                     version="1.0">
                 <xsl:template match="/"> <!-- a comment -->
                 <aaa>
                   <bbb><xsl:apply-templates mode="bbb"/></bbb>
                 </aaa>
                 </xsl:template>
                 <xsl:template match="processing-instruction('newline')">
                     ...
                 </xsl:template>
                 </xsl:stylesheet>'''
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = '(xsl:stylesheet(xsl:template(aaa(bbb(xsl:apply-templates))))(xsl:template))'
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testWellMalformed7(self):
        """Test big document"""
        txt = '<root>' + '<aaaa>bbbb</aaaa>' * 3000 + '</root>'
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = '(root' + '(aaaa)' * 3000 + ')'
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testMalformed1(self):
        """Test malformed/partial document. Empty result"""
        txt = '''<?xml'''
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = ""
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testMalformed2(self):
        """Test malformed document with malformed tags. The tokenizer
        detects only the root tag"""
        txt = '''<?xml version="1.0"?>
                <web-app id="wa" version="2.4"
                <filter'''
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = "(web-app)"
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testMalformed3(self):
        """Test malformed document with malformed tags. The tokenizer
        detects only the root tag"""
        txt = '''<?xml version="1.0"?>
                <web-app
                <filter><'''
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = "(web-app)"
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testMalformed4(self):
        """Test malformed document with malformed tags. The tokenizer
        detects only the root tag"""
        txt = '''<?xml version="1.0" encoding=
                <web-app  a =
                <filter>'''
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = "(web-app)"
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testMalformed6(self):
        """Test malformed document: empty closing tag"""
        txt = ' />'
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = ''
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testMalformed7(self):
        """Test malformed document: empty closing tag"""
        txt = ' >'
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = ''
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testMalformed8(self):
        """Test malformed document: empty open tag"""
        txt = ' <'
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = ''
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    # repair strategies test

    def testMalformed9(self):
        """1st repair strategy fails, 2nd strategy succeeds: orphan end tag is interpreted as
        an empty-element tag."""
        txt = '<html></script><body></body></html>'
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = '(html(script)(body))'
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testMalformed10(self):
        """1st repair strategy succeeds: </html> tag is not
        matched because on the top of the stack an unclosed <script> tag
        is found. Just below this tag, the stack contains the <html> matching tag
        so <script> is popped of with all his (probably wrong) children and reparented to
        the now closed <html>.
        """
        txt = '<html><script><body><p>ssss</p></body></html>'
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = '(html(script(body(p))))'
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testMalformed11(self):
        """1st repair strategy succeeds: found </html> start tag deep into the stack"""
        txt = '<html><script><body><p></html>'
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = '(html(script(body(p))))'
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testMalformed12(self):
        """1st repair strategy succeeds"""
        txt = '<root><child><alfa><beta></beta><gamma><delta><lambda>aaaa</lambda></child></root>'
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = '(root(child(alfa(beta)(gamma(delta(lambda))))))'
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testMalformed13(self):
        """2nd repair strategy: cascade of end tag treated as empty-element tags"""
        txt = '</root></child></alfa></beta></gamma></delta></lambda>'
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = '(root(child)(alfa)(beta)(gamma)(delta)(lambda))'
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testMalformed14(self):
        """3rd repair strategy: cascade of start tag left on the stack implicitly closed
        and treated as a hierarchy of tags. The bottom of the stack is the root.
        """
        txt = '<root><child><alfa><beta><gamma><delta><lambda>'
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = '(root(child(alfa(beta(gamma(delta(lambda)))))))'
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testMalformed15(self):
        """3rd repair strategy"""
        txt = '<root><child><alfa></alfa>'
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = '(root(child(alfa)))'
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def testNoRoot(self):
        """Test document with no root (3rd repair strategy handle this)"""
        txt = '<a></a><b></b><c></c>'
        tags = xmltags.GenerateTags(StringIO.StringIO(txt))
        s1 = '(a(b)(c))'
        self._tree2str(tags)
        s2 = ''.join(self.buf)
        self.assertEquals(s1, s2)
        s2 = None

    def _tree2str(self, node):
        """flatten the tree rooted at node into a parenthesized expression"""
        for elt in node.GetElements():
            for elt in elt[xmltags.XmlTagsBuilder.TAG_ID]:
                self.buf.append('(')
                if elt != None:
                    self.buf.append(elt.name)
                    self._tree2str(elt)
                self.buf.append(')')

if __name__ == '__main__':
    unittest.main()
