import {
    useEffect,
    useState
} from "react";


import {
    Link
} from "react-router-dom";


import api from "../api/axios";





function ReadingList(){


    const [readings,setReadings]
        = useState([]);


    const [language,setLanguage]
        = useState(

            localStorage.getItem(
                "learningLanguage"
            )
            ||
            "de"

        );


    const [loading,setLoading]
        = useState(true);









    async function loadReadings(){


        try{


            setLoading(true);



            const res = await api.get(

                "/readings"

            );





            const filtered =

                res.data.filter(

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


            const newLanguage =

                localStorage.getItem(

                    "learningLanguage"

                )
                ||
                "de";



            setLanguage(

                newLanguage

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

            <div

            style={{

                textAlign:"center",

                marginTop:"80px"

            }}

            >

                Loading readings...

            </div>

        );


    }









    return (


        <div

        style={{


            maxWidth:"1100px",


            margin:"40px auto",


            padding:"0 30px"


        }}

        >







            <div

            style={{

                display:"flex",

                justifyContent:"space-between",

                alignItems:"center",

                marginBottom:"35px"

            }}

            >




                <div>


                    <h1

                    style={{

                        marginBottom:"8px"

                    }}

                    >

                        My Readings

                    </h1>





                    <p

                    style={{

                        color:"#6b7280"

                    }}

                    >

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

                style={{


                    textDecoration:"none",


                    background:"#2563eb",


                    color:"white",


                    padding:"12px 20px",


                    borderRadius:"12px",


                    fontWeight:"600"


                }}

                >

                    + Create Reading

                </Link>





            </div>









            {


            readings.length === 0


            ?


            (

                <div

                style={{


                    textAlign:"center",


                    padding:"60px",


                    background:"#f9fafb",


                    borderRadius:"20px",


                    color:"#6b7280"


                }}

                >


                    No readings available.


                </div>


            )



            :



            (

                <div

                style={{

                    display:"grid",

                    gridTemplateColumns:

                    "repeat(auto-fill,minmax(300px,1fr))",

                    gap:"20px"

                }}

                >




                {


                readings.map(

                    reading=>(


                    <Link

                    key={

                        reading.id

                    }


                    to={

                        `/readings/${reading.id}`

                    }


                    style={{


                        textDecoration:"none",


                        color:"inherit"


                    }}

                    >





                        <div

                        style={{


                            background:"white",


                            border:

                            "1px solid #e5e7eb",


                            borderRadius:"18px",


                            padding:"24px",


                            minHeight:"150px",


                            boxShadow:

                            "0 4px 12px rgba(0,0,0,0.05)"


                        }}

                        >




                            <h3>


                                {

                                    reading.title

                                    ||

                                    "Untitled Reading"


                                }


                            </h3>






                            <p

                            style={{


                                color:"#6b7280",


                                lineHeight:"1.5"


                            }}

                            >


                                {

                                    reading.difficulty

                                    ||

                                    "B2"


                                }


                            </p>






                            <span

                            style={{


                                display:"inline-block",


                                marginTop:"15px",


                                padding:"5px 12px",


                                borderRadius:"20px",


                                background:

                                reading.status === "completed"

                                ?

                                "#dcfce7"

                                :

                                "#fef3c7",


                                color:

                                reading.status === "completed"

                                ?

                                "#166534"

                                :

                                "#92400e",


                                fontSize:"13px"


                            }}

                            >


                                {

                                    reading.status

                                }


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