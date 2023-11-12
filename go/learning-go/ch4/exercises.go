package main

import "fmt"
import "math/rand"

func main() {
  // exercise 1 for loop that puts 100 random numbers between 0 and 100 in an int slice
  var mySlice []int = make([]int, 100)
  for i := 0; i < 100; i++ {
    mySlice[i] = rand.Intn(100)
  }
  fmt.Println(mySlice);

  // exercise 2, fizz buzz by another name
  for _, v := range mySlice {
    if v % 2 == 0 && v % 3 == 0 {
      fmt.Println("Six")
      continue
    }
    
    if v % 2 == 0 {
      fmt.Println("Two")
      continue
    }

    if v % 3 == 0 {
      fmt.Println("Three")
      continue
    }

    fmt.Println("Nevermind")

  }

  // exericse 3
  var total int = 0

  for i := 0 ; i < 10; i++ {
    total := total + i
    fmt.Println(total)
  }

  for i := 0; i < 10; i++ {
    total = total + i
    fmt.Println(total)
  }


}
