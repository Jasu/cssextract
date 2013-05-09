CSSExtract
==========

A command-line tool to filter CSS rules affecting specific parameters.

Dependencies
------------
  
  *  **Python 3.3** (older versions might work)
  *  **cssutils** pip install cssutils

Usage
-----

### Example 1 

  cssextract --property background-image input.css output.css

  Output.css contains only the CSS affecting background-image from input.css.

### Example 1 

  cssextract -p background -p background-image input.css output.css

  Output.css contains only the CSS potentially affecting background image 
  (and of course anything that background might affect.)

