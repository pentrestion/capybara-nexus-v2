package main

import (
	"fmt"
	"sync"
)

/**
 * A classic data race condition in a concurrent map.
 * Static analyzers find simple races, but this one is "hidden"
 * inside a conditional logic gate that only triggers under high load.
 */
func main() {
	var wg sync.WaitGroup
	data := make(map[string]int)
	
	// Two concurrent goroutines accessing the same map without a Mutex.
	// This only crashes the Go runtime under specific race conditions.
	wg.Add(2)

	go func() {
		defer wg.Done()
		for i := 0; i < 1000; i++ {
			data["key"] = i // Write
		}
	}()

	go func() {
		defer wg.Done()
		for i := 0; i < 1000; i++ {
			_ = data["key"] // Read
		}
	}()

	wg.Wait()
	fmt.Println("Final value:", data["key"])
}
