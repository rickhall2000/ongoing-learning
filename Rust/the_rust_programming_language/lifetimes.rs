fn main() {
    let string1 = String::from("abcd");
    let result;
    {
        let string2 = String::from("xyz");

        result = longest(string1.as_str(), string2.as_str());
        println!("The longest string is {result}");
    }
// string2 does not live long enough
//    println!("The longest string is {result}");

    let novel = String::from(
        "Call me Ishmael. Some years ago..."
    );
    let first_sentence = novel
        .split('.')
        .next()
        .expect("Could not find a '.'");
    
    let i = ImportantExcerpt {
        part: first_sentence,
    };

}

fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

struct ImportantExcerpt<'a> {
    part: &'a str,
}

