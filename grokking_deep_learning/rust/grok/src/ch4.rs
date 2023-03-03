pub fn hot_and_cold_learning() {
    let mut weight = 0.5;
    let input = 0.5;
    let goal_prediction :f32 = 0.8;

    let step_amount = 0.001;

    for _iteration in 0..1101 {
        let prediction = input * weight;
        let error  = (prediction - goal_prediction).powf(2.0);

        println!("Error: {} Prediction: {}", error, prediction);

        let up_prediction = input * (weight + step_amount);
        let up_error = (goal_prediction - up_prediction).powf(2.0);

        let down_prediction = input * (weight - step_amount);
        let down_error = (goal_prediction - down_prediction).powf(2.0);

        if down_error < up_error {
            weight = weight - step_amount;
        }

        if down_error > up_error {
            weight = weight + step_amount;
        }
    }
}