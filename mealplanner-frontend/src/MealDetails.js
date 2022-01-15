import { useNavigate, useParams } from "react-router-dom"
import useFetch from "./useFetch";

const MealDetails = () => {
    const { id } = useParams();
    const { data: meal, error, isPending } = useFetch('http://localhost:8080/meals/' + id);
    const navigate = useNavigate();

    const handleClick = () => {
        navigate('/');
    }

    return (
        <div className="meal-details">
            { isPending && <div>Loading ...</div> }
            { error && <div>{ error }</div> }
            { meal && (
                <article>
                    <h2>{ meal.title }</h2>
                    <p>Tags: <ul>{meal.tags.map(tag => {
                        return <li>{tag}</li>
                    })}</ul>
                    </p>
                    <p>Zutaten für: {meal.servings} Personen</p>
                    <h3>Zutaten</h3>
                    <p><ul>{meal.ingredients.map(ingredient => {
                        return (<li>
                                    <p>Name: {ingredient.name}</p>
                                    {ingredient.amount && <p>Menge: {ingredient.amount} {ingredient.unit}</p>}
                                </li>)
                    })}</ul>
                    </p>
                    <h3>Zubereitung</h3>
                    <p><ol>{meal.instructions.map(step => {
                        return <li>{step}</li>
                    })}</ol>
                    </p>
                    <button onClick={handleClick}>zurück</button>

                </article>
            )}
        </div>
    );
}

export default MealDetails;