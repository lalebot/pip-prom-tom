#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.parse
import urllib.request
import os
import optparse

url="http://bioinformatics.psb.ugent.be/webtools/plantcare/cgi-bin/CallMat_NN47.htpl"
params={
    'Field_Sequence':'CTAATCTTATGCATTTAGCAGTACAAATTCAAAAATTTCCCATTTTTATTCATGAATCATACCATTATATATTAACTAAATCCAAGGTAAAAAAAAGGTATGAAAGCTCTATAGTAAGTAAAATATAAATTCCCCATAAGGAAAGGGCCAAGTCCACCAGGCAAGTAAAATGAGCAAGCACCACTCCACCATCACACAATTTCACTCATAGATAACGATAAGATTCATGGAATTATCTTCCACGTGGCATTATTCCAGCGGTTCAAGCCGATAAGGGTCTCAACACCTCTCCTTAGGCCTTTGTGGCCGTTACCAAGTAAAATTAACCTCACACATATCCACACTCAAAATCCAACGGTGTAGATCCTAGTCCACTTGAATCTCATGTATCCTAGACCCTCCGATCACTCCAAAGCTTGTTCTCATTGTTGTTATCATTATATATAGATGACCAAAGCACTAGACCAAACCTCAGTCACACAAAGAGTAAAGAAGAACAA',
    'Field_SequenceName':'demo',
    'Field_SequenceDate':'4.27',
    'Mode':'readonly',
    'StartAt':'0',
    'NbRecs':'10',
    'MatInspector':'Search'
    }
data=urllib.parse.urlencode(params)
data = data.encode('utf-8')
# print urllib2.urlopen(url, data).read()
req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as response:
    the_page = response.read()
print(the_page)

# https://docs.python.org/3.4/howto/urllib2.html
