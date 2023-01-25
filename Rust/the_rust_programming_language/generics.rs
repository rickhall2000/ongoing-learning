fn main() {
    let number_list = vec![34, 50, 25, 100, 65];

    /* 
    extracting to function
    let mut largest = &number_list[0];

    for number in &number_list {
        if number > largest {
            largest = number;
        }
    }
    */
    let result = largest(&number_list);
    println!("The largest number is {result}");

    let number_list = vec![102, 34, 6000, 89, 53, 2, 43, 8];

    /* 
    extracting to function
    let mut largest = &number_list[0];

    for number in &number_list {
        if number > largest {
            largest = number;
        }
    }
    */

    let result = largest(&number_list);
    println!("The largest number is {result}");


    let char_list = vec!['y', 'm', 'a', 'q'];
    let result = largest(&char_list);
    println!("the largest char is {result}");


    let integer = Point { x: 5, y: 10 };
    let float = Point { x: 1.0, y: 4.0 };

    println!("integer.x = {}", integer.x);
    println!("float is {} from origin", float.distance_from_origin());
}

fn largest<T: std::cmp::PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];

    for number in list {
        if number > largest {
            largest = number;
        }
    }
    largest
}

struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

impl Point<f32> {
    fn distance_from_origin(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}

struct Pont<X1, Y1> {
    x: X1,
    y: Y1
}

impl<X1, Y1> Pont<X1, Y1> {
    fn mixup<X2, Y2>(
        self,
        other: Pont<X2, Y2>,
    ) -> Pont<X1, Y2> {
        Pont {
            x: self.x,
            y: other.y,
        }
    }
}