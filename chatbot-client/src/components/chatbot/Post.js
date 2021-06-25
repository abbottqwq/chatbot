import React, { Component } from 'react';
import axios from 'axios';


class Post extends Component {
  constructor(props) {
    super(props);
    const { steps } = this.props;
    const { message } = steps;
    let res = '';
    this.state =  { message, res }; 
  }


  async componentDidMount() {
    let response = await axios.post(`/api/message`, {'message': this.state.message.value});
    console.log(response.status);
    this.setState({res:response.data['res']});
    // axios.post(`/api/message`, {'message': this.state.message.value})
    // .then(response => {
    //   console.log(response.status);
    //   this.setState({res:response.data['res']})
    // }).catch(function(error) {
    //   console.log(error);
    // });
  }

  render() {
    return (
      <div>{this.state.res}</div>
      );
    }
  };


  export default Post;