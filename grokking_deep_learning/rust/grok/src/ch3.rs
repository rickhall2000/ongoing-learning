use ndarray::prelude::*;

pub fn first_example() {
    let weights  = vec![0.1, 0.2, 0.0];
    let toes = [8.5, 9.5, 9.9, 9.0];
    let wlrec = [0.65, 0.8, 0.8, 0.9];
    let nfans = [1.2, 1.3, 0.5, 1.0];
    
    let input = vec![toes[0], wlrec[0], nfans[0]];
    let pred = neural_network1(input, weights);
    println!("{}", pred);
}

fn neural_network1(input: Vec<f64>, weights: Vec<f64>) -> f64 {
    w_sum(input, weights)
}

fn w_sum(a: Vec<f64>, b: Vec<f64>) -> f64 {
    
    assert!(a.len() == b.len());

    let mut output = 0.0;
    for i in 0..a.len() {
        output += a[i] * b[i];
    }
    output
}

fn neural_network2(input: Array1<f64>, weights: Array1<f64>) -> f64 {
    input.dot(&weights)
}

pub fn second_example() {
    let weights = array![0.1, 0.2, 0.0];
    let toes = array![8.5, 9.5, 9.9, 9.0];
    let wlrec = array![0.65, 0.8, 0.8, 0.9];
    let nfans = array![1.2, 1.3, 0.5, 1.0];
    let input = array![toes[0], wlrec[0], nfans[0]];

    let pred = neural_network2(input, weights);
    println!("{}", pred); 
}