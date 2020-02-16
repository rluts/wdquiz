import React, {Component} from 'react';
import {connect} from 'react-redux';
import classes from './Quiz.module.scss'
import { Button } from '@material-ui/core';

function mapStateToProps(state) {
    return {};
}

function mapDispatchToProps(dispatch) {
    return {};
}

class Quiz extends Component {
    render() {
        return (
            <div className={classes.Quiz}>
                <h2>{this.props.question}</h2>
                <div>
                    <img  className={classes.QuizImage} src={'http://127.0.0.1' + this.props.imageUrl} alt={this.props.questionId} />
                </div>
                <div className={classes.ButtonContainer}>
                    <Button variant="contained" color="primary" disableElevation>
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