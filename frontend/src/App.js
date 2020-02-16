import React, {Component} from 'react';
import classes from './components/Quiz/Quiz.module.scss'
import Quiz from "./components/Quiz/Quiz";


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