import {
    useEffect,
    useState
} from "react";


import api from "../api/axios";





function Vocabulary(){


    const [words,setWords] = useState([]);


    const [loading,setLoading] = useState(true);



    const [language,setLanguage] = useState(

        localStorage.getItem(
            "learningLanguage"
        )
        ||
        "de"

    );



    const [isMobile,setIsMobile] = useState(

        window.innerWidth <= 768

    );









    useEffect(()=>{


        function resize(){


            setIsMobile(

                window.innerWidth <= 768

            );


        }



        window.addEventListener(

            "resize",

            resize

        );



        return ()=>{


            window.removeEventListener(

                "resize",

                resize

            );


        };


    },[]);









    async function loadVocabulary(){


        try{


            setLoading(true);



            const response = await api.get(

                "/vocabulary"

            );



            const currentLanguage =

                localStorage.getItem(

                    "learningLanguage"

                )
                ||
                "de";



            setLanguage(

                currentLanguage

            );





            const filteredWords =

                response.data.filter(

                    word =>

                    word.source_language

                    ===

                    currentLanguage

                );





            setWords(

                filteredWords

            );





        }catch(error){


            console.error(

                error

            );


        }finally{


            setLoading(false);


        }


    }









    useEffect(()=>{


        loadVocabulary();


    },[]);









    useEffect(()=>{


        function handleLanguageChange(){


            loadVocabulary();


        }





        window.addEventListener(

            "languageChange",

            handleLanguageChange

        );





        return ()=>{


            window.removeEventListener(

                "languageChange",

                handleLanguageChange

            );


        };


    },[]);









    if(loading){


        return (

            <div className="loading-page">

                Loading vocabulary...

            </div>

        );


    }









    return (

        <div

        className="vocabulary-page"

        style={{


            padding:

                isMobile

                ?

                "0 16px"

                :

                "0 30px"


        }}

        >





            <h1>

                📚 Vocabulary

            </h1>





            <p className="subtitle">


                Current language:

                {" "}


                {


                    language === "de"

                    ?

                    "🇩🇪 German"

                    :

                    "🇬🇧 English"


                }


            </p>









            {


            words.length === 0


            ?


            <div className="empty-box">


                No vocabulary yet.


            </div>



            :



            <div

            className="vocabulary-list"

            >



            {


            words.map(

                word=>(


                <div

                key={word.id}

                className="vocabulary-card"

                style={{


                    overflowWrap:"break-word",

                    wordBreak:"break-word"


                }}

                >





                    <h2>


                        {word.word}


                    </h2>






                    <p>


                        <b>

                            Lemma:

                        </b>


                        {" "}


                        {word.lemma}


                    </p>








                    {


                    word.translation &&


                    <p>


                        <b>

                            Translation:

                        </b>


                        {" "}


                        {word.translation}


                    </p>


                    }








                    {


                    word.definition &&


                    <p>


                        <b>

                            Definition:

                        </b>


                        {" "}


                        {word.definition}


                    </p>


                    }








                    {


                    word.cefr &&


                    <p>


                        <b>

                            CEFR:

                        </b>


                        {" "}


                        {word.cefr}


                    </p>


                    }



                </div>


                )


            )


            }



            </div>


            }



        </div>

    );


}



export default Vocabulary;