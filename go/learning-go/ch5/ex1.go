package main

import "errors"
import "fmt"
import "strconv"

// modify calculator example to check for div by 0

var (
  add = func(i int, j int) (int, error) { 
    return i + j, nil 
  }
  sub = func(i int, j int) (int, error) { return i - j, nil }
  mul = func(i int, j int) (int, error) { return i * j, nil }
  div = func(i int, j int) (int, error)  {
    if j == 0 {
      return 0, errors.New("Div by 0 error") 
    }
    return i / j, nil }
)

var opMap = map[string]func(int, int) (int, error){
  "+": add,
  "-": sub,
  "*": mul,
  "/": div,
}

func main() {
  expressions := [][]string{
    {"2", "+", "2"},
    {"12", "/", "0"},
  }

  for _, expression := range expressions {

    if len(expression) != 3 {
      fmt.Println("Invalid expression")
      break
    }

    p1,err  := strconv.Atoi(expression[0])
    if err != nil {
      fmt.Println("Error parsing the first value")
      break
    }
    
    op := expression[1] 
    opFunc, ok := opMap[op]
    if !ok {
      fmt.Println("The operator was not found")
      break
    }

    p2, err := strconv.Atoi(expression[2])
    if err != nil {
      fmt.Println("Error parsing the second value")
      break
    }

    result, err := opFunc(p1, p2)
    if err != nil {
      fmt.Println("Math error: ", err)
      break
    }

    fmt.Println(expression, " = ", result)
  }


}

