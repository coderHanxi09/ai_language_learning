import {
    Link,
    useLocation
} from "react-router-dom";


import {
    useState
} from "react";





function Navbar(){


    const location = useLocation();



    const [language,setLanguage] = useState(

        localStorage.getItem(
            "learningLanguage"
        )
        ||
        "de"

    );







    function changeLanguage(){


        const newLanguage =

            language === "de"

            ?

            "en"

            :

            "de";



        localStorage.setItem(

            "learningLanguage",

            newLanguage

        );



        setLanguage(

            newLanguage

        );




        // notify all pages

        window.dispatchEvent(

            new Event(
                "languageChange"
            )

        );


    }







    function active(path){


        return (

            location.pathname === path

        );


    }








    const linkStyle = (path)=>({


        textDecoration:"none",


        padding:"8px 14px",


        borderRadius:"10px",


        fontSize:"15px",


        fontWeight:"500",


        transition:"all 0.2s ease",


        color:


            active(path)

            ?

            "#2563eb"

            :

            "#374151",




        background:


            active(path)

            ?

            "#eff6ff"

            :

            "transparent"


    });









    return (



        <nav


        style={{



            position:"sticky",


            top:0,


            zIndex:100,



            display:"flex",


            alignItems:"center",


            gap:"10px",



            padding:"16px 40px",



            background:"#ffffff",



            borderBottom:

            "1px solid #e5e7eb",



            boxShadow:

            "0 2px 12px rgba(0,0,0,0.05)"



        }}



        >









            <Link


            to="/readings"


            style={{


                textDecoration:"none",


                fontSize:"20px",


                fontWeight:"700",


                color:"#111827",


                marginRight:"25px",


                whiteSpace:"nowrap"


            }}


            >

                AI Learning


            </Link>









            <Link


            to="/readings"


            style={

                linkStyle(
                    "/readings"
                )

            }


            >

                Readings


            </Link>









            <Link


            to="/writing"


            style={

                linkStyle(
                    "/writing"
                )

            }


            >

                AI Writing


            </Link>









            <Link


            to="/vocabulary"


            style={

                linkStyle(
                    "/vocabulary"
                )

            }


            >

                Vocabulary


            </Link>









            <Link


            to="/flashcards"


            style={

                linkStyle(
                    "/flashcards"
                )

            }


            >

                Flashcards


            </Link>









            <div


            style={{


                marginLeft:"auto"


            }}


            >





                <button


                onClick={changeLanguage}



                style={{



                    border:"none",



                    background:"#f3f4f6",



                    padding:"10px 16px",



                    borderRadius:"12px",



                    cursor:"pointer",



                    fontSize:"15px",



                    fontWeight:"600",



                    transition:"all 0.2s ease"



                }}



                >





                    {


                        language === "de"


                        ?


                        "🇩🇪 German"


                        :


                        "🇬🇧 English"



                    }





                    <span


                    style={{


                        marginLeft:"8px"


                    }}


                    >

                        ⇄

                    </span>



                </button>





            </div>







        </nav>


    );


}



export default Navbar;