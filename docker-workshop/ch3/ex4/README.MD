Note on this example:
Static linking didn't work on my mac (also I didn't have g++ so I used gcc)

### Without static linking
When I compiled with 
```
gcc -o test test.c
```
running in a scratch container didn't work, because it didn't have the libraries it needed.

### Static linking on mac
When I tried to compile with
```
gcc -static -o test test.c
```
I got an error
```
 ld: library not found for -lcrt0.o
```

It turns out macOS is designed around dynamic linking

### Building the program in a container
I ran an ubuntu container and then I ran
```
sudo apt-get update
sudo apt-get install libc6-dev
sudo apt-get install musl-tools

musl-gcc -static -o test test.c
```
I used a bound volume to get the source code in, and the executable out.

Then I reran the scratch container with the linked libary.

With the linking, the size of the executable is 33752
Without the linking, the size is only 12556
