use std::thread;
//use std::error::Error;
use std::io::prelude::*;
use std::time::Duration;


struct Expression {
    exp: String
}

impl Expression {
    fn new(exp: &str) -> Expression {
        Expression{exp: exp.to_string()}
    }
}


struct Board {
    port: Box<dyn serialport::SerialPort>
}


impl Board {
    const WIDTH:usize = 20;
    const HEIGHT:usize = 15;
    const LED_ALOCATION: [[u8; Board::WIDTH]; Board::HEIGHT] = [
        [  0,  1,  2,  3,  4,  5,  0,  0,  0,  0,  0,  0,  0,  0,200,199,198,197,196,  0],
        [  0,  6,  7,  8,  9, 10,  0,  0,  0,  0,  0,  0,  0,  0,195,194,193,192,191,  0],
        [  0, 11, 12, 13, 14, 15,  0,  0,  0,  0,  0,  0,  0,  0,190,189,188,187,186,  0],
        [  0, 16, 17, 18, 19, 20,  0,  0,  0,  0,  0,  0,  0,  0,185,184,183,182,181,  0],
        [  0, 21, 22, 23, 24, 25,  0,  0,  0,  0,  0,  0,  0,  0,180,179,178,177,176,  0],
        [ 26, 27, 28, 29, 30, 71, 66, 61, 56, 51,146,141,136,131,126,175,174,173,172,171],
        [ 31, 32, 33, 34, 35, 72, 67, 62, 57, 52,147,142,137,132,127,170,169,168,167,166],
        [ 36, 37, 38, 39, 40, 73, 68, 63, 58, 53,148,143,138,133,128,165,164,163,162,161],
        [ 41, 42, 43, 44, 45, 74, 69, 64, 59, 54,149,144,139,134,129,160,159,158,157,156],
        [ 46, 47, 48, 49, 50, 75, 70, 65, 60, 55,150,145,140,135,130,155,154,153,152,151],
        [  0,  0,  0,  0,  0, 76, 77, 78, 79, 80,125,124,123,122,121,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0, 81, 82, 83, 84, 85,120,119,118,117,116,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0, 86, 87, 88, 89, 90,115,114,113,112,111,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0, 91, 92, 93, 94, 95,110,109,108,107,106,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0, 96, 97, 98, 99,100,105,104,103,102,101,  0,  0,  0,  0,  0],];

    fn set(&mut self, exp: Expression) {
        let mut buf: [u8; 30] = Default::default();
        let mut cs = exp.exp;
        buf[0] = 0x80;
        cs.retain(|c| c == ' ' || c == '1');
        let v: Vec<char> = cs.chars().collect();
        for y in 0..Board::HEIGHT {
            for x in 0..Board::WIDTH {
                let n:usize = y * Board::WIDTH + x;
                if v[n] == '1' && Board::LED_ALOCATION[y][x] != 0 {
                    let led_index:usize = (Board::LED_ALOCATION[y][x]-1) as usize;
                    buf[led_index/7+1] |= 1<< (led_index % 7);
                }
            }
        }
        match self.port.write(&buf) {
            Ok(_) => std::io::stdout().flush().unwrap(),
            Err(_e) => {},
        };
    }

    fn new(port: &str) -> Board {
        let b = Board{port: serialport::new(port, 38400).open().unwrap()};
        thread::sleep(Duration::from_millis(4000));
        b
    }
}


fn main() {
    let e_normal = Expression::new("
 , , , , , , , , , , , , , , , , , , , ,
 , , , , , , , , , , , , , , , , , , , ,
 , , ,1,1, , , , , , , , , , ,1,1, , , ,
 , , ,1,1, , , , , , , , , , ,1,1, , , ,
 , , ,1,1, , , , , , , , , , ,1,1, , , ,
 , , ,1,1, , , , , , , , , , ,1,1, , , ,
 , , , , , , , , , , , , , , , , , , , ,
 , , , , , , , , , , , , , , , , , , , ,
 , , , , , , , , , , , , , , , , , , , ,
 , , , , , , , , , , , , , , , , , , , ,
 , , , , , ,1, , , , , , ,1, , , , , , ,
 , , , , , , ,1,1,1,1,1,1, , , , , , , ,
 , , , , , , , , , , , , , , , , , , , ,
 , , , , , , , , , , , , , , , , , , , ,
 , , , , , , , , , , , , , , , , , , , ,");


    let mut board = Board::new("/dev/ttyUSB0");
    board.set(e_normal);
}
