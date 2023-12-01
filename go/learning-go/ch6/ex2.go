package main

import "fmt"

func UpdateSlice(target []string, newVal string) {
  lastIndex := len(target) - 1
  target[lastIndex] = newVal
  fmt.Println(target)
}

func GrowSlice(target []string, newVal string) {
  target = append(target, newVal)
  fmt.Println(target)
}

func main() {
  
  sliceOne := []string {"This", "is", "Sparta"}

  fmt.Println(sliceOne)
  UpdateSlice(sliceOne, "something")
  fmt.Println(sliceOne)

  sliceTwo := []string {"Pineapple", "on", "pizza?"}
  fmt.Println(sliceTwo)
  GrowSlice(sliceTwo, "NEVER")
  fmt.Println(sliceTwo)
}
