package main

import (
	"fmt"
	"time"
)

func getConfig() (bool, string, time.Time) {
	return false, "info", time.Now()
}

func main() {
	debug, logLevel, startUpTime := getConfig()
	fmt.Println(debug, logLevel, startUpTime)
}
