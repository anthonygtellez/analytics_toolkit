# analytics_toolkit
Splunk BA &amp; IoT Toolkit, Cool stuff we've built.


## Macros
### Linear Trendline

```
sourcetype=my_data | timechart count as yvalue | `lineartrend(_time,yvalue)` | timechart sum(yvalue) sum(newY)
```

Plotting R2

```
sourcetype=my_data | timechart count as yvalue | `lineartrend(_time,yvalue)` | stats first(R2)
```
More info: https://wiki.splunk.com/Community:Plotting_a_linear_trendline

### forecast5w

Arguments: $1: Value to predict, $2: confidence interval, $3: relative time, $4: Number of days into the future to predict.

```
sourcetype=my_data | timechart span=10m avg(count) as avg_count | `forecast5w(avg_count,90.0,+1d,3)`
```

### Producer Consumer Ratio

Arguments: $1: inbound traffic field, $2: outbound traffic field

```
sourcetype=my_data | `pcr(bytes_in,bytes_out)`
```
