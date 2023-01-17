enum IpAddrKind {
    V4(u8, u8, u8, u8),
    V6(String)
}

fn route (ip_kind: IpAddrKind) {}

let home = IpAddrKind::V4(127.0.0.1);
let loopback = IpAddrKind::V6(String::from("::1"));

enum Message {
    Quit,
    Move { x: i32, y: i32},
    Write(String),
    ChangeColor(i32, i32, i32),
}

impl Message {
    fn call(&self) {
        // method goes ehre
    }
}

let some_number = Some(5);
let absent_number: Option<i32> = None;

let x: i8 = 5
let y Option<i8> = Some(5);

// not allowed
// x + y

enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter(UsState),
}

enum UsState {
    Georgia,
    NewYork,
    Etc,
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => {
            println!("Lucky penny!");
            1
        }
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter(state) => {
            println!("State quarter from {:?}!", state);
            25
        }
    }
}

fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i + 1),
    }
}

let five = Some(5);
let six - plus_one(five);
let none = plus_one(None);

let config_max = Some(3u8):
if let Some(max) = config_max {
    println!("The max is configured to be {max}");
}

let mut count = 0;

if let Coin::Quarter(state) = coin {
    println!("State quarter from {:?}!", state);    
} else {
    count += 1;
}