# Extended Plain String Object Notation

## Usage

### Convert from JSON file

```
$ python -m epson.json2epson <json_file >epson_file
```

### Convert to JSON file

```
$ python -m epson.epson2json <epson_file >json_file
```

## Notation Example

### JSON multi-line string

```
{
    "How to Use It": "The human whose name is written in this note shall die.\n\nThis note will not take effect unless the writer has the person's face in their mind when writing his/her name.\nTherefore, people sharing the same name will not be affected.\n\nIf the cause of death is written within the next 40 seconds of writing the person's name, it will happen.\n\nIf the cause of death is not specified, the person will simply die of a heart attack.\n\nAfter writing the cause of death, details of the death should be written in the next 6 minutes and 40 seconds.\n"
}
```

### EPSON multi-line string

Like a shell-script's here-document...

```
{
    "How to Use It": "".
The human whose name is written in this note shall die.

This note will not take effect unless the writer has the person's face in their mind when writing his/her name.
Therefore, people sharing the same name will not be affected.

If the cause of death is written within the next 40 seconds of writing the person's name, it will happen.

If the cause of death is not specified, the person will simply die of a heart attack.

After writing the cause of death, details of the death should be written in the next 6 minutes and 40 seconds.

.
}
```

In above example, period character (.) is guard-string.

And if you carefully choose guard-string, you will put raw-binary data as string.

## Syntax

* any [JSON Syntax](https://www.json.org/)
* multi-line-string
    * '"' '"' guard-string '\n' raw-string '\n' guard-string '\n'
        * former guard-sting and later one MUST be same sequence of characters
        * line-feed characters (\n) around raw-string are exclusive of raw-string self
* guard-string
    * characters
* raw-string
    * raw-characters
* raw-characters
    * raw-character raw-characters
* raw-character
    * character
    * ws
