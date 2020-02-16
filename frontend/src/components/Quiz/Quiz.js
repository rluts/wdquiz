import React, {Component} from 'react';
import {connect} from 'react-redux';
import classes from './Quiz.module.scss'
import { Button, TextField } from '@material-ui/core';
import {ask, check, newQuiz} from '../../actions'
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
    },
    newQuiz: () => {
        dispatch(newQuiz())
    }
  };
};

class Quiz extends Component {

    state = {
        answer: ''
    };

    componentDidMount() {
        this.props.loadQuiz()
    }

    checkAnswer = () => {
        if (this.state.answer.trim()) {
            this.props.checkAnswer(this.state.answer)
        }
    };

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.answered && this.props.right) {
            this.props.newQuiz();
            setTimeout(() => {this.props.loadQuiz();}, 1000)
        }
    }

    handleChangeAnswer = (event) => {
      this.setState({answer: event.target.value});
    };

    render() {
        return (
            <div className={classes.Quiz}>
                <h2>{this.props.question}</h2>
                {this.props.answered ? this.props.right ? <h3>Correct</h3> : <h3>Not correct</h3>: null}
                <div>
                    {this.props.imageUrl && !this.props.loading ?
                    <img  className={classes.QuizImage} src={'http://127.0.0.1' + this.props.imageUrl} alt={this.props.questionId} />
                    : <CircularProgress />
                    }
                </div>
                <div className={classes.FormContainer}>
                    <TextField id="outlined-basic" label="Answer" onChange={this.handleChangeAnswer} variant="outlined" />
                    <Button variant="contained" color="primary" onClick={this.checkAnswer} disableElevation>
                      Next >>
                    </Button>
                </div>
            </div>
        );
    }
}

export default connect(
    mapStateToProps, mapDispatchToProps
)(Quiz);