# Ownership
## Ownership rules
- each value has an owner
- there can only be 1 owner at a time
- when the owner goes out of scope, the value will be dropped

## Variables and Data interacting with Move
Simple values make a copy
```
   let x = 5;
   let y = x; 
   // this is a copy both x and y own their values
```
Items on the heap do a move 
```
    let s1 = String::from("hello");
    let s2 = s1;
    // this is a move, s2 now owns the data
    // when s2 goes out of scope, the memory will be released
    println!("{s1}, world!"); 
    // error, borrow of moved value `s1`
```
To make a copy use clone
```
    let s1 = String::from("hello");
    let s2 = s1.clone();
    println!("s1 = {s1}, s2 = {s2}");
```
If you create a type that you want copied by default you can add the `Copy` trait.
You can only add the `Copy` trait to items that doesn't have any components that have the `Drop` trait.
Tuples implement `Copy` if they don't contain items that don't (eg, String).

## Ownership and functions
When an object is passed in to a function, that function takes ownership. Passing by reference allows borrowing instead of moving.
```
    fn main() {
        let s1 = String::from("hello");
        let len = calculate_length(&s1);
        println!("The length of '{s1}' is {len}.");
    }

    fn calculate_length(s: &String) -> usize {
        s.len()
    }
```

Returning a reference to something that goes out of scope would create a dangling pointer
```
    fn main() {
        let reference_to_nothing = dangle();
    }

    fn dangle() -> &String {
        let s = String::from("Hello");
        &s
    }
    // error missing lifetime specifier
```

## Slices
You can store portions of arrays and strings as slices, which are immutale references.
```
    let s = String::from("hello");
    let slice = &s[0..2];
    // string literals are themselves slices

    let a = [1,2,3,4,5];
    let slice = &a[1..3];
    assert_eq!(slice, &[2,3]);
```
