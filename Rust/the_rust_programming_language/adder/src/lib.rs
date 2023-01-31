pub fn add(left: usize, right: usize) -> usize {
    left + right
}

pub fn add_two(num: usize) -> usize {
    num + 2
}

#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,    
}

impl Rectangle {
    fn canHold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn exploration() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }

    #[test]
    fn larger_can_hold_smaller() {
        let larger = Rectangle {
            width: 8,
            height: 7
        };
        let smaller = Rectangle {
            width: 5,
            height: 1,
        };
        assert!(larger.canHold(&smaller));
    }

        #[test]
    fn smaller_cant_hold_larger() {
        let larger = Rectangle {
            width: 8,
            height: 7
        };
        let smaller = Rectangle {
            width: 5,
            height: 1,
        };
        assert!(!smaller.canHold(&larger));
    }

}
