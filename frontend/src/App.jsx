import {
    BrowserRouter,
    Routes,
    Route
} from "react-router-dom";


import Navbar from "./components/Navbar";


import ReadingList from "./pages/ReadingList";
import ReadingDetail from "./pages/ReadingDetail";
import CreateReading from "./pages/CreateReading";
import Vocabulary from "./pages/Vocabulary";



function App(){


    return (

        <BrowserRouter>


            <Navbar />


            <Routes>


                <Route

                    path="/"

                    element={
                        <ReadingList />
                    }

                />



                <Route

                    path="/create"

                    element={
                        <CreateReading />
                    }

                />



                <Route

                    path="/readings/:id"

                    element={
                        <ReadingDetail />
                    }

                />



                <Route

                    path="/vocabulary"

                    element={
                        <Vocabulary />
                    }

                />


            </Routes>


        </BrowserRouter>

    );


}


export default App;