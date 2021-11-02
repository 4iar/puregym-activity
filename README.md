### Update: no longer works due to changes in the PureGym website

See discussion [here](https://github.com/4iar/puregym-activity/issues/1) for alternatives

## Installation

Install dependencies for puregym-activity-logger.py
```
$ pip3 install -r requirements.txt
```

Install ggplot2 if using the R analysis script.
```
> install.packages('ggplot2')
```


## Usage

Start recording activity:
```
>> python3 puregym_activity_logger.py [GYM NAME]
```

`[GYM NAME]` is the name of the gym found from the url. For example if your gym is at http://www.puregym.com/gyms/cardiff then run:
```
>> python3 puregym_activity_logger.py cardiff
```


By default, the number of people currently in the gym is scraped and written to `./recorded_data/[GYM NAME].csv` every ten minutes.

The data is scraped from `http//www.puregym.com/gyms/[GYM NAME]/whats-happening`. Some gyms don't seem to have that page, in that case it won't be possible to log gym activity.

## Analysis

Activity for a single gym can be plotted using the R script. Run plot.R and follow the instructions. 
```
> source('plot.R')
```
Plots are saved to the variables p1, p2, and p3. 


An example plot (p3) is shown below.
![](https://raw.githubusercontent.com/4iar/puregym-activity-logger/master/examples/example1.png)













