package main

import "fmt"

func add5Value(count int) {
	count += 5
	fmt.Println("Add5Value ", count)
}

func add5Point(count *int) {
	*count += 5
	fmt.Println("Add5Point ", *count)
}

func main() {
	var count int
	add5Value(count)
	fmt.Println("Add5Value post", count)
	add5Point(&count)
	fmt.Println("Add5Point post", count)
}
