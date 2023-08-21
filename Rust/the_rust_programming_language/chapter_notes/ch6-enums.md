## Chapter 6 Enums and Pattern Matching

Enums give you a way of saying that a value is one of a possible set of values.

### Simplest form:
```
    enum IpAddrKind {
        V4,
        V6,
    }

    let four = IpAddrKind::V4;
    let six = IpAddrKind::V6;

    fn route(ip_kind: IpAddrKind) {...}
```

### Storing data in enums
```
    enum IpAddr {
        V4(String),
        V6(String),
    }

    let home = IpAddr::V4(String::from("127.0.0.1"));
    let loopback = IpAddr::V6(String::from("::1"));

```
Or a more complicated example
```
    enum Message {
        Quit,
        Move { x: i32, y: i32 },
        Write(String),
        ChangeColor(i32, i32, i32),
    }
```

### Define functions on enums
```
    impl Message {
        fn call(&self) {
            // method body
        }
    }

    let m = Message::Write(String::from("hello"));
    m.call();
```

### Options instead of nulls 
```
// option in the standard library
    enum Option<T> {
        None,
        Some(T),
    }

    let some_number = Some(5);
    let some_char = Some('e');
    let absent_number: Option<i32> = None;
```

### Values in enums are wrapped
The value is wrapped up in the option, so we need to unwrap to use it. This won't work:
```
    let x: i8 = 6;
    let y: Option<i8> = Some(5);
// compiler error no implemention for i8 + Option<i8>
    let sum = x + y;

    fn add_int_to_option(x: i8, y: Option<i8>) -> Option<i8> {
        match y {
            None => None,
            Some(i) => Some(i + x), 
        }
    }

    let sum = add_int_to_option(x, y); // returns Some(11)


```

### Matching to convert values
```
    enum Coin {
        Penny,
        Nickel,
        Dime,
        Quarter,
    }

    fn value_in_cents(coin: Coin) -> u8 {
        match coin {
            Coin::Penny => {
                println!("Lucky penny!");
                1
            }
            Coin::Nickel => 5,
            Coin::Dime => 10,
            Coin::Quarter => 25,
        }
    }
```
### Catch-all patterns
```
    let dice_roll = 9;
    match dice_roll {
        3 => add_fancy_hat(),
        7 => remove_fancy_hat(),
        other => move_player(other),
    }

    fn add_fancy_hat() {}
    fn remove_fancy_hat() {}
    fn move_player(num_spaces: u8) {}

    // if you don't want to use the value, use _, so the last arm would be
    _ => reroll(),
```

### If let for concision
Do something only if a value exists.
```
    let config_max = Some(3u8);
    match config_max {
        Some(max) => println!("The max is configured to be {max}"),
        _ => (),
    }
```
With if let we can be more concise
```
    let config_max = Some(3u8);
    if let Some(max) = config_max {
        println!("The maxiumum is configured to be {max}");
    }
```
We can also have an else clause
```
    let mut count = 0;
// match
    match coin {
        Coin::Quarter(state) => println!("State quarter from {"?}!", state),
        _ => count += 1,
    }
// if-let-else
    if let Coin::Quarter(state) = coin {
        println!("State quarter from {:?}", state);
    } else {
        count += 1;
    }
```
