import React, { Component } from "react";
import ChatBot from "react-simple-chatbot";
import Post from "./Post";
import Teachme from "./teachme";

class SimpleForm extends Component {
	render() {
		return (
			<ChatBot
				steps={[
					{
						id: "1",
						message: "Please input something",
						trigger: "message",
					},
					{
						id: "message",
						user: true,
						trigger: "res_from_robot",
					},
					{
						id: "res_from_robot",
						component: <Post />,
						asMessage: true,
						trigger: "evaluate",
						// waitAction: true
					},
					{
						id: "evaluate",
						options: [
							{
								value: "good",
								label: "Good",
								trigger: "thankyou",
							},
							{
								vale: "bad",
								label: "I don't like it. I want to teach you",
								trigger: "teachme",
							},
						],
					},
					{
						id: "teachme",
						message: "Input ideal response",
						trigger: "res",
					},
					{
						id: "res",
						user: true,
						trigger: "whatever",
					},
					{
						id: "whatever",
						component: <Teachme />,
						asMessage: true,
						trigger: "1",
						// waitAction: true
					},
					{
						id:'thankyou',
						message:'thank you :)',
						trigger: "1"
					}
				]}
			/>
		);
	}
}

export default SimpleForm;
