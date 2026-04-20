# TweeTools
**Some Tools For Twee &amp; Twine**

Play Twee games from the commandline or [web browser](Twish)

Export Twee games to Markdown

Shuffle Twee game passages for book usage

[Export Twee to Canvas](Canvas) format or Canvas format to Twee

## Scripts -

`./tweePlay.pl FILE.twee` - play through a basic Twee choice game from the commandline

`./tweeXport.pl FILE.twee` - export a basic Twee choice game into MarkDown

`./randMark.pl  FILE.twee.md` - shuffle the MarkDown file into random choice numbers (for exporting to PDF)

Export Markdown to PDF etc. using pandoc

`pandoc input.md -o output.pdf`

## Not Yet Implemented -

X `./tweeWebPlay.pl FILE.twee` - play through a basic Twee choice game in a browser

I already sort of implemented in Twish - see below

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

# Twish
**Twee-ish Gamebook Web Rendering**

## Usage -

```
:: Passage Title
Text <b>description</b><br>
[[My Link|Link]]

(set: $animal to "horse")
(if: $animal is "dog")It's a dog!
(if: $animal is "horse")[[$animal]]
```

# Twee-Canvas-Converter
**Converts Twee files to JSON Canvas format or Canvas format to Twee files**

See - https://github.com/obsidianmd/jsoncanvas

## Usage

`./twee_canvas_convert TestCanvas.twee`
or
`./twee_canvas_convert TestCanvas.canvas`

## Resources

* Web Editor - https://hi-canvas.marknoteapp.com/
* Web Editor / Converter - https://flowchart.fun/
* Mermaid convert - https://alexwiench.github.io/json-canvas-to-mermaid-demo/
* Obsidian Usage - https://help.obsidian.md/Plugins/Canvas#:~:text=Obsidian%20stores%20your%20canvas%20data,file%20format%20called%20JSON%20Canvas.
