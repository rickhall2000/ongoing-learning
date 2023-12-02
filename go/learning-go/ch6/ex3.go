package main

type Person struct {
  name string
  age int
}

func main() {
//  var people = make( []Person, 0, 10_000_000)
  var people []Person
  for i := 0 ; i < 10_000_000 ; i++ {
    joe := Person{name: "Joe", age: 81}
    people = append(people, joe)
  }
}
