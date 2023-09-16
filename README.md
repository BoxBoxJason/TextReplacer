# Text Replacer
User friendly tool to replace certain text patterns in your project folders / files

### Replaces regular text or text pattern (regex) of your project.<br/>
The algorithm searches *recursively* through all children it has access to below the source folder path.<br/>
You can input as many patterns / words / phrases / letters to change as you wish<br/>
Replacements have to be specified in a .json file, the format should be:<br/>
```
{
        "[Regex pattern to replace]" : "New Text",
        "Text to replace" : "New Text 2"
}
```

### Running the program
**Requires** at least one argument: *source folder/file path* (absolute or relative)<br/>
As second argument, you can specify another path for replacement .json file, the default value is *replaceDict.json*

### Attention
It will replace text in every file within the source folder and below.<br/>
The files must be encoded in utf-8, otherwise they will not be opened.<br/>
**Be careful, there will be no confirmation message and changes cannot be undone**
