# Link Creator 

### Dependencies
1. Python 3.5+ 

### How to run:
1. fill out variables in the settings.json file
2. add a csv to parse in the input folder `/input`
3. excute script `python main.py` | `./main.py` etc. 

### How it works:

In short we take the value from the `base_url` and append all the values in the csv file.

csv values are defined by their header name (first row of the file)

#### Files

`settings.json` should contain these variables:

```json

{
  "input_folder":"input", // folder where the input file lives (relative path)
  "templates_folder":"templates", //folder where default templates live
  "input_file": "input.csv", // csv file to parse
  "output_file": "output.txt", // where to post outout 
  "csv_deliminator": ",", // what to delimatine csv on 
  "base_url": "" // base url for all links created (if not found in input_file

}
```

`input_file` The file as described variable of `settings.json` 

```csv
base_url,android_passive_deepview,og:imagename,platform
soul.app.link/30?,TRUE,helloworld.png,facebook cross platform
```

**base_url** must be included in either `settings.json` or the `input_file`. 

The value is the settings file will take priority.  


