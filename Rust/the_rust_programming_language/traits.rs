use std::fmt::{Debug, Display};

/* - no default impl
pub trait Summary {
    fn summarize(&self) -> String;
}
 */

 pub trait Summary {
    fn summarize(&self) -> String {
        String::from("(Read more...)")
    }
}

pub struct NewsArticle {
    pub headline: String,
    pub location: String,
    pub author: String,
    pub content: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!(
            "{}, by {} ({})",
            self.headline,
            self.author,
            self.location
        )
    }
}

pub struct Tweet {
    pub username: String,
    pub content: String,
    pub reply: bool,
    pub retweet: bool,
}

impl Summary for Tweet {
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }
}

fn main() {
    let tweet = Tweet {
        username: String::from("horse_ebooks"),
        content: String::from(
            "Of course, as you probably already know, people",
        ),
        reply: false,
        retweet: false,
    };

    println!("1 new tweet: {}", tweet.summarize());
}

pub fn notify(item: &impl Summary) {
    println!("Breaking news! {}", item.summarize());
}

pub fn notify_long_form<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}

pub fn notify_allow_diff_types(item1: &impl Summary, item2: impl Summary) {}
pub fn notifiy_restrict_to_one_type<T: Summary>(item1: &T, item2: &T) {}

pub fn notify_mult_traits(item1: &(impl Summary + Display)) {}
pub fn notify_mult_traits_long<T: Summary + Display>(item: &T) {}

fn sum_function<T, U>(t: &T, u: &U) -> i32
where 
    T: Display + Clone,
    U: Clone + Debug,
{1}