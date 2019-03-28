# Link Creator 

### Dependencies
1. Python 3.5+ 

### How to run:
1. fill out variables in the settings.json file
2. add a csv to parse in the input folder `/input`
3. excute script `python main.py` | `./main.py` etc. 

### How it works:

In short we take the value from the `base_url` and append all the values in the csv file. Templated data can also be
appended by using the `template_name` field

csv values are defined by their header name (first row of the file)

#### Files

`settings.json` should contain these variables:

```javascript

{
  "input_folder":"input", // folder where the input file lives (relative path)
  "templates_folder":"templates", //folder where default templates live
  "input_file": "input.csv", // csv file to parse
  "output_file": "output.txt", // where to post output 
  "csv_deliminator": ",", // what to delimatine csv on 
  "base_url": "" // base url for all links created (if not found in input_file)

}
```

`input_file` The file as described variable of `settings.json` 

```csv
base_url,android_passive_deepview,og:imagename,platform,~campaign
company.app.link/30?,TRUE,helloworld.png,facebook cross platform,test_campaign
```

**base_url** and **~campaign** must be included in either `settings.json` or the `input_file`. 
**template_name** is optional. It should be included in either `input_file` as a column header. The current values are the name 
of the files in templates. the template name column can be null. Below are examples of valid csv files:

Example of csv with template filled out along with all required params:
```csv

base_url,template_name,~campaign
company.app.link,facebook_app_only,Facebook
```

Example of csv with optional `template_name` intentionally left blank
```csv

base_url,template_name,og:name,~campaign
company.app.link,,testing_links,myspace
```

current valid template names 
```
1. facebook_app_only
2. facebook_cross_platform
3. google_cross_platform
```


**The value in the settings file and `input_file` will take priority over template values**


### Examples


input
```csv
base_url,android_passive_deepview,og:imagename,platofrm,~campaign,template_name
company.app.link/3p?,TRUE,helloworld.png,facebook cross plat,{campgaignname},
```
output (located in output/output.csv)
```csv
soul.app.link/30?base_url=company.app.link%2F3p%3F&android_passive_deepview=TRUE&og:imagename=helloworld.png&platofrm=facebook+cross+plat&campaign={campgaignname}
```
