package main

import "fmt"

func main() {
  // first exercise
  greetings := []string{"Hello", "Hola", "नमस्कार", "こんにちは", "Привіт"}
  fmt.Println(greetings)
  first := greetings[:2]
  fmt.Println(first)
  second := greetings[1:4]
  fmt.Println(second)
  third := greetings[3:]
  fmt.Println(third)

  // second exercise
  // I cant paste the emojis in either vi or vs code, so using chars instead
  message := "Hi こ and ん "
  var asRunes []rune = []rune(message)
  oneRune := asRunes[3]
  fmt.Println(oneRune)

  // third exercise
  type Employee struct {
    firstName string
    lastName string
    id int
  }
  one := Employee {
    "joe",
    "smith",
    1,
  }

  two := Employee {
    firstName: "bob",
    lastName: "test",
    id: 3,
  }

  var three Employee
  three.firstName = "Mr"
  three.lastName = "T"
  three.id = 27

  fmt.Println(one)
  fmt.Println(two)
  fmt.Println(three)

}
