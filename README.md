# Text Replacer
User friendly tool to replace certain text patterns in your project folders / files

Replaces regular text or text pattern (regex) of your project.<br/>
You can input as many patterns / words / phrases / letters to change as you wish<br/>
Replacements have to be specified in a .json file, the format should be:<br/>
        { "[Regex pattern to replace]" : "New Text",<br/>
          "Text to replace" : "New Text 2"<br/>
        }

Requires at least one argument: source folder/file path (absolute or relative)<br/>
As second argument, you can specify another path for replacement .json file, the default value is replaceDict.json

Be careful, there will be no confirmation message and changes cannot be undone
