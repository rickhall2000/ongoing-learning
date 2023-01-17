struct User {
    active: bool,
    username: String, 
    email: String,
    sign_in_count: u64,
}

fn mainly() {
    let user1 = User {
        active: true,
        username: String::from("someusername123"),
        email: String::from("someone@example.com"),
        sign_in_count: 1
    };

    let mut user2 = User {
        active: true,
        username: String::from("someusername123"),
        email: String::from("someone@example.com"),
        sign_in_count: 1
    };

    user2.email = String::from("anotheremail@example.com");

    // note this is a move, so we can't use user1 anymore
    let user3 = User {
        email: String::from("yetanother#example.com"),
        ..user1
    };
}    

fn build_user(email: String, username: String) -> User {
    User {
        active: true,
        username,
        email,
        sign_in_count: 1,
    }
}

struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

// unit struct
struct AlwaysEqual;


fn tuple_struts() {
    let black = Color(0,0,0);
    let origin = Point(0,0,0);
    let subject = AlwaysEqual;
}

fn main_vars() {
    let width1 = 30;
    let height1 = 50;
    println!("The area is {} square somethings",
        area_vars(width1, height1));
}

fn area_vars(width: u32, height: u32) -> u32 {
    width * height
}

fn main_tup() {
    let rect1 = (30, 50);
    println!("The area is really {}", area_tup(rect1));
}

fn area_tup(dimensions: (u32, u32)) -> u32 {
    dimensions.0 * dimensions.1
}

#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main_function() {
    let scale = 2;
    let rect1 = Rectangle {
        width: dbg!(30 * scale),
        height: 50,
    };

    println!("The area is still {}.", area(&rect1));

    println!("rect1 is {:#?}", rect1);
    dbg!(&rect1);
}

fn area(rectangle: &Rectangle) -> u32 {
    rectangle.width * rectangle.height
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
    fn width(&self) -> bool {
        self.width > 0
    }


}

fn main() {
    let rect1 = Rectangle {
        width: 32,
        height: 50,
    };

    if rect1.width(){
        println!(
            "the area is now {}.",
            rect1.area()
        );    
    }

    let rect2 = Rectangle {
        width: 10, 
        height: 40,
    };

    println!("Can rect1 hold rect2? {}", rect1.can_hold(&rect2));
    let rect3 = Rectangle::square(20);

    println!("can rect2 hold rect 3? {}", rect2.can_hold(&rect3));
}

impl Rectangle {
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width >= other.width && self.height >= other.height
    }

    fn square(size: u32) -> Self {
        Self {
            width: size,
            height: size,
        }
    }
}