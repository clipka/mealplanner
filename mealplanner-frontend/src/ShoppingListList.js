import { Link } from 'react-router-dom'
import useFetch from './useFetch'

const ShoppingListList = () => {
    const { error, isPending, data: shoppingLists } = useFetch('http://127.0.0.1:8080/shopping_lists')
    return (
        <div className="shopping-lists">
            { error && <div>{ error }</div> }
            { isPending && <div>Loading...</div> }
            { shoppingLists && shoppingLists.map(shoppingList => (
                <div className="shopping-list-preview" key={shoppingList.id}>
                    <Link to={`/shoppingLists/${shoppingList.id}`}>
                        <h2>Einkaufsliste #{shoppingList.id}</h2>
                    </Link>
                </div>
            ))}
        </div>
    )
}

export default ShoppingListList;