import {
    useEffect,
    useState
} from "react";


import api from "../api/axios";



function Flashcards(){


    const [cards,setCards] = useState([]);


    const [sets,setSets] = useState([]);


    const [currentSet,setCurrentSet] = useState(1);


    const [currentIndex,setCurrentIndex] = useState(0);


    const [showBack,setShowBack] = useState(false);


    const [loading,setLoading] = useState(true);



    const [language,setLanguage] = useState(

        localStorage.getItem(
            "learningLanguage"
        )
        ||
        "de"

    );









    async function loadSets(){


        try{


            const res = await api.get(

                `/flashcards/sets?language=${language}`

            );


            setSets(

                res.data

            );


        }catch(error){


            console.error(error);


        }


    }









    async function loadCards(

        setNumber

    ){


        try{


            setLoading(true);



            const res = await api.get(

                `/flashcards?set_number=${setNumber}&language=${language}`

            );



            setCards(

                res.data

            );



            setCurrentIndex(0);



        }catch(error){


            console.error(error);


        }finally{


            setLoading(false);


        }


    }









    useEffect(()=>{


        loadSets();


        loadCards(

            currentSet

        );


    },[language]);









    useEffect(()=>{


        function handleLanguageChange(){


            const newLanguage =

                localStorage.getItem(

                    "learningLanguage"

                )
                ||
                "de";



            setLanguage(

                newLanguage

            );



            setCurrentSet(1);



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









    async function updateStatus(

        status

    ){


        const card =

            cards[currentIndex];



        if(!card){

            return;

        }





        try{


            await api.put(

                `/flashcards/${card.id}`,

                {

                    status

                }

            );



            nextCard();



        }catch(error){


            console.error(error);


        }


    }









    function nextCard(){


        setShowBack(false);



        if(

            currentIndex <

            cards.length - 1

        ){


            setCurrentIndex(

                currentIndex + 1

            );


        }

        else{


            alert(

                "Set completed!"

            );


        }


    }









    function changeSet(number){


        setCurrentSet(

            number

        );


        loadCards(

            number

        );


    }









    if(loading){


        return (

            <div

            style={{

                padding:"40px"

            }}

            >

                Loading flashcards...

            </div>

        );

    }









    if(cards.length===0){


        return (

            <div

            style={{

                padding:"40px"

            }}

            >


                <h1>

                    🎴 Flashcards

                </h1>



                <p>

                    No flashcards available.

                </p>


            </div>


        );

    }








    const card =

        cards[currentIndex];









    return (

        <div

        style={{

            maxWidth:"700px",

            margin:"40px auto",

            textAlign:"center",

            padding:"20px"

        }}

        >



            <h1>

                🎴 Flashcards

            </h1>





            <p

            style={{

                color:"#666"

            }}

            >

                {

                    language==="de"

                    ?

                    "🇩🇪 German"

                    :

                    "🇬🇧 English"

                }


            </p>







            <div>

            {

                sets.map(

                    s=>(


                    <button

                    key={

                        s.set_number

                    }


                    onClick={()=>changeSet(

                        s.set_number

                    )}


                    style={{

                        margin:"5px",

                        padding:"8px 15px",

                        borderRadius:"8px",

                        cursor:"pointer"

                    }}

                    >

                        Set {s.set_number}

                    </button>


                    )


                )

            }


            </div>









            <h3>

                Set {currentSet}

                {" | "}

                {currentIndex + 1}

                /

                {cards.length}


            </h3>









            <div

            onClick={()=>setShowBack(

                !showBack

            )}


            style={{

                height:"260px",

                border:"1px solid #ddd",

                borderRadius:"16px",

                display:"flex",

                alignItems:"center",

                justifyContent:"center",

                padding:"30px",

                cursor:"pointer",

                fontSize:"30px",

                background:"#fff",

                boxShadow:

                "0 4px 15px rgba(0,0,0,0.1)",

                whiteSpace:"pre-line"

            }}

            >


                {

                    showBack

                    ?

                    card.back

                    :

                    card.front

                }


            </div>









            <p

            style={{

                color:"#777"

            }}

            >

                Click card to flip

            </p>









            <div

            style={{

                display:"flex",

                justifyContent:"center",

                gap:"20px",

                marginTop:"30px"

            }}

            >


                <button

                onClick={()=>updateStatus(

                    "learning"

                )}

                >

                    Again

                </button>




                <button

                onClick={()=>updateStatus(

                    "mastered"

                )}

                >

                    Mastered ✓

                </button>


            </div>



        </div>

    );


}


export default Flashcards;