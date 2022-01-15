import { Link } from 'react-router-dom'

const MealsList = ({ meals }) => {
    return (
        <div className="menu-list">
            {meals.map(meal => (
                <div className="meal-preview" key={meal.id} >
                    <Link to={`/meals/${meal.id}`}>
                        <h2>{ meal.title }</h2>
                        <p> Tags: {meal.tags} </p>
                    </Link>
                </div>
            ))}
        </div>
    );
}

export default MealsList;