import {
    createContext,
    useContext,
    useState,
    useEffect
} from "react";



const LanguageContext =
    createContext();




export function LanguageProvider({
    children
}){


    const [language,setLanguage] = useState(

        localStorage.getItem(
            "learningLanguage"
        )
        ||
        "de"

    );





    function changeLanguage(newLanguage){


        localStorage.setItem(

            "learningLanguage",

            newLanguage

        );


        setLanguage(
            newLanguage
        );


    }






    useEffect(()=>{


        const current =

            localStorage.getItem(
                "learningLanguage"
            );



        if(current){

            setLanguage(
                current
            );

        }


    },[]);






    return (

        <LanguageContext.Provider

        value={{

            language,

            changeLanguage

        }}

        >

            {children}


        </LanguageContext.Provider>


    );


}






export function useLanguage(){


    return useContext(
        LanguageContext
    );


}