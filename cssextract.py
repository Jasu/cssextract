#!/usr/bin/python

import argparse
import os
import sys

import cssutils
import cssutils.css

### Parse args

cliParser = argparse.ArgumentParser(
  description="CSSExtract - Extract CSS affecting specific properties")

cliParser.add_argument('-f', 
                       '--force', 
                      help="Overwrite without prompting.", 
                      action='store_true')
cliParser.add_argument('-p', 
                       '--property', 
                      help="CSS property to filter",
                      action='append')
cliParser.add_argument('infile', help="Input file names", nargs='+')
cliParser.add_argument('outfile', help="Output file name")

args = cliParser.parse_args()

### Process

outCss = cssutils.css.CSSStyleSheet()

for inFile in args.infile:
  inCss = cssutils.parseFile(inFile)
  for rule in inCss.cssRules.rulesOfType(cssutils.css.CSSRule.STYLE_RULE):
    for prop in rule.style:
      if prop.name not in args.property:
        continue
      targetRule = None
      outRules = outCss.cssRules.rulesOfType(cssutils.css.CSSRule.STYLE_RULE)
      for outRule in outRules:
        if outRule.selectorText == rule.selectorText:
          targetRule = outRule
          break
      if not targetRule:
        targetRule = cssutils.css.CSSStyleRule(rule.selectorText)
        outCss.add(targetRule)
      if prop.priority == 'important':
        targetRule.style[prop.name] = (prop.value, 'important')
      else:
        targetRule.style[prop.name] = prop.value

if os.path.exists(args.outfile) and not args.force:
  print ('File ' + args.outfile + ' already exists.')
  input = input('Overwrite? [y/N]: ')
  if input.strip() != 'y':
    print ('Nothing done.')
    sys.exit(1)

with open(args.outfile, 'wb') as file:
  file.write(outCss.cssText)
