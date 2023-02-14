use crate::List::{Cons, Nil};
use crate::List2::{Cons2, Nil2};
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

    let c = CustomSmartPointer {
        data: String::from("my stuff"),
    };
    let d = CustomSmartPointer {
        data: String::from("other stuff"),
    };
    drop(c);
    println!("CustomSmartPointers created.");

    let a = Rc::new(Cons2(5, Rc::new(Cons2(10, Rc::new(Nil2)))));
    let b = Cons2(3, Rc::clone(&a));
    let c = Cons2(4, Rc::clone(&a));
    println!("how many A's do we have? {}", Rc::strong_count(&a) );
}

enum List2 {
    Cons2(i32, Rc<List2>),
    Nil2,
}

use std::rc::Rc;


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

struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!(
            "Dropping CustomSmartPointer with data `{}`!",
            self.data
        )
    }
}