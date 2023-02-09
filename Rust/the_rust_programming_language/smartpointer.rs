use crate::List::{Cons, Nil};
use std::ops::Deref;

fn main() {
    box_example();
    
    let list = Cons(
        1,
        Box::new(Cons(
            2,
            Box::new(Cons(
                3,
                Box::new(Nil)
            ))
        ))
    );

    deref_example();
    deref_coercion();
}

fn box_example() {
    let b = Box::new(5);
    println!("b = {b}");
}

enum List {
    Cons(i32, Box<List>),
    Nil,
}

fn deref_example () {
    let x = 5;
    let y = Box::new(x);

    assert_eq!(5, x);
    assert_eq!(5, *y);

    let z = MyBox::new(x);

    assert_eq!(5, x);
    assert_eq!(5, *z);
}

struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn hello(name: &str) {
    println!("Hello {name}!")
}

fn deref_coercion() {
    let m = MyBox::new(String::from("Rust"));
    hello(&m);
}