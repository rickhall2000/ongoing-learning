package main

import "fmt"

const GlobalLimit = 100
const MaxCacheSize = 10 * GlobalLimit

const (
	CacheKeyBook = "book_"
	CacheKeyCD   = "cd_"
)

var cache map[string]string

func cacheGet(key string) string {
	return cache[key]
}

func cacheSet(key, val string) {
	if len(cache)+1 >= MaxCacheSize {
		return
	}
	cache[key] = val
}

func GetBook(isbn string) string {
	return cacheGet(CacheKeyBook + isbn)
}

func SetBook(isbn string, name string) {
	cacheSet(CacheKeyBook+isbn, name)
}

func main() {
	cache = make(map[string]string)
	SetBook("1234-5678", "Get Ready To Go")
	fmt.Println("Book :", GetBook("1234-5678"))
}
