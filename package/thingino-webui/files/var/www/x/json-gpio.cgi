#!/bin/sh
. ./_json.sh

[ -n "$QUERY_STRING" ] && eval $(echo "$QUERY_STRING" | sed "s/&/;/g")

state=${s:-0}

[ -z "$n" ] && json_error "Required parameter 'n' is not set"

pin=$(fw_printenv -n $n)
[ -z "$pin" ] && json_error "GPIO is not found"

# default to output high
[ "$pin" = "${pin//[^0-9]/}" ] && pin="${pin}O"
case "${pin:0-1}" in
	o) pin_on=0; pin_off=1 ;;
	O) pin_on=1; pin_off=0 ;;
esac
pin=${pin:0:(-1)}

gpio set "$pin" "$state"
pin_status=$(cat /sys/class/gpio/gpio$pin/value)

json_ok "{\"pin\":\"$pin\",\"status\":\"$pin_status\"}"