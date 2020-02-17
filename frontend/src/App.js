import React, {Component} from 'react';
import classes from './components/quiz/Quiz.module.scss'
import Quiz from "./components/quiz/Quiz";


class App extends Component {
    render() {
        return (
            <div className={classes.QuizContainer}>
                <Quiz />
            </div>
        );
    }
}

export default App