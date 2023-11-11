package main

import "fmt"

func main() {
  var i int = 20
  var f float64 = float64(i)
  fmt.Println("int and values:", i, f)

  const value = 21
  var i2 int = value
  var f2 float64 = value
  fmt.Println("I can use my const as either an int or float", i2, f2)

  var b byte = 255
  var smallI int32 = 2_147_483_647
  var bigI uint64 = 18_446_744_073_709_551_615
  b += 1
  smallI += 1
  bigI += 1
  fmt.Println("What happens when I go big?", b, smallI, bigI)
}
