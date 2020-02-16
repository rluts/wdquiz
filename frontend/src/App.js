import React, {Component} from 'react';
import classes from './components/Quiz/Quiz.module.scss'
import Quiz from "./components/Quiz/Quiz";


class App extends Component {
    render() {
        return (
            <div className={classes.QuizContainer}>
                <Quiz question={"What the country is this?"} imageUrl={"/media/65_file_1.png"} questionId={"65"}/>
            </div>
        );
    }
}

export default App