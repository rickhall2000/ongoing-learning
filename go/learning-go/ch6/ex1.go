package main

import "fmt"

type Person struct { 
  FirstName string
  LastName string
  Age int
}

func MakePerson(firstName, lastName string, age int) Person {
  return Person{FirstName: firstName, LastName: lastName, Age: age}
}

func MakePersonPointer(firstName string, lastName string, age int)  *Person {
  return &Person{FirstName: firstName, LastName: lastName, Age: age}
}

func main() {
  p1 := MakePerson("Joe", "Smith", 12)
  p2 := MakePersonPointer("Tom", "Jones", 17)
  fmt.Println(p1, p2)
}
