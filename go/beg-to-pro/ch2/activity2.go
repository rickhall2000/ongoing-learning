package main

import (
	"fmt"
	"strconv"
)

func main() {
	for i := 1; i <= 100; i++ {
		var value string

		switch {
		case i%15 == 0:
			value = "FizzBuzz"
		case i%3 == 0:
			value = "Fizz"
		case i%5 == 0:
			value = "Buzz"
		default:
			value = strconv.Itoa(i)
		}

		fmt.Println(value)
	}

}
