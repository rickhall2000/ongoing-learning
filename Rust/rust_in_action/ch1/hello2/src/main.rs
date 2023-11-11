fn greet_world() {
    println!("Hello, world!");
    let sourthern_germany = "Grüß Gott!";
    let japan = "ハロー・ワールド";
    let regions = [sourthern_germany, japan];
    for region in regions.iter() {
        println!("{}", &region);
    }
}
fn main() {
    greet_world();
}
