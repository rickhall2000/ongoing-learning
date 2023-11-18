package main 

import "os"
import "fmt"
import "io"

func fileLen(filename string) (int, error) {
  f, err := os.Open(filename)
  if err != nil {
    return 0, err
  }
  defer f.Close()
  data := make([]byte, 2048)
  totalCount := 0
  for {
    count, err := f.Read(data)
    if err != nil {
      if err != io.EOF {
        return 0, err
      }
      return totalCount, nil
    }
    totalCount += count
  }
}

func main() {
  len1, err := fileLen("ex2.go")
  
  if err != nil {
    fmt.Println("Error: ", err)
  } else {
    fmt.Println("File length", len1)
  }

  len2, err := fileLen("notfound.file")
  if err != nil {
    fmt.Println("Error: ", err)
  } else {
    fmt.Println("File length", len2)
  }
}
