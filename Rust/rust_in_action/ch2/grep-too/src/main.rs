use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;
use regex::Regex
use clap::{App,Arg};

fn process_lines<T: BufRead + Sized>(reader: T, re: Regex) {
  for line_ in reader.lines() {
    let line = line.unwrap();
    match re.find(&line) {
      Some(_) => println!("{}", line),
      None => (),
    }
  }
}

fn main() {
    let args = App::new("grep-too")
        .version("1.0")
        .about("Searches for patterns")
        .arg(Arg::with_name("pattern")
            .help("The pattern to search for")
            .takes_value(true)
            .required(true))
        .arg(Arg::with_name("input")
            .help("File to search")
            .takes_value(true)
            .required(false))
        .get_matches();

    let pattern = args.value_of("pattern").unwrap();      
    let re = Regex::new(pattern).unwrap();

    let input = args.value_of("input").unwrap_or("-");
    let f = File::open(input).unwrap();
    let reader = BufReader::new(f);

    if input == "-" {
      let stdin = io::stdin();
      let
      process_lines(reader, re);
    } else {
      let f = File::open(input).unwrap();
      let reader = BufReader::new(f);
      process_lines(reader, re);
    }
  }
