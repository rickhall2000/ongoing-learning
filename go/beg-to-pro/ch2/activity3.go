package main

import "fmt"

func main() {
	rawNums := []int{1, 7, 3, 4, 2, 5, 1}
	fmt.Println(rawNums)

	for unsorted := true; unsorted; {
		unsorted = false
		for i := 1; i < len(rawNums); i++ {
			if rawNums[i-1] > rawNums[i] {
				rawNums[i], rawNums[i-1] = rawNums[i-1], rawNums[i]
				unsorted = true
			}
		}
	}
	fmt.Println(rawNums)

}
