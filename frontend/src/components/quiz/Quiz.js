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
    checkAnswer: (answer, questionId) => {
        dispatch(check(answer, questionId))
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

    checkAnswer = (event) => {
        event.preventDefault();
        if (this.state.answer.trim()) {
            this.props.checkAnswer(this.state.answer, this.props.questionId);
            this.setState({answer: ''})
        }
    };

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.answered && this.props.right) {
            this.props.newQuiz();
            this.props.loadQuiz();
        }
    }

    handleChangeAnswer = (event) => {
      this.setState({answer: event.target.value});
    };

    render() {
        return (
            <div className={classes.Quiz}>
                <h2>{this.props.question}</h2>
                {this.props.answered || this.props.loading ? this.props.right ? <h3>Correct</h3> : !this.props.loading ? <h3>Not correct</h3>: null: null}
                <div>
                    {this.props.imageUrl && !this.props.loading ?
                    <img  className={classes.QuizImage} src={this.props.imageUrl} alt={this.props.questionId} />
                    : <CircularProgress />
                    }
                </div>
                <form className={classes.FormContainer} onSubmit={this.checkAnswer}>
                    <TextField id="outlined-basic"  label="Answer" value={this.state.answer} onChange={this.handleChangeAnswer} variant="outlined" />
                    <Button type="submit" variant="contained" color="primary" disableElevation>
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