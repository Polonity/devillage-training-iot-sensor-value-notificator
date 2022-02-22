//SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.7;

contract sensorDiag {
	uint32 private THRESHOLD = 10;

	/// storage variants
	uint32 private value;
	bool private alert;
	uint64 private alert_count;

	/// Constructor that initializes the `bool` value to the given `init_value`.
	constructor() {
		value = 0;
		alert = false;
		alert_count = 0;
	}

	/// A message that can be called on instantiated contracts.
	/// This one flips the value of the stored `bool` from `true`
	/// to `false` and vice versa.
	function set(uint32 _value) public {
		value = _value;
		if (_value < THRESHOLD) {
			// Non alert
			alert = false;
		}
		else {
			// alert
			alert = true;
			alert_count += 1;
		}
	}

	/// Simply returns the current value of our `bool`.
	function get_value() public view returns (uint32) {
		return value;
	}

	/// Simply returns the current value of our `bool`.
	function get_alert() public view returns (bool) {
		return alert;
	}

	/// Simply returns the current value of our `bool`.
	function get_alert_count() public view returns (uint64) {
		return alert_count;
	}
}
