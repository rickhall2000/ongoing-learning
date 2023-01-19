fn main() {
    let v1: Vec<i32> = Vec::new();

    let v1 = vec![1, 2, 3];

    let mut v = Vec::new();

    v.push(5);
    v.push(5);
    v.push(7);
    v.push(8);

    let v = vec![1, 2, 3, 4, 5];
    let third: &i32 = &v[2];
    println!("The third element is {third}");

    let third: Option<&i32> = v.get(2);
    match third {
        Some(third) => println!("The third element is still {third}"),
        None => println!("there is no spoon"),
    }
    // DON'T PANIC let no_bueno = &v[100];
    let less_bad = v.get(100);

    loopy();

    let row = vec![
        SpreadsheetCell::Int(3),
        SpreadsheetCell::Text(String::from("blue")),
        SpreadsheetCell::Float(10.12),
    ];

    // trings
    let mut s = String::new();

    let data = "initial comments";
    let s = data.to_string();

    let s = "initial contents".to_string();

    let s = String::from("initial contents");

    mult_refs_and_strings();
    hash_maps();
}

enum SpreadsheetCell {
    Int(i32),
    Float(f64),
    Text(String),
}

fn mult_refs_and_strings() {
    let mut v = vec![1, 2, 3, 4, 5];
    let first = &v[0];
    //    v.push(6);
    // can't do this because first already borrows a reference to the vector
    println!("The first element is: {first}");

    // Strings are utf8
    let hello = String::from("السلام عليكم");
    let hello = String::from("Dobrý den");
    let hello = String::from("Hello");
    let hello = String::from("שָׁלוֹם");
    let hello = String::from("नमस्ते");
    let hello = String::from("こんにちは");
    let hello = String::from("안녕하세요");
    let hello = String::from("你好");
    let hello = String::from("Olá");
    let hello = String::from("Здравствуйте");
    let hello = String::from("Hola");

    let mut s = String::from("foo");
    s.push_str("bar");

    let mut s1 = String::from("foo");
    let s2 = "bar";
    s1.push_str(s2);
    println!("s2 is {s2}");

    let mut s = String::from("lo");
    s.push('l');

    let s1 = String::from("Hello, ");
    let s2 = String::from("world!");
    let s3 = s1 + &s2; // not s1 is moved here and can't be used later

    let s1 = String::from("tic");
    let s2 = String::from("tac");
    let s3 = String::from("toe");

    let s = s1 + "-" + &s2 + "-" + &s3;

    let s1 = String::from("tic");

    let s = format!("{s1}-{s2}-{s3}");
    println!("{}",s);

    for c in "Зд".chars() {
        println!("{c}");
    }
    println!("---");
    for b in "Зд".bytes() {
        println!("{b}");
    }


}

use std::collections::HashMap;

fn hash_maps() {
    let mut scores = HashMap::new();

    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);

    let team_name = String::from("Blue");
    let score = scores.get(&team_name).copied().unwrap_or(0);

    for (key, value) in &scores {
        println!("{key}: {value}");
    }

    let field_name = String::from("Favorite Color");
    let field_value = String::from("Blue");

    let mut map = HashMap::new();
    map.insert(field_name, field_value);
    // map owns these now

    // overwrite values
    println!("{:?}", scores);

    let mut scores = HashMap::new();
    scores.insert(String::from("Blue"), 10);

    scores.entry(String::from("Yellow")).or_insert(50);
    scores.entry(String::from("Blue")).or_insert(50);

    println!("{:?}", scores);

    let text = "hello world wonderful world";

    let mut map = HashMap::new();

    for word in text.split_whitespace() {
        let count = map.entry(word).or_insert(0);
        *count += 1
    }

    println!("{:?}", map);

}

fn loopy() {
    let v = vec![100, 32, 57];
    for i in &v {
        println!("{i}");
    }

    let mut v = vec![100, 32, 57];
    for i in &mut v {
        *i += 50;
    }
}
