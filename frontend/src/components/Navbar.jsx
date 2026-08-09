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


    const [menuOpen,setMenuOpen] = useState(false);









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









    function closeMenu(){


        setMenuOpen(false);


    }









    const linkStyle=(path)=>({


        textDecoration:"none",


        padding:"10px 14px",


        borderRadius:"10px",


        fontSize:"15px",


        fontWeight:"500",


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


            zIndex:1000,


            background:"#fff",


            borderBottom:

            "1px solid #e5e7eb",


            boxShadow:

            "0 2px 12px rgba(0,0,0,0.05)"


        }}


        >







            <div


            style={{


                display:"flex",


                alignItems:"center",


                justifyContent:"space-between",


                padding:

                "14px clamp(16px,4vw,40px)"


            }}



            >






                {/* Logo */}



                <Link


                to="/readings"


                onClick={closeMenu}


                style={{


                    textDecoration:"none",


                    fontSize:"20px",


                    fontWeight:"700",


                    color:"#111827"


                }}


                >

                    AI Learning

                </Link>









                {/* Desktop Menu */}



                <div


                className="desktop-navbar"


                style={{


                    display:"flex",


                    alignItems:"center",


                    gap:"8px",


                    marginLeft:"20px",


                    flex:1


                }}


                >





                    <Link

                    to="/readings"

                    style={linkStyle("/readings")}

                    >

                        Readings

                    </Link>





                    <Link

                    to="/writing"

                    style={linkStyle("/writing")}

                    >

                        AI Writing

                    </Link>





                    <Link

                    to="/vocabulary"

                    style={linkStyle("/vocabulary")}

                    >

                        Vocabulary

                    </Link>





                    <Link

                    to="/flashcards"

                    style={linkStyle("/flashcards")}

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

                            padding:"10px 14px",

                            borderRadius:"12px",

                            cursor:"pointer",

                            fontWeight:"600"

                        }}


                        >


                            {

                            language==="de"

                            ?

                            "🇩🇪 German"

                            :

                            "🇬🇧 English"


                            }

                            {" ⇄ "}


                        </button>



                    </div>




                </div>









                {/* Mobile Button */}



                <button


                className="mobile-menu-button"


                onClick={()=>setMenuOpen(!menuOpen)}



                style={{


                    display:"none",


                    border:"none",


                    background:"#f3f4f6",


                    borderRadius:"10px",


                    padding:"10px 14px",


                    fontSize:"22px",


                    cursor:"pointer"


                }}



                >

                    ☰

                </button>





            </div>









            {/* Mobile Menu */}



            {

            menuOpen &&


            <div


            className="mobile-menu"


            style={{


                display:"flex",


                flexDirection:"column",


                padding:"10px 16px 20px",


                gap:"8px"


            }}


            >




                <Link

                to="/readings"

                onClick={closeMenu}

                style={linkStyle("/readings")}

                >

                    Readings

                </Link>





                <Link

                to="/writing"

                onClick={closeMenu}

                style={linkStyle("/writing")}

                >

                    AI Writing

                </Link>





                <Link

                to="/vocabulary"

                onClick={closeMenu}

                style={linkStyle("/vocabulary")}

                >

                    Vocabulary

                </Link>





                <Link

                to="/flashcards"

                onClick={closeMenu}

                style={linkStyle("/flashcards")}

                >

                    Flashcards

                </Link>







                <button


                onClick={changeLanguage}


                style={{


                    marginTop:"10px",


                    padding:"12px",


                    border:"none",


                    borderRadius:"12px",


                    background:"#f3f4f6",


                    fontWeight:"600"


                }}



                >


                    {

                    language==="de"

                    ?

                    "🇩🇪 German ⇄"

                    :

                    "🇬🇧 English ⇄"


                    }


                </button>





            </div>


            }





        </nav>


    );


}



export default Navbar;