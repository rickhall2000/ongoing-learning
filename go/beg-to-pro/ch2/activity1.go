package main

import "fmt"

func main() {
	roll := map[string]int{
		"Gonna": 3,
		"You":   3,
		"Give":  2,
		"Never": 1,
		"Up":    4,
	}

	for word, value := range roll {
		fmt.Println(word, " count = ", value)
	}
}
