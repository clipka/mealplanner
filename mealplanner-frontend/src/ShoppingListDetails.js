import { useNavigate, useParams } from "react-router";
import useFetch from "./useFetch";


const ShoppingListDetails = () => {
    const { id } = useParams();
    const { data: shoppingList, error, isPending } = useFetch('http://localhost:8080/shopping_lists/' + id);
    const navigate = useNavigate();

    const handleClickHome = () => {
        navigate('/shoppingLists');
    }

    return (
        <div className="shopping-list-details">
            { isPending && <div>Loading...</div> }
            { error && <div>{ error }</div> }
            { shoppingList && (
                <article>
                    <h2>Einkaufsliste { shoppingList.id }</h2>
                    <p><ul>
                        {shoppingList.items.map(item => {
                            return (
                                <li>
                                <p>{ item.amount } { item.unit } { item.name } </p>
                                </li>
                            )
                        })}
                    </ul>
                    </p>
                    <button onClick={handleClickHome}>zurück</button>
                </article>
            )}
        </div>
    );
}

export default ShoppingListDetails;