import React, { Component } from "react";
import axios from "axios";

class Teachme extends Component {
	constructor(props) {
		super(props);
		const { steps } = this.props;
		const { message, res } = steps;
		let success = true;
		this.state = { message, res, success };
	}

	async componentDidMount() {
		let response = axios.post(`/api/teachme`, {
			message: this.state.message.value,
			res: this.state.res.value,
		});
		console.log(response.status);
		if ("error" in response.data) {
			this.setState({ success: false });
		}
		// axios
		// 	.post(`/api/teachme`, {
		// 		message: this.state.message.value,
		// 		res: this.state.res.value,
		// 	})
		// 	.then((response) => {
		// 		console.log(response.status);
		// 		//   this.setState({success:response.data['res']})
		// 		if ("error" in response.data) {
		// 			this.setState({ success: false });
		// 		}
		// 	})
		// 	.catch(function(error) {
		// 		console.log(error);
		// 	});
	}

	render() {
		if (this.state.success) return <div>Great, try it</div>;
		else return <div>Sorry, network error. Please try again.</div>;
	}
}

export default Teachme;
