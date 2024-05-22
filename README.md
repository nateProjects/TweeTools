# TweeTools
Some Tools For Twee &amp; Twine

I needed a simple page randomiser for a choice-based narrative game and got carried away.

## Scripts -

`./tweePlay.pl FILE.twee` - play through a basic Twee choice game from the commandline

`./tweeXport.pl FILE.twee` - export a basic Twee choice game into MarkDown

`./randMark.pl  FILE.twee.md` - shuffle the MarkDown file into random choice numbers (for exporting to PDF)

Export Markdown to PDF etc. using pandoc

`pandoc input.md -o output.pdf`

## Not Yet Implemented -

X `./tweeWebPlay.pl FILE.twee` - play through a basic Twee choice game in a browser

I already sort of implemented in https://github.com/nateProjects/twish

X `./tweeImport.pl FILE.md` - import a basic MarkDown file into a Twee choice game

## Twee formatting

```
:: Start works
:: Passage Name works
Followed by a description
[Links work]
[Link text|works]
[So does->this]
[This<-doesnt] # Does anyone use this?
```

Note: for Twee includes you could just `cat *.twee > combined.twee`

## Why PERL?

Because it is pre-installed on MacoS, Linux, and te default Windows WSL.
