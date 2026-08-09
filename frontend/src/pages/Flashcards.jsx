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









    async function loadCards(setNumber){


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









    async function updateStatus(status){


        const card = cards[currentIndex];



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

            currentIndex < cards.length - 1

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

            <div className="loading-page">

                Loading flashcards...

            </div>

        );

    }









    if(cards.length === 0){


        return (

            <div className="flashcards-page">


                <h1>

                    🎴 Flashcards

                </h1>



                <p>

                    No flashcards available.

                </p>



            </div>

        );


    }









    const card = cards[currentIndex];









    return (

        <div

        className="flashcards-page"

        style={{

            width:"100%",

            maxWidth:"700px",

            margin:

                isMobile

                ?

                "20px auto"

                :

                "40px auto",

            padding:

                isMobile

                ?

                "0 16px"

                :

                "0 30px",

            textAlign:"center"

        }}

        >






            <h1>

                🎴 Flashcards

            </h1>






            <p className="subtitle">


                {

                    language === "de"

                    ?

                    "🇩🇪 German"

                    :

                    "🇬🇧 English"


                }


            </p>









            <div

            className="flashcard-sets"

            style={{

                display:"flex",

                flexWrap:"wrap",

                justifyContent:"center",

                gap:"8px",

                marginBottom:"20px"

            }}

            >



            {

            sets.map(

                s=>(


                <button


                key={s.set_number}


                onClick={()=>changeSet(

                    s.set_number

                )}


                style={{


                    padding:

                        isMobile

                        ?

                        "8px 12px"

                        :

                        "8px 15px",


                    borderRadius:"10px",


                    border:

                    currentSet === s.set_number

                    ?

                    "2px solid #2563eb"

                    :

                    "1px solid #ddd",


                    background:

                    currentSet === s.set_number

                    ?

                    "#eff6ff"

                    :

                    "white",


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


            className="flashcard"


            onClick={()=>setShowBack(

                !showBack

            )}


            style={{


                width:"100%",


                minHeight:

                    isMobile

                    ?

                    "220px"

                    :

                    "260px",


                border:"1px solid #ddd",


                borderRadius:"18px",


                display:"flex",


                alignItems:"center",


                justifyContent:"center",


                padding:

                    isMobile

                    ?

                    "20px"

                    :

                    "30px",


                cursor:"pointer",


                fontSize:

                    isMobile

                    ?

                    "22px"

                    :

                    "30px",


                background:"white",


                boxShadow:

                "0 4px 15px rgba(0,0,0,0.1)",


                whiteSpace:"pre-line",


                overflowWrap:"break-word"

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

            className="flip-hint"

            style={{

                color:"#777"

            }}

            >

                Click card to flip

            </p>









            <div

            className="flashcard-actions"


            style={{


                display:"flex",


                flexDirection:

                    isMobile

                    ?

                    "column"

                    :

                    "row",


                justifyContent:"center",


                gap:"15px",


                marginTop:"30px"

            }}

            >




                <button


                onClick={()=>updateStatus(

                    "learning"

                )}


                style={{


                    padding:"12px 25px",

                    borderRadius:"10px",

                    cursor:"pointer"

                }}

                >

                    Again

                </button>





                <button


                onClick={()=>updateStatus(

                    "mastered"

                )}


                style={{


                    padding:"12px 25px",

                    borderRadius:"10px",

                    cursor:"pointer"

                }}

                >

                    Mastered ✓

                </button>





            </div>







        </div>

    );


}


export default Flashcards;