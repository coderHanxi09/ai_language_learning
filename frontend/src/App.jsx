import {
    BrowserRouter,
    Routes,
    Route
} from "react-router-dom";



import Navbar from "./components/Navbar";



import ReadingList from "./pages/ReadingList";

import CreateReading from "./pages/CreateReading";

import ReadingDetail from "./pages/ReadingDetail";

import Vocabulary from "./pages/Vocabulary";

import Flashcards from "./pages/Flashcards";

import Writing from "./pages/Writing";





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

                path="/readings"

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







                <Route

                path="/flashcards"

                element={
                    <Flashcards />
                }

                />







                <Route

                path="/writing"

                element={
                    <Writing />
                }

                />





            </Routes>



        </BrowserRouter>


    );


}



export default App;