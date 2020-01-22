## Usage:
### FLAGS:
* python main.py --i [ints] --s [floats] --t [thresholds] [--silent]
               [--e] [-dataset DATASET] [-correct CORRECT] [--haskey]
* --i [ints]: required, iterations, can be a list, ints
* --s [floats]: required, sample ratio, can be a list, the sample size will be # records * ratio, floats
* --t [thresholds]: required, thresholds for accepting constraints, ranging from 0 to 1, floats
* --e: optional, default: false, if add the flag, set evaluting the output constraints to be true
* --silent: optional, default: false, if add the flag, all output in cmd line will be muted and saved to file
* -dataset [datafile]: optional, default: 'inputDatabase.csv' (the hospital data), input dataset
* -correct [datafile]: optional, default: 'hospital_correct.csv', ground truth
* --haskey: optional, default: false, if add the flag, it will load key from json file
* --dc: out put in the form of denial constraints [TO BE IMPLEMENTED]

### PARAMETER CAN BE CHANGED IN MAIN.PY
* ID: differentiate each run
* read_loc: where to find data, default:"../datasets/"
* write_loc: where to write data, default:"./output"

### SUPPORT SINGLE AND BATCH RUN
* if all iterations, sample_ratio, thershold only have one number, it will run in this setting
* if any has more than one, it will run in the setting of all the combinations
* e.g. --s 0.3 -0.5 --t 0.8 0.9 --i 5 10
* it will run settings for 
  * s = 0.3 t = 0.8 i = 5
  * s = 0.3 t = 0.8 i = 10
  * ...
  * s = 0.5 t = 0.9 i = 10
 
## EVALUATION
column name: ID, InputDataName, NumberOfTuples, SampleRatio, Iteration, Threshold, 
            TimeUsage, NumberOfFD, TP, TN, FP, FN, Precision, Recall
