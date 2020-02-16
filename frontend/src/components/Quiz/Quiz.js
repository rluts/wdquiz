import React, {Component} from 'react';
import {connect} from 'react-redux';
import classes from './Quiz.module.scss'
import { Button, TextField } from '@material-ui/core';
import {ask, check} from '../../actions'
import CircularProgress from "@material-ui/core/CircularProgress";

function mapStateToProps(state) {
    return state.quiz;
}

const mapDispatchToProps = dispatch => {
  return {
    loadQuiz: () => {
        dispatch(ask());
    },
    checkAnswer: (answer) => {
        dispatch(check(answer))
    }
  };
};

class Quiz extends Component {

    componentDidMount() {
        this.props.loadQuiz()
    }

    checkAnswer = () => {
        this.props.checkAnswer(this.state.answer)
    };

    handleChangeAnswer = (event) => {
      this.setState({answer: event.target.value});
    };

    componentDidUpdate(prevProps, prevState, snapshot) {
          if (prevProps.right) {
              setTimeout(() => {
                prevProps.ask()
              }, 2000);
          }
    }

    render() {
        return (
            <div className={classes.Quiz}>
                <h2>{this.props.question}</h2>
                {this.props.right ? <h3>Right answer</h3> : null}
                <div>
                    {this.props.imageUrl && !this.props.loading ?
                    <img  className={classes.QuizImage} src={'http://127.0.0.1' + this.props.imageUrl} alt={this.props.questionId} />
                    : <CircularProgress />
                    }
                </div>
                <form className={classes.FormContainer}>
                    <TextField id="outlined-basic" label="Answer" onChange={this.handleChangeAnswer} variant="outlined" />
                    <Button variant="contained" color="primary" onClick={this.checkAnswer} disableElevation>
                      Next >>
                    </Button>
                </form>
            </div>
        );
    }
}

export default connect(
    mapStateToProps, mapDispatchToProps
)(Quiz);