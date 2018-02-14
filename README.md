# analytics_toolkit
Toolkit for Machine Learning & Analytics Use Cases.

## What is it?
This is a Splunk App which has macros, algos, lookups and searches which can be leveraged for Data Science using Splunk. The various Knowledge Objects can be used for feature engineering or combined with each other to solve various use cases in information security, business analytics, it operations, fraud, etc.


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

### error_rate
Arguments: $1: count of success, $2: count of failure

```
sourcetype=my_data | `error_rate(success,failure)`
```

### success_rate
Arguments: $1: count of success, $2: count of failure

```
sourcetype=my_data | `error_rate(success,failure)`
```

### http_error
Arguments: $1: http status_code field

```
sourcetype=my_data | `http_error(status_code)`
```

### pearsoncoorelationcoe
Pearson correlation coefficient for single pair of fields Arguments: $1: x $2: y

```
sourcetype=my_data | `pearsoncoorelationcoe(x,y)`
```

## Lookup Macros

### subnet_to_cidr
Arguments: $1: subnet mask field (eg: 255.255.255.0), $2: network for subnet/vlan (eg:10.1.1.0)

```
sourcetype=my_data | `subnet_to_cidr(subnet_mask,network)`
```

### port2service
Arguments: $1: numerical list of dest_ports (eg: 22, 23, 443)

```
sourcetype=my_data | `port2service(dest_port)`
```

### adversaries
Arguments: $1: input of country data (eg: "United States", "Russian Federation" | "USA","RUS" | "US", "RU"), $2: type of country data in input (eg: country | iso3 | iso2 )

```
sourcetype=my_data | `adversaries(country_list,iso3)`
```

### cdn
Arguments: $1: parsed domain (eg:amazon.com, google.com)

```
sourcetype=my_data | `cdn(domain)`
```

### ddns
Arguments: $1: parsed domain (eg:amazon.com, google.com)

```
sourcetype=my_data | `ddns(domain)`
```

### insecure_ciphers
Arguments: $1: cipher identified by IPS/IDS (eg: TLS_ECDH_RSA_WITH_RC4_128_SHA)

```
sourcetype=my_data | `insecure_ciphers(cipher)`
```

## Algos
