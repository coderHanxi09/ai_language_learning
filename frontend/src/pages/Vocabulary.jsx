import {
    useEffect,
    useState
} from "react";

import api from "../api/axios";


function Vocabulary(){


    const [words,setWords] = useState([]);



    useEffect(()=>{


        api.get("/vocabulary")

        .then(res=>{


            console.log(res.data);


            setWords(
                res.data
            );


        })

        .catch(err=>{


            console.error(err);


        });


    },[]);




    return (

        <div>


            <h1>
                My Vocabulary
            </h1>



            {
                words.length === 0 && (

                    <p>
                        No vocabulary yet.
                    </p>

                )
            }



            {
                words.map(
                    word=>(


                    <div
                    key={word.id}
                    style={{
                        border:"1px solid gray",
                        padding:"10px",
                        margin:"10px"
                    }}
                    >


                        <h3>
                            {word.word}
                        </h3>


                        <p>
                            {word.definition}
                        </p>


                        <p>
                            CEFR:
                            {word.cefr}
                        </p>


                    </div>


                    )

                )
            }



        </div>

    );

}


export default Vocabulary;