#![cfg_attr(not(feature = "std"), no_std)]

use ink_lang as ink;


#[ink::contract]
mod sensor_diag {

    /// センサ値をアラートありと判断する閾値
    const THRESHOLD: u32 = 10;
    
    /// センサ値に対して診断するためのスマートコントラクト。
    /// 以下の機能を有する。
    /// - センサ値をスマートコントラクト上で保存する
    /// - センサ値が閾値以上であればアラートを設定する
    /// - センサ値が閾値以上であればアラートカウンタをインクリメントする
    #[ink(storage)]
    pub struct SensorDiag {
        /// Stores a single `bool` value on the storage.
        value: u32,
        alert: bool,
        alert_count: u64,
    }

    impl SensorDiag {
        /// Constructor that initializes the `bool` value to the given `init_value`.
        #[ink(constructor, payable)]
        pub fn new(init_value: u32, init_alert: bool, init_alert_count: u64) -> Self {
            Self { 
                value: init_value,
                alert: init_alert,
                alert_count: init_alert_count
            }
        }

        /// Constructor that initializes the `bool` value to `false`.
        ///
        /// Constructors can delegate to other constructors.
        #[ink(constructor, payable)]
        pub fn default() -> Self {
            Self::new(Default::default(),Default::default(),Default::default())
        }

        /// A message that can be called on instantiated contracts.
        /// This one flips the value of the stored `bool` from `true`
        /// to `false` and vice versa.
        #[ink(message)]
        pub fn set(&mut self, value: u32) {
            self.value = value;
            if value < THRESHOLD {
                self.alert = false;
            }
            else {
                self.alert = true;
                self.alert_count += 1;
            }
        }

        /// Simply returns the current value of our `bool`.
        #[ink(message)]
        pub fn get_value(&self) -> u32 {
            self.value
        }

        /// Simply returns the current value of our `bool`.
        #[ink(message)]
        pub fn get_alert(&self) -> bool {
            self.alert
        }

        /// Simply returns the current value of our `bool`.
        #[ink(message)]
        pub fn get_alert_count(&self) -> u64 {
            self.alert_count
        }

    }

    /// Unit tests in Rust are normally defined within such a `#[cfg(test)]`
    /// module and test functions are marked with a `#[test]` attribute.
    /// The below code is technically just normal Rust code.
    #[cfg(test)]
    mod tests {
        /// Imports all the definitions from the outer scope so we can use them here.
        use super::*;

        /// Imports `ink_lang` so we can use `#[ink::test]`.
        use ink_lang as ink;

        /// We test if the default constructor does its job.
        #[ink::test]
        fn default_works() {
            let sensor_diag = SensorDiag::default();
            assert_eq!(sensor_diag.get_value(), 0);
            assert_eq!(sensor_diag.get_alert(), false);
        }

        /// We test a simple use case of our contract.
        #[ink::test]
        fn set_value_works() {
            let mut sensor_diag = SensorDiag::new(0, false,0);
            sensor_diag.set(65535);
            assert_eq!(sensor_diag.get_value(), 65535);
        }

        /// We test a simple use case of our contract.
        #[ink::test]
        fn set_alert_works() {
            let mut sensor_diag = SensorDiag::new(0, false,0);
            assert_eq!(sensor_diag.get_alert(), false);
            assert_eq!(sensor_diag.get_alert_count(), 0);
            sensor_diag.set(9);
            assert_eq!(sensor_diag.get_alert(), false);
            assert_eq!(sensor_diag.get_alert_count(), 0);
            sensor_diag.set(10);
            assert_eq!(sensor_diag.get_alert(), true);
            assert_eq!(sensor_diag.get_alert_count(), 1);
            sensor_diag.set(65535);
            assert_eq!(sensor_diag.get_alert(), true);
            assert_eq!(sensor_diag.get_alert_count(), 2);
        }
        /// We test a simple use case of our contract.
        #[ink::test]
        fn set_non_alert_works() {
            let mut sensor_diag = SensorDiag::new(10, true,1);
            sensor_diag.set(11);
            assert_eq!(sensor_diag.get_alert(), true);
            assert_eq!(sensor_diag.get_alert_count(), 2);
            sensor_diag.set(9);
            assert_eq!(sensor_diag.get_alert(), false);
            assert_eq!(sensor_diag.get_alert_count(), 1);
            sensor_diag.set(2);
            assert_eq!(sensor_diag.get_alert(), false);
            assert_eq!(sensor_diag.get_alert_count(), 1);
        }
    }
}
