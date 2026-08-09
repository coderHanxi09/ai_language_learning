import {
    useEffect,
    useState
} from "react";


import {
    Link
} from "react-router-dom";


import api from "../api/axios";





function ReadingList(){


    const [readings,setReadings] = useState([]);



    const [language,setLanguage] = useState(

        localStorage.getItem(
            "learningLanguage"
        )
        ||
        "de"

    );



    const [loading,setLoading] = useState(true);









    async function loadReadings(){


        try{


            setLoading(true);



            const res = await api.get(

                "/readings"

            );



            const filtered = res.data.filter(


                reading =>


                    reading.source_language

                    ===

                    language


            );



            setReadings(

                filtered

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


        loadReadings();


    },[language]);









    useEffect(()=>{


        function updateLanguage(){


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

            updateLanguage

        );





        return ()=>{


            window.removeEventListener(

                "languageChange",

                updateLanguage

            );


        };


    },[]);









    if(loading){


        return (

            <div className="loading-page">

                Loading readings...

            </div>

        );


    }









    return (


        <div className="reading-list-page">





            {/* Header */}



            <div className="reading-list-header">



                <div>


                    <h1>

                        My Readings

                    </h1>




                    <p className="subtitle">


                        {


                        language === "de"

                        ?

                        "🇩🇪 German readings"

                        :

                        "🇬🇧 English readings"


                        }


                    </p>


                </div>








                <Link

                to="/create"

                className="create-button"

                >

                    + Create Reading

                </Link>




            </div>









            {


            readings.length === 0



            ?



            (

                <div className="empty-box">


                    No readings available.


                </div>


            )



            :



            (

                <div className="reading-grid">



                {


                readings.map(

                    reading => (


                    <Link


                    key={reading.id}


                    to={`/readings/${reading.id}`}


                    className="reading-card-link"


                    >




                        <div className="reading-card">





                            <h3>


                                {


                                reading.title

                                ||

                                "Untitled Reading"


                                }


                            </h3>





                            <p>


                                {


                                reading.difficulty

                                ||

                                "B2"


                                }


                            </p>







                            <span


                            className={

                                reading.status === "completed"

                                ?

                                "status completed"

                                :

                                "status processing"

                            }


                            >


                                {reading.status}


                            </span>




                        </div>




                    </Link>


                    )


                )


                }



                </div>


            )


            }




        </div>


    );


}



export default ReadingList;