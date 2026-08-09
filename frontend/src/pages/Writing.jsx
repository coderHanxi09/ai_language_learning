import {
    useEffect,
    useState
} from "react";


import {
    useNavigate
} from "react-router-dom";


import api from "../api/axios";





function Writing(){


    const navigate = useNavigate();



    const [language,setLanguage] = useState(

        localStorage.getItem(
            "learningLanguage"
        )
        ||
        "de"

    );



    const [level,setLevel] = useState("B2");


    const [vocabularyCount,setVocabularyCount] = useState(0);


    const [loading,setLoading] = useState(false);









    useEffect(()=>{


        function syncLanguage(){


            setLanguage(

                localStorage.getItem(
                    "learningLanguage"
                )
                ||
                "de"

            );


        }




        window.addEventListener(

            "languageChange",

            syncLanguage

        );





        return ()=>{


            window.removeEventListener(

                "languageChange",

                syncLanguage

            );


        };


    },[]);









    async function loadVocabularyCount(){


        try{


            const res = await api.get(

                "/vocabulary"

            );



            const filtered =

                res.data.filter(

                    item =>

                    item.source_language

                    ===

                    language

                );



            setVocabularyCount(

                filtered.length

            );



        }catch(error){


            console.error(

                error

            );


        }


    }









    useEffect(()=>{


        loadVocabularyCount();


    },[language]);









    async function generate(){


        try{


            setLoading(true);



            const res = await api.post(

                "/writing/generate",

                {

                    language,

                    level

                }

            );





            if(res.data.id){


                navigate(

                    `/readings/${res.data.id}`

                );


            }
            else{


                setLoading(false);


            }



        }catch(error){


            console.error(

                error

            );



            alert(

                "Failed to generate article"

            );


            setLoading(false);


        }


    }









    return (

        <div className="writing-page">



            <h1>

                AI Writing

            </h1>





            <p className="subtitle">

                Generate a personalized reading article
                based on your vocabulary.

            </p>









            <div className="writing-info-card">


                <p>

                    Vocabulary available:

                    {" "}

                    <b>

                        {vocabularyCount}

                    </b>

                </p>





                <p>

                    Words used:

                    {" "}

                    <b>

                        {

                        Math.min(

                            50,

                            vocabularyCount

                        )

                        }

                    </b>

                </p>


            </div>









            <label>

                Language

            </label>



            <select

            className="writing-select"


            value={language}



            onChange={

                e=>{

                    setLanguage(

                        e.target.value

                    );

                }

            }


            >


                <option value="de">

                    German

                </option>


                <option value="en">

                    English

                </option>


            </select>









            <label>

                Level

            </label>






            <select


            className="writing-select"


            value={level}



            onChange={

                e=>

                setLevel(

                    e.target.value

                )

            }


            >


                <option value="A2">

                    A2

                </option>


                <option value="B1">

                    B1

                </option>


                <option value="B2">

                    B2

                </option>


                <option value="C1">

                    C1

                </option>


            </select>









            <button


            className="generate-button"



            onClick={generate}



            disabled={loading}



            >


                {

                loading

                ?

                "Generating..."

                :

                "Generate Article"


                }



            </button>




        </div>

    );


}


export default Writing;