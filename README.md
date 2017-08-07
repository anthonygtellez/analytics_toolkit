# analytics_toolkit
Splunk BA &amp; IoT Toolkit, Cool stuff we've built.


## Macros
Linear Trendline


```
sourcetype=my_data | timechart count as yvalue | `lineartrend(_time,yvalue)` | timechart sum(yvalue) sum(newY)
```

Plotting R2

```
sourcetype=my_data | timechart count as yvalue | `lineartrend(_time,yvalue)` | stats first(R2)
```
More info: https://wiki.splunk.com/Community:Plotting_a_linear_trendline
