import {
    Link
} from "react-router-dom";


function Navbar(){


    return (

        <nav>

            <Link to="/">
                Readings
            </Link>


            {" | "}


            <Link to="/vocabulary">
                Vocabulary
            </Link>


        </nav>

    );

}


export default Navbar;