import MealsList from "./MealsList";
import useFetch from "./useFetch";

const Home = () => {
    const { error, isPending, data: meals } = useFetch('http://127.0.0.1:8080/meals')
    return (
        <div className="home">
            { error && <div>{ error }</div> }
            { isPending && <div>Loading...</div> }
            { meals && <MealsList meals={meals} /> }
        </div>
     );
}

export default Home;